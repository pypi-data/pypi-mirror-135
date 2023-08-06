"""
The url module deals with URL translation in buildup. URL translation includes:
changing urls between relative and absolute; adjusting relative paths when the
same link is used in another location; and applying custom modifier functions to
the paths.
"""

import posixpath
import logging
from gitbuilding.buildup.utilities import as_posix

_LOGGER = logging.getLogger('BuildUp')

def split_anchor(url):
    """
    Splits off the anchor from the url. Will escape any other
    anchor characters. Returns a list of the url without anchor
    and the anchor
    """
    split_url = url.split('#')
    if len(split_url) == 2:
        return split_url
    if len(split_url) == 1:
        split_url.append('')
        return split_url
    # Escape other hashes and return
    return [r'%23'.join(split_url[:-1]), split_url[-1]]

class URLRules:
    """
    This class holds the rules for translating the url in the BuildUp into the
    final output url. When initialised the only value set is whether output paths
    will be relative to the root of the documentation directory. If false they
    will be output relative to the page they are on (default).
    The `add_modifier` function can be used to add custom functions that modify the
    urls further, for example to prepend a baseurl, or to change a file extension.
    """

    def __init__(self, rel_to_root=False):
        self._rel_to_root = rel_to_root
        self._modifiers = []
        # May want to be more intelligent with the modifer list
        # storage if we add more options
        self._part_modifiers = []

    @property
    def rel_to_root(self):
        """
        Boolean value, if True then the output url will be relative
        to the documentation root. If False the output URL will be
        relative to the page.
        """
        return self._rel_to_root

    def add_modifier(self, modifier):
        """
        Add a modifier to the URLRules object.
        The modifier should be a function.
        The input to the function will be the output url before
          modification (it will be relative to root or page depending
          on the value of URLRules.rel_to_root.
        The output should be the modified output
        The output_url will be put through all modifiers sequentially.
        """
        if callable(modifier):
            self._modifiers.append(modifier)
        else:
            raise TypeError("modifier must be a callable function")

    def add_part_modifier(self, modifier):
        """
        This behaves the same as URLRules.add_modifier except that
        the modifier function is only used by part links. These
        modifiers are run after all of the other modifiers.
        """
        if callable(modifier):
            self._part_modifiers.append(modifier)
        else:
            raise TypeError("modifier must be a callable function")

    def create_translator(self, page, part_translator=False, replace_links=None):
        """
        Creates a URLTranslator object based on the rules in this class.
        """
        if page is None:
            page = 'index.md'
        if part_translator:
            mods = self._modifiers + self._part_modifiers
        else:
            mods = self._modifiers
        return URLTranslator(self.rel_to_root, page, mods, replace_links)


class URLTranslator:
    """
    Translates the url in the BuildUp into the final output
    url. This class should only be made by URLRules "create_translator".
    """

    def __init__(self, rel_to_root, page, modifiers, replace_links):
        self._rel_to_root = rel_to_root
        self._page = page
        self._modifiers = modifiers
        self._replace_links = replace_links

    @property
    def directory(self):
        """
        The directory to be used if link is not relative to
        the root directory
        """
        return posixpath.dirname(self._page)

    def translate(self, link):
        """
        This takes in a link object and uses the modifier rules
        to create an output url
        """
        return self.simple_translate(link.link_rel_to_root)

    def simple_translate(self, url):
        """
        This takes in a simple url relative to the root and uses the
        modifier rules to create an output url
        """
        url = as_posix(url, warn=True)

        if (self._replace_links is not None) and (url in self._replace_links):
            url = self._replace_links[url]
        if url.startswith('..'):
            _LOGGER.warning('Linking to file outside build directory "%s" '
                            'File has been moved to "orphaned_files" directory',
                            url)
            url = "orphaned_files/" + posixpath.basename(url)
        if url != "" and not self._rel_to_root:
            url = posixpath.relpath(url, self.directory)
        page_url, anchor = split_anchor(url)
        for mod in self._modifiers:
            page_url, anchor = mod(page_url, anchor)
        if anchor == "":
            return page_url
        return '#'.join([page_url, anchor])
