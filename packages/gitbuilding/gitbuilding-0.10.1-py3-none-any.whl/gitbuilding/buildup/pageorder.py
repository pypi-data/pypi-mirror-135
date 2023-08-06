"""
This submodule constains the PageOrder class which is used to store and manipulate the paths
through the buildup documentation.
"""

import posixpath
from copy import copy, deepcopy
import logging

_LOGGER = logging.getLogger('BuildUp')

def _tree2list(tree, depth=0):
    """
    Input is a step tree for a page, output is a list detailing the order the pages
    should be displayed in. The list containts tuples, these tuples have two elements,
    the pagename, and the depth in the steptree.
    """
    pagename = list(tree.keys())[0]
    pagelist = [(pagename, depth)]
    for subtree in tree[pagename]:
        pagelist += _tree2list(subtree, depth+1)
    return pagelist

class PageOrder():
    """
    A PageOrder is object is initialised with the step trees from every page and the landing page.
    It will calculate the number of paths through the documentation, these can be accessed as
    trees or as lists.
    The lists have two versions, the list of the pages, and the list for navigation, the list for
    navigation also include bill of materials.
    """

    def __init__(self, trees, doc_obj):

        self._trees = deepcopy(trees)
        self._tuple_pagelists = [_tree2list(tree) for tree in self._trees]
        self._remove_empty_trees_and_lists()
        self._remove_non_rooted_trees()
        self._include_boms(doc_obj)
        if len(self.pagelists) > 0:
            self._validate_pagelists(doc_obj.landing_page)
        self._generate_masterlist_and_duplicates()

    @property
    def number_of_paths(self):
        """
        Read-only property which returns a the number of paths through the documentation
        """
        return len(self._tuple_pagelists)

    @property
    def trees(self):
        """
        Read-only property which returns a copy of the step trees. One for each path through
        the documentation.
        """
        return deepcopy(self._trees)

    @property
    def masterlist(self):
        """
        Read-only property which returns a list of all pages that are on any step list. The items
        in each list are just the page_names.
        """
        return copy(self._masterlist)

    @property
    def duplicates(self):
        """
        Read-only property which returns a dictionary. The keys are the pagenames of any pages
        that are used in more than one path through the documentation, the value is a list of
        the pagenames of the roots of those paths.
        """
        return deepcopy(self._duplicates)

    @property
    def filenames_of_duplicates(self):
        filenames = []
        for duplicate in self.duplicates:
            for root_pagename in self.duplicates[duplicate]:
                list_no = self.get_list_number(root_pagename)
                replacement_dict = self.link_replacement_dictionaries[list_no]
                filenames.append(replacement_dict[duplicate])
        return filenames

    @property
    def pagelists(self):
        """
        Read-only property which returns a copy of the pagelists. One list for each path through
        the documentation. The items in each list are just the page_names.
        """
        pagelists = []
        for pagelist in self._tuple_pagelists:
            pagelists.append([page_tuple[0] for page_tuple in pagelist])
        return pagelists

    @property
    def nav_pagelists(self):
        """
        Read-only property which returns a copy of the pagelists. One list for each path through
        the documentation. The items in each list are a tuple of the page_name, the depth (i.e.
        0 for top level pages, 1 their steps, etc), and the corresponding bill of materials page.
        """
        nav_pagelists = []
        for tuple_pagelist in self._tuple_pagelists:
            nav_pagelist = []
            for page_tuple in tuple_pagelist:
                # Note the 3rd element in the tuple is either None or a list of all bom_pages
                # navigation only reqires the markdown bom page thich is the first in this list.
                bom_page_md = None if page_tuple[2] is None else page_tuple[2][0]
                nav_pagelist.append([page_tuple[0], page_tuple[1], bom_page_md])
            nav_pagelists.append(nav_pagelist)
        return nav_pagelists

    @property
    def link_replacement_dictionaries(self):
        """
        Read-only property which returns a copy of the pagelists. One list for each path through
        the documentation. The items in each list are a tuple of the file name in the input
        documentation and the file name in the output doucumentation.
        """
        out_lists = []
        for tuple_pagelist in self._tuple_pagelists:
            # first element in the lists is the first page, first element in the nav tuple
            # is the path
            rootpage_path = tuple_pagelist[0][0]
            # subdirectory is the first page in the page order minus the '.md'
            subdir = rootpage_path[:-3]

            in_paths = []
            out_paths = []
            for page_path, _, bom_pages in tuple_pagelist[1:]:
                if page_path in self._duplicates:
                    in_paths.append(page_path)
                    out_paths.append(posixpath.join(subdir, page_path))
                    if bom_pages is not None:
                        for bom_page in bom_pages:
                            in_paths.append(bom_page)
                            out_paths.append(posixpath.join(subdir, bom_page))
            out_lists.append(dict(zip(in_paths, out_paths)))
        return out_lists

    def get_list_number(self, root_pagename):
        """
        Return the number (index) of the pagelist with the input page name as root. If the input
        page is not a root of any pagelist then reutn None.
        """
        list_roots = [plist[0] for plist in self.pagelists]
        try:
            return list_roots.index(root_pagename)
        except ValueError:
            return None

    def _validate_pagelists(self, landing_page):
        """
        Checks the page order doesn't have unexpected problems like repeated steps. The
        landing page doesn't need to be in the page order list, but if it is in it must
        be at the start.
        The function does not return anything, it just logs any issues
        """
        for pagelist in self.pagelists:
            if len(pagelist) == 0:
                return

            if landing_page in pagelist[1:]:
                _LOGGER.warning('The landing page cannot be a step of another page.')

            #warn if steps are repeated
            if len(set(pagelist)) != len(pagelist):
                _LOGGER.warning('The defined page order has the same step repeated: "%s"',
                                '->'.join(pagelist))

    def _remove_empty_trees_and_lists(self):
        """
        Some page lists contain only the name of the page the tree was read from as
        they have no steps. This function removes those lists and trees.
        """
        poplist = []
        for n, pagelist in enumerate(self._tuple_pagelists):
            if len(pagelist) == 1:
                poplist.append(n)
        #pop in reverse
        for n in poplist[::-1]:
            self._tuple_pagelists.pop(n)
            self._trees.pop(n)

    def _remove_non_rooted_trees(self):
        """
        This function removes any trees (and corresponding pagelists) that are not the
        root of a step tree.
        """
        #list of pagelists to remove as they are a sub-part of another list
        poplist = []
        for n, pagelist in enumerate(self._tuple_pagelists):
            for otherlist in self._tuple_pagelists[0:n]+self._tuple_pagelists[n+1:]:
                otherlist_names = [page_tuple[0] for page_tuple in otherlist]
                if pagelist[0][0] in otherlist_names:
                    poplist.append(n)
                    break
        #pop in reverse
        for n in poplist[::-1]:
            self._tuple_pagelists.pop(n)
            self._trees.pop(n)

    def _include_boms(self, doc_obj):
        """
        Add bills of materials to the pagelists tuple.
        """
        for pagelist in self._tuple_pagelists:
            for n, page_tuple in enumerate(pagelist):
                pagename = page_tuple[0]
                page = doc_obj.get_page_by_path(pagename)
                pagelist[n] = (page_tuple[0], page_tuple[1], page.get_bom_page())

    def _generate_masterlist_and_duplicates(self):
        """
        Generate a list of all pages that are in step trees
        """
        self._masterlist = []
        reused_pages = []
        for pagelist in self.pagelists:
            for pagename in pagelist:
                if pagename not in self._masterlist:
                    self._masterlist.append(pagename)
                elif pagename not in reused_pages:
                    reused_pages.append(pagename)

        self._duplicates = {}
        for page in reused_pages:
            self._duplicates[page] = [plist[0] for plist in self.pagelists if page in plist]

    def get_nav_pagelist_for_page(self, page):
        """
        return a navigation pagelist rooted at the specific page, and also returns
        the replacement links to go tot he correct version of duplicated pages.
        """
        if page not in self.masterlist:
            raise IndexError(f"{page} is not in any page order")

        page_ind = None
        nav_pagelist = None
        replace_links = None
        for n, pagelist in enumerate(self.pagelists):
            if page in pagelist:
                page_ind = pagelist.index(page)
                nav_pagelist = self.nav_pagelists[n]
                if self.number_of_paths == 0:
                    replace_links = None
                else:
                    replace_links = self.link_replacement_dictionaries[n]
                break
        if (page_ind is None) or (nav_pagelist is None):
            raise RuntimeError("Navigation page not found when in masterlist")

        sub_pageslist = [nav_pagelist[page_ind]]
        page_level = sub_pageslist[0][1]
        ind = page_ind + 1
        while ind < len(nav_pagelist) and nav_pagelist[ind][1] > page_level:
            sub_pageslist.append(nav_pagelist[ind])
            ind+=1
        return sub_pageslist, replace_links
