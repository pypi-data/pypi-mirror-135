"""
This submodule contains the main BuildUp Documentation class.
"""

from copy import copy, deepcopy
import fnmatch
import logging
from dataclasses import is_dataclass
from gitbuilding.buildup.page import Page
from gitbuilding.buildup.libraries import Libraries
from gitbuilding.buildup.files import FileInfo
from gitbuilding.buildup.url import URLRules
from gitbuilding.buildup.link import LibraryLink
from gitbuilding.buildup.config import ConfigSchema
from gitbuilding.buildup.pageorder import PageOrder
from gitbuilding.buildup import utilities

_LOGGER = logging.getLogger('BuildUp')

class Documentation:
    """
    This class represents the documentation in a BuildUp project. All other objects
    representing Pages, Libraries, Parts, Partlists, Links, etc are held within this
    the Documentation object. The most simple use of the Documentation object is to
    initialise it with a configuration and then run `buildall` with a list of input
    files.
    """

    def __init__(self, configuration, url_rules=None, previewers=None):
        self._filelist = None
        self._landing_page = None
        self._pages = []
        self._libs = Libraries([])
        self._output_files = []
        self._page_order = None
        if is_dataclass(configuration):
            self._input_config = configuration
        elif isinstance(configuration, dict):
            self._input_config = ConfigSchema().load(configuration)
        else:
            raise TypeError("configuration should be a dataclass or dictionary")
        self._config = deepcopy(self._input_config)

        if url_rules is None:
            self._url_rules = URLRules()
        else:
            if not isinstance(url_rules, URLRules):
                raise TypeError('url_rules must a URLRules object')
            self._url_rules = url_rules
        if previewers is None:
            self._previewers = []
        else:
            self._previewers = previewers


    @property
    def config(self):
        """
        Read only property that returns the config object
        """
        return self._config

    @property
    def landing_page(self):
        """
        Somewhat confusing read only property. This option is the
        Page object of the landing page. `config.landing_page` is
        the path to the landing page. This may be changed in future
        versions!
        """
        return self._landing_page

    @property
    def pages(self):
        """
        Read only property that returns the list of pages (list of
        Page objects) in the documentation. The list is returned so any
        modifications to the returned list will affect the Documentation.
        """
        return self._pages

    @property
    def page_order(self):
        """
        Returns the PageOrder object describing the paths through the documentation
        """
        return self._page_order

    @property
    def libs(self):
        """
        Read only property that returns the list of libraries (list of
        Library objects) in the documentation. The list is returned so any
        modifications to the returned list will affect the Documentation.
        """
        return self._libs

    @property
    def output_files(self):
        '''
        List of all output files as FileInfo objects
        '''
        return self._output_files

    @property
    def previewers(self):
        return self._previewers

    @property
    def url_rules(self):
        '''
        Returns the URLRules object to set how output urls are formatted
        '''

        return self._url_rules

    def get_file(self, path):
        '''If a file with at this path in the output exists a
        FileInfo object is returned

        If the file is not in the output None is returned'''
        if path in self._output_files:
            return self.output_files[self.output_files.index(path)]
        return None

    def previewer_for_uri(self, uri):
        """
        Returns the previewer for this file or link. Returns None if cannot
        preview
        """
        for previewer in self.previewers:
            if previewer.can_preview(uri):
                return previewer
        return None

    def get_page_by_path(self, filepath):
        """
        Returns the page object matching the file path, or None if missing
        """
        if filepath in self._pages:
            return self._pages[self._pages.index(filepath)]
        return None

    def get_page_objects(self, path_list, warn=False):
        """
        Returns a list of valid page objects for an input list of paths. Any missing
        paths are silently ignored. Therefore an invalid input list results in an
        empty output list. Set `warn=True` to log a warning for each missing page
        """
        obj_list = []
        for path in path_list:
            if path in self._pages:
                obj_list.append(self.get_page_by_path(path))
            elif warn:
                _LOGGER.warning('Missing page "%s"', path)
        return obj_list

    def _create_all_pages(self, filelist):
        """
        Creates a Page object for each markdown page in the input filelist.
        """

        self._pages = []
        for file_obj in filelist:
            if file_obj.dynamic_content and file_obj.path.endswith('.md'):
                self._pages.append(Page(file_obj, self))


    def _check_landing_page(self):
        """
        Checks if the landing page exists. Also looks for index.md as this
        is the standard landing page once we change to html
        """

        if "index.md" in self._pages:
            if self._config.landing_page is None:
                self._config.landing_page = "index.md"
            elif self._config.landing_page != "index.md":
                _LOGGER.warning("Landing page is set to %s but also `index.md` exists. "
                                "This may cause unreliable behaviour",
                                self._config.landing_page)

        if self._config.landing_page in self._pages:
            self._landing_page = self._pages[self._pages.index(self._config.landing_page)]

    def _make_navigation(self):
        """
        If the navigation is not set in the configuration a Navigation
        is automatically created
        """
        if self._config.navigation != []:
            self._check_and_complete_subnav()

        elif self.page_order.number_of_paths == 0:
            url_translator = self.url_rules.create_translator('index.md')
            pages = [page for page in self._pages if page != self._landing_page]
            for page in pages:
                link = url_translator.simple_translate(page.filepath)
                self._config.navigation.append({'title': page.summary, 'link': link})
        else:
            for n in range(self.page_order.number_of_paths):
                nav_pagelist = self.page_order.nav_pagelists[n]
                replace_links = self.page_order.link_replacement_dictionaries[n]
                url_translator = self.url_rules.create_translator('index.md',
                                                                  replace_links=replace_links)
                nav = self._make_navigation_from_page_order(nav_pagelist, url_translator)
                self._config.navigation += nav

    def _check_and_complete_subnav(self):
        #A standard translatior to translate urls into output format
        url_translator = self.url_rules.create_translator('index.md')
        for [n, nav_item] in enumerate(self._config.navigation):
            link = nav_item["link"]
            if link in self._page_order.duplicates:
                _LOGGER.warning("Creating navigation link for duplicated page.")
                continue
            if self._config.autocompletesubnav:
                has_subnav = "subnavigation" in nav_item
                on_pagelist = link in self.page_order.masterlist
                if (not has_subnav) and on_pagelist:
                    this_sub_nav, replace_links = self.page_order.get_nav_pagelist_for_page(link)
                    # A translatior that replaces pages to the correct version for the active path
                    # of the documentation
                    this_translator = self.url_rules.create_translator('index.md',
                                                                       replace_links=replace_links)
                    nav = self._make_navigation_from_page_order(this_sub_nav, this_translator)
                    nav[0]["title"] = nav_item["title"]
                    self._config.navigation[n] = nav[0]
                    continue
            self._translate_nav_item(nav_item, url_translator)
            

    def _translate_nav_item(self, nav_item, url_translator):
        nav_item["link"] = url_translator.simple_translate(nav_item["link"])
        if "subnavigation" in nav_item:
            for sub_nav_item in nav_item["subnavigation"]:
                self._translate_nav_item(sub_nav_item, url_translator)

    def _make_navigation_from_page_order(self, nav_pagelist, url_translator):

        #if the first page in the page order is the landing page then depth 0, is only
        # the landing page which is ommited from the navigation. As such the base depth
        # becomes 1

        def append_nav_item(nav, nav_item, nav_depth):
            if nav_depth == 0:
                nav.append(nav_item)
            elif nav_depth == 1:
                parent_item = nav[-1]
                if "subnavigation" not in parent_item:
                    parent_item["subnavigation"] = []
                parent_item["subnavigation"].append(nav_item)

        nav = []
        basedepth = 1 if self._landing_page == nav_pagelist[0][0] else 0
        for page_path, depth, bom in nav_pagelist:
            page = self.get_page_by_path(page_path)
            link = url_translator.simple_translate(page.filepath)
            nav_item = {'title': page.summary, 'link': link}
            nav_depth = depth-basedepth
            append_nav_item(nav, nav_item, nav_depth)
            if bom is not None:
                bom_link = url_translator.simple_translate(bom)
                bom_nav_item = {'title': "Bill of Materials", 'link': bom_link}
                append_nav_item(nav, bom_nav_item, nav_depth+1)
        return nav

    def _generate_output_files(self):
        """
        Returns a list of all files that need to be output
        for plain markdown output.
        """
        all_output_files = []

        for page in self._pages:
            #Skip any pages on a step tree, they will be generated later.
            if page in self._page_order.masterlist:
                continue
            self._append_outputs_for_page(all_output_files, page, [])

        for n in range(self._page_order.number_of_paths):
            replace_links = self._page_order.link_replacement_dictionaries[n]
            nav_pagelist = self._page_order.nav_pagelists[n]
            for page_name in self._page_order.pagelists[n]:
                if page_name in replace_links:
                    out_path = replace_links[page_name]
                else:
                    out_path = page_name
                duplicate_of = None if page_name == out_path else page_name
                page = self.get_page_by_path(page_name)
                self._append_outputs_for_page(all_output_files,
                                              page,
                                              nav_pagelist,
                                              out_path,
                                              replace_links,
                                              duplicate_of)

        self._append_page_for_duplicates(all_output_files)

        return all_output_files

    def _append_page_for_duplicates(self, all_output_files):
        for duplicate in self._page_order.duplicates:
            page = self.get_page_by_path(duplicate)
            links = []
            # Duplicates is a dictionary.
            # Each page that is duplicated is a key who's value is the list of the root of
            # each documentation path that contains the page
            for root_pagename in self._page_order.duplicates[duplicate]:
                #For each copy find the output path, and the title of the root page.
                root_page = self.get_page_by_path(root_pagename)
                list_no = self._page_order.get_list_number(root_pagename)
                replace_links = self._page_order.link_replacement_dictionaries[list_no]
                url_translator = self.url_rules.create_translator(duplicate,
                                                                  replace_links=replace_links)
                translated_target = url_translator.simple_translate(duplicate)
                links.append((root_page.title, translated_target))
            content = ("# There are multiple versions of this page.\n\nPlease select one "
                       "of these projects:\n\n")
            for link in links:
                content += f"* [{link[0]}]({link[1]})\n"
            content += "\n"
            file_obj = FileInfo(page.filepath, dynamic_content=True, content=content)
            all_output_files.append(file_obj)

    def _append_outputs_for_page(self,
                                 all_output_files,
                                 page,
                                 nav_pagelist,
                                 overloaded_path=None,
                                 replace_links=None,
                                 duplicate_of=None):

        page_content = page.generate_output(nav_pagelist, overloaded_path, replace_links)
        outpath = overloaded_path if overloaded_path is not None else page.filepath
        file_obj = FileInfo(outpath,
                            dynamic_content=True,
                            content=page_content,
                            meta_info=page.meta_info,
                            duplicate_of=duplicate_of)
        all_output_files.append(file_obj)
        if page.get_bom_page(as_filelist=True) is not None:
            all_output_files += page.get_bom_page(as_filelist=True)
        for link in page.all_links_and_images:
            linked_file = None
            if link.content_generated:
                if isinstance(link, LibraryLink):
                    linked_file = self._libs.part_page(*link.library_location)
                elif link.is_zip:
                    link_urls = [link.link_rel_to_root_no_preview for link in page.all_links]
                    link_urls = [link_url for link_url in link_urls if link_url is not None]
                    matching = fnmatch.filter(link_urls, link.zip_pattern)
                    linked_file = link.as_output_file(files_to_zip=matching)
                else:
                    link_path = utilities.strip_internal_links(link.link_rel_to_root)
                    if link_path not in self._filelist + self._page_order.filenames_of_duplicates:
                        _LOGGER.warning("Linked markdown page does not exist: %s", link_path)
            else:
                linked_file = link.as_output_file()
            if linked_file is not None:
                if linked_file not in all_output_files:
                    if not(linked_file.dynamic_content or linked_file in self._filelist):
                        _LOGGER.warning("Linked file does not exist: %s", linked_file.path)
                    # append even if missing to avoid duplicate warnings
                    all_output_files.append(linked_file)

    def _append_preview_pages(self, all_output_files):
        for output_file in all_output_files:
            output_path = output_file.path
            if self.previewer_for_uri(output_path) is not None:
                previewer = self.previewer_for_uri(output_path)
                if previewer.create_preview_page:
                    prev_path = previewer.preview_page_uri(output_path)
                    md = previewer.preview_page_content(output_path)
                    file_obj = FileInfo(prev_path,
                                        dynamic_content=True,
                                        content=md,
                                        meta_info={'previewers_used': previewer.name})
                    all_output_files.append(file_obj)

    def buildall(self, filelist):
        """
        Builds the output documentation as a list of FileInfo objects based on the input
        documentation directory defined by `filelist` (also a list of FileInfo objects)
        """
        # By deepcopying the input config this refreshes the config state
        # if this is not the first time the documentation has run the config will
        # contain information generated from the buildup files, such as navigation or
        # project title
        self._filelist = filelist
        self._config = deepcopy(self._input_config)
        self._libs = Libraries(filelist)
        self._create_all_pages(filelist)
        self._check_landing_page()

        if self._config.title is None:
            if self._config.landing_page is None:
                self._config.title = "Untitled project"
            else:
                self._config.title = self._landing_page.title

        # NOTE: If changing the key page functions below be sure to also change
        # the Page.rebuild

        # build step_tree for all pages
        trees = []
        for page in self._pages:
            trees.append(page.get_step_tree())

        self._page_order = PageOrder(trees, self)

        # count parts on pages and sub pages
        for page in self._pages:
            page.count()

        self._make_navigation()
        self._output_files = self._generate_output_files()
        self._append_preview_pages(self._output_files)
        self._append_forced_outputs(self._output_files)

        return self._output_files

    def _append_forced_outputs(self, outputs):
        for filename in self._config.force_output:
            if utilities.contains_wildcards(filename):
                matches = utilities.match_files(filename, self._filelist)
                outputs += matches
            elif filename not in outputs:
                try:
                    #append this file to the output list
                    matched_file = self._filelist[self._filelist.index(filename)]
                    outputs.append(copy(matched_file))
                except ValueError:
                    _LOGGER.warning('"%s" is on the forced output list but the file'
                                    'cannot be found', filename)

    def output_for_pathlist(self, list_number):
        """
        Returns a list of all files that need to be output if only the documentation
        for a specific pagelist is being generated. This function runs based on the
        outputs created the last time build_all was run.
        """

        nav_pagelist = self._page_order.nav_pagelists[list_number]
        output_files = []
        for page_name, _, _ in nav_pagelist:
            page = self.get_page_by_path(page_name)
            self._append_outputs_for_page(output_files, page, nav_pagelist)

        self._append_preview_pages(output_files)
        self._append_forced_outputs(output_files)
        return output_files
