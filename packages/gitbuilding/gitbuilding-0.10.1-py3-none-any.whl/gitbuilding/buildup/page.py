"""
This submodule deals with BuildUp pages. A Page object is created for each markdown
(buildup) file in the documentation directory.
"""

import posixpath
import logging
from copy import copy, deepcopy

from gitbuilding.buildup.link import FromStepLink
from gitbuilding.buildup.parts import UsedPart
from gitbuilding.buildup.partlist import PartList
from gitbuilding.buildup.buildup import BuildUpParser
from gitbuilding.buildup.files import FileInfo
from gitbuilding.buildup import utilities

_LOGGER = logging.getLogger('BuildUp')

def notify_logger(wrapped_func):
    """
    Notifies the logger of the page being processed
    """
    def wrapper(*args, **kwargs):
        _LOGGER.info('Changing page', extra={'set_active_page': args[0].filename})
        result = wrapped_func(*args, **kwargs)
        _LOGGER.info('Changing page', extra={'set_active_page': None})
        return result
    return wrapper

class Page:
    """
    This class represents one BuildUp page. It can be used to: track its relation to
    other pages using the step_tree; to count the parts in the page; and to export a
    pure markdown page.
    """
    AS_MARKDOWN = 0
    AS_CSV = 1

    def __init__(self, file_obj, doc):
        self._file_obj = deepcopy(file_obj)
        self._doc = doc
        self._overloaded_path = None
        self._replace_links = None
        self._meta_info = {}

        self._part_list = PartList(self._doc.config)
        self._all_parts = None
        self._bom_pages = None

        self._step_tree = None
        self._set_parser(self.get_raw())

    def __repr__(self):
        return f'<Page: {self.filepath}>'

    @property
    def summary(self):
        """
        Page summary is either the title or the first 14 characters plus "..."
        """
        if self.title != "":
            return self.title
        if len(self.raw_md) > 17:
            return self.raw_md[:14]+'...'
        return self.raw_md

    @property
    def raw_md(self):
        """
        Read only property that returns the raw markdown of the page (without frontmatter)
        """
        return self._parser.raw_md

    @property
    def metadata(self):
        """
        Read only property that returns the metadata in from the fontmatter
        """
        return self._parser.metadata

    @property
    def part_data(self):
        """
        Read only property that returns the part data from the front matter.
        """
        return self._parser.part_data

    @property
    def title(self):
        """
        Read only property that returns the title of the page as read
        from the fist H1 level title in page.
        """
        return copy(self._parser.get_title())

    @property
    def filepath(self):
        """
        Read only property that the full filepath of the page relative to
        the root directory of the documentation
        """
        return copy(self._file_obj.path)

    @property
    def pagedir(self):
        '''
        The directory of the input page
        '''
        return posixpath.dirname(self.filepath)

    @property
    def filename(self):
        '''
        The filename of the input page and output pages
        '''
        return posixpath.basename(self.filepath)

    @property
    def meta_info(self):
        '''
        Return a dictionary of any meta information for the page.
        '''
        return self._meta_info

    @property
    def counted(self):
        '''
        Sets whether the main part list has been counted (this happens after running
        count_page)
        '''
        return self._all_parts is not None

    @property
    def part_list(self):
        """
        Returns the part list for the page this is a PartList object.
        """
        return self._part_list

    @property
    def steps(self):
        """
        Returns a list of all the steps in the page (as the url relative to the root
        of the project). This is only the steps defined in the page. Not the full tree.
        This comes directly from the parser there is no garuntee that the the url
        refers to a valid page!
        """
        return self._parser.steps

    @property
    def outputs(self):
        """
        Returns a list of all the output links. This directly by the buildUp
        parser. It is seperate from the CreatedPart objects in the partlist
        as the partlists as the FromStep links need to be resolved before
        making the part list.
        """
        return self._parser.outputs

    @property
    def images(self):
        """
        Returns a list of Image objects, one for each image
        """
        return self._parser.images

    @property
    def plain_links(self):
        """
        Returns a list of Link objects, one for each link that is not a build up link
        """
        return self._parser.plain_links

    @property
    def all_links(self):
        """
        Returns a list of Link objects, one for each link in the page.
        Doesn't return images. See all_links_and_images()
        """
        return self._parser.all_links

    @property
    def all_links_and_images(self):
        """
        Returns a list of Link and Image objects, one for each link/image
        in the page.
        """
        return self._parser.all_links_and_images

    def get_bom_page(self, as_filelist=False):
        """
        Returns the link to the bill of materials pages, or None if there is not
        a bom-link on the page. If as_filelist is True a list of FileInfo objects
        for the bill of materials is returned (if it has been created).
        If None is returned for as_filelist=True but not when as_filelist=False,
        this means that page.generate_output has not been run.
        """
        if as_filelist:
            return self._bom_pages
        return self._bom_urls() if self._has_bom_page() else None

    def _has_bom_page(self):
        bom_links = self._parser.bom_links
        bom_links_oldstyle = self._parser.bom_links_dep
        return len(bom_links) + len(bom_links_oldstyle) > 0

    def _bom_urls(self):
        urls = []
        for filetype in [self.AS_MARKDOWN, self.AS_CSV]:
            urls.append(self._bom_url(filetype))
        return urls

    def _bom_url(self, filetype=None):
        if filetype is None:
            filetype = self.AS_MARKDOWN

        if filetype == self.AS_MARKDOWN:
            return self.filepath[:-3] + "_BOM.md"
        if filetype == self.AS_CSV:
            return self.filepath[:-3] + "_BOM.csv"
        raise ValueError("Filetype for BOM URL not recognised.")

    @property
    def _url_translator(self):
        if self._overloaded_path is None:
            filepath = self.filepath
        else:
            filepath = self._overloaded_path
        return self._doc.url_rules.create_translator(filepath,
                                                     replace_links=self._replace_links)

    @property
    def _part_url_translator(self):
        if self._overloaded_path is None:
            filepath = self.filepath
        else:
            filepath = self._overloaded_path
        return self._doc.url_rules.create_translator(filepath,
                                                     part_translator=True,
                                                     replace_links=self._replace_links)

    @notify_logger
    def _set_parser(self, raw_text):
        self._parser = BuildUpParser(raw_text, self.filepath)

    def rebuild(self, md, overload_path=None):
        """
        This is to replace the raw text and rebuild.
        This can be used to live edit a single page.
        md is the input markdown to use instead of the pages markdown
        overload_path is used to overload the path input to the
          URL_Translator. This is useful if you are displaying the
          live edited text and a different URL.
        """

        self._part_list = PartList(self._doc.config)
        self._all_parts = None
        self._step_tree = None
        self._bom_pages = None
        self._meta_info = {}

        self._set_parser(md)

        self.get_step_tree()
        self.count()

        if self._doc.page_order.number_of_paths == 0:
            nav_pagelist = []
        elif self._doc.page_order.number_of_paths == 1:
            nav_pagelist = self._doc.page_order.nav_pagelists[0]
        else:
            #Relates to issue #175
            nav_pagelist = self._doc.page_order.nav_pagelists[0]
        result = self.generate_output(nav_pagelist, overload_path)
        return result

    def __eq__(self, other):
        """
        Checks for equality using the file name. Used to find pages in lists.
        """
        return self.filepath == other

    def get_raw(self):
        """
        Returns the raw BuildUp file contents.
        """
        return self._file_obj.content

    def _resolve_from_step_links(self, pagelist):
        """
        Look for outputs in previous pages
        """
        fs_links = [link for link in self._parser.all_links if isinstance(link, FromStepLink)]
        if len(fs_links) == 0:
            return
        if self not in pagelist:
            _LOGGER.warning('Cannot reference a part using FromStep on a page that is '
                            'not in the step tree.')
            return

        index = pagelist.index(self)
        prev_pages = self._doc.get_page_objects(pagelist[:index])
        outputs = []
        for page in prev_pages:
            outputs += page.outputs
        for from_step_link in fs_links:
            from_step_link.resolve(outputs)

    def _reset_from_step_links(self):
        fs_links = [link for link in self._parser.all_links if isinstance(link, FromStepLink)]
        for from_step_link in fs_links:
            from_step_link.reset()

    @notify_logger
    def count(self):
        """
        Counts all of the part on the page and puts them into a PartList object
        """
        if self.counted:
            return

        for output in self.outputs:
            self._part_list.count_link(output)

        part_links = self._parser.reference_defined_parts + self._parser.inline_parts
        for part_link in part_links:
            self._part_list.count_link(part_link)

        for part in self._part_list.used_parts:
            if part.linklocation == '' and not part.from_step:
                _LOGGER.warning('"%s" has no link specified',
                                part.name,
                                extra={'fussy':True})

        self._all_parts = PartList(self._doc.config)
        self._all_parts.merge(self._part_list)
        for step in self._doc.get_page_objects(self.steps):
            # if step page is not already counted it will be counted when accessing
            # all parts property
            self._all_parts.merge(step.all_parts)

    @property
    def all_parts(self):
        """
        Returns PartList of of all parts for the page and all steps the page references.
        If the page has not yet been counted it will run Page.count.
        """

        if not self.counted:
            self.count()
        return self._all_parts

    def _write_bom(self, processed_text, nav_pagelist, replace_links):
        """
        Write the bill of the materials into text and links to the bill of materials
        page if required. Currently also builds the BOM page - split later
        """
        # Add all BOMs into the page
        boms = self._parser.inline_boms
        if len(boms) > 0:
            bom_text = self._all_parts.bom_md(self._doc.config.page_bom_title,
                                              self._part_url_translator,
                                              exclude_refs=self._part_list)
        for bom in boms:
            processed_text = processed_text.replace(bom, bom_text)

        # Add links to bill of materials page and make page
        if self._has_bom_page():
            self._bom_pages = self.make_bom_page(nav_pagelist, replace_links)
            bom_links = self._parser.bom_links
            bom_links_oldstyle = self._parser.bom_links_dep
            for bomlink in bom_links:
                bom_url = self._url_translator.simple_translate(self._bom_pages[0].path)
                bom_url_csv = self._url_translator.simple_translate(self._bom_pages[1].path)
                md_link = f"[{bomlink.linktext}]({bom_url})"
                csv_link = f" [(csv)]({bom_url_csv})"
                rep_text = md_link + csv_link
                processed_text = processed_text.replace(bomlink.fullmatch, rep_text)
            for bomlink in bom_links_oldstyle:
                bom_url = self._url_translator.simple_translate(self._bom_pages[0].path)
                processed_text = processed_text.replace(bomlink, f"{bom_url}")
        return processed_text

    def _write_in_page_step_headings(self, processed_text):
        """
        Writes in the headings for each in-page step. Adds ID for in-page links,
        and class for fancy CSS
        """
        for i, in_page_step in enumerate(self._parser.in_page_steps):
            kramdown_block = "{:"
            kramdown_block += f'id="{in_page_step["id"]}" '
            kramdown_block += 'class="page-step"}'
            step_heading = f"## Step {i+1}: {in_page_step['heading']} {kramdown_block}"
            processed_text = processed_text.replace(in_page_step["fullmatch"],
                                                    step_heading)
        return processed_text

    def _replace_step_links(self, processed_text):
        """
        Replace all step links it with processed markdown
        """
        for link in self._parser.step_links:
            #Overriding the input link text if it was just a .
            text_override = None
            if link.linktext == ".":
                page = self._doc.get_page_by_path(link.link_rel_to_root)
                if page is not None:
                    text_override = page.title
            rep_text = link.link_md(self._url_translator, text_override)
            processed_text = processed_text.replace(link.fullmatch, rep_text)
        return processed_text

    def _replace_plain_links(self, processed_text):
        """
        Replace all non buildup links it with processed markdown
        the only processing here is the url translation rules
        """
        for link in self._parser.plain_links:
            rep_text = link.link_md(self._url_translator)
            processed_text = processed_text.replace(link.fullmatch, rep_text)
        return processed_text

    def _replace_outputs(self, processed_text):
        """
        Replace all outputs with anchor points
        """
        for output in self._parser.outputs:
            rep_text = output.link_md(None)
            processed_text = processed_text.replace(output.fullmatch, rep_text)
        return processed_text

    def _replace_zip_links(self, processed_text):
        """
        Replace all zip links with processed markdown
        """
        for zip_link in self._parser.zip_links:
            rep_text = zip_link.link_md(self._url_translator)
            processed_text = processed_text.replace(zip_link.fullmatch, rep_text)
        return processed_text

    def _replace_images(self, processed_text):
        """
        Replace all images it with processed markdown
        the only processing here is the url translation rules
        """
        for image in self._parser.images:
            previewer =  self._doc.previewer_for_uri(image.image_rel_to_root)
            if previewer is None:
                if image.buildup_data is not None:
                    _LOGGER.warning('Image has unused buildup data',
                                    extra={'fussy':True})
                rep_text = image.image_md(self._url_translator)
            else:
                if 'previewers_used' in self._meta_info:
                    if previewer.name not in self._meta_info['previewers_used']:
                        self._meta_info['previewers_used'].append(previewer.name)
                else:
                    self._meta_info['previewers_used'] = [previewer.name]
                location = image.output_url(self._url_translator)
                rep_text = previewer.display_code(location,
                                                  image.alttext,
                                                  image.hovertext,
                                                  image.buildup_data)
            processed_text = processed_text.replace(image.fullmatch, rep_text)
        return processed_text

    def _replace_part_links(self, processed_text):
        """
        Replace all part links with processed (Kramdown) markdown
        """
        for link in self._parser.part_links:
            rep_text = f'[{link.linktext}]'
            part = self._part_list.getpart(link.linktext)
            if part is not None:
                if part.location_undefined:
                    rep_text += '{: Class="missing"}'
            processed_text = processed_text.replace(link.fullmatch, rep_text)
        return processed_text

    def _replace_link_refs(self, processed_text):
        """
        Replace link references with BuildUp data and replace it with a
        standard markdown link reference.
        """

        for link_ref in self._parser.link_refs:
            translator = self._url_translator
            if link_ref.linktext in self._part_list:
                translator = self._part_url_translator
            processed_text = processed_text.replace(link_ref.fullmatch,
                                                    link_ref.link_ref_md(translator))
        return processed_text

    def _add_missing_link_refs(self, processed_text):
        """
        Adds link reference for any part that doesn't have one
        """
        for part in self._part_list:
            if isinstance(part, UsedPart):
                refnames = [ref.linktext for ref in self._parser.link_refs]
                if part.name not in refnames:
                    processed_text += "\n"
                    processed_text += part.link_ref_md(self._part_url_translator)
        return processed_text

    def _add_bottom_navigation(self, processed_text, nav_pagelist, overload_path=None):

        page_ordering = utilities.nav_order_from_nav_pagelist(nav_pagelist)

        path = self.filepath if overload_path is None else overload_path
        if path in page_ordering:
            processed_text += "\n\n---\n\n"
            index = page_ordering.index(path)

            if index != 0:
                link = self._url_translator.simple_translate(page_ordering[index-1])
                processed_text += f"[Previous page]({link})"
                prev_page = True
            else:
                prev_page = False

            if index != len(page_ordering)-1:
                if prev_page:
                    processed_text += " | "
                link = self._url_translator.simple_translate(page_ordering[index+1])
                processed_text += f"[Next page]({link})"
        return processed_text

    @notify_logger
    def generate_output(self, nav_pagelist, overload_path=None, replace_links=None):
        """
        Does the final stages of building the output markdown
        """
        self._overloaded_path = overload_path
        self._replace_links = replace_links
        pagelist = [page_tuple[0] for page_tuple in nav_pagelist]
        self._resolve_from_step_links(pagelist)
        processed_text = copy(self.raw_md)
        if self == self._doc.landing_page:
            if self._doc.config.remove_landing_title:
                processed_text = processed_text.replace(self._parser.get_title_match(), "", 1)
        processed_text = self._write_bom(processed_text, nav_pagelist, replace_links)
        processed_text = self._write_in_page_step_headings(processed_text)
        processed_text = self._replace_step_links(processed_text)
        processed_text = self._replace_part_links(processed_text)
        processed_text = self._replace_outputs(processed_text)
        processed_text = self._replace_zip_links(processed_text)
        processed_text = self._replace_plain_links(processed_text)
        processed_text = self._replace_link_refs(processed_text)
        processed_text = self._add_missing_link_refs(processed_text)
        #replace images last as they may be inside other links
        processed_text = self._replace_images(processed_text)
        if self.part_data is not None:
            processed_text += self.part_data.page_markdown
        if not self._doc.config.remove_bottom_nav:
            processed_text = self._add_bottom_navigation(processed_text, nav_pagelist)
        self._reset_from_step_links()
        self._overloaded_path = None
        self._replace_links = None
        return processed_text

    @notify_logger
    def get_step_tree(self, breadcrumbs=None):
        """
        This function traverses returns the step tree for a page. Any page that is
        finding its current step tree should pass it's breadcrumbs
        """

        if breadcrumbs is None:
            breadcrumbs = []
        else:
            breadcrumbs = copy(breadcrumbs)

        if self.filepath in breadcrumbs:
            trail = ''
            for crumb in breadcrumbs:
                trail += crumb + ' -> '
            trail += self.filepath
            _LOGGER.warning("The steps in the documentation form a loop! [%s] "
                            "This can cause very weird behaviour.",
                            trail,
                            extra={'this':'that'})
            return {self.filepath: []}

        if self._step_tree is None:
            breadcrumbs.append(self.filepath)
            self._parse_step_tree(breadcrumbs)
        return self._step_tree

    def _parse_step_tree(self, breadcrumbs=None):
        """
        This function traverses the steps in the page to create a complete downward step tree
        it uses the same function of other steps until all pages downstream have completed.
        Breadcrumbs showing the path down the step tree is passed on to allow checks for loops
        in the step definition. This stops infinite loops occurring.
        """
        if breadcrumbs is None:
            breadcrumbs = [self.filepath]

        list_of_subtrees = []
        for step in self._doc.get_page_objects(self.steps, warn=True):
            list_of_subtrees.append(step.get_step_tree(breadcrumbs))
        # Note that page object is not hashable so the step tree key is the path.
        self._step_tree = {self.filepath: list_of_subtrees}

    def make_bom_page(self, nav_pagelist, replace_links):
        """
        Makes separate Bill of materials page for the all parts on this page (including those
        in steps). Returns the filepath of the resulting file and the markdown in a dictionary
        """

        md_path = self._bom_url()
        csv_path = self._bom_url(self.AS_CSV)

        bom_intro = f"Download this as a [CSV file]({posixpath.basename(csv_path)})"
        # Fine to use self._url_translator as the BOM page will be in same
        # output directory
        md = self._all_parts.bom_md("# Bill of Materials", self._part_url_translator, intro=bom_intro)
        if not self._doc.config.remove_bottom_nav:
            md = self._add_bottom_navigation(md, nav_pagelist, overload_path=md_path)
        csv = self._all_parts.bom_csv(self._doc)

        if replace_links is not None:
            if md_path in replace_links:
                md_path = replace_links[md_path]
            if csv_path in replace_links:
                csv_path = replace_links[csv_path]

        md_file = FileInfo(md_path, dynamic_content=True, content=md)
        csv_file = FileInfo(csv_path, dynamic_content=True, content=csv)
        return md_file, csv_file
