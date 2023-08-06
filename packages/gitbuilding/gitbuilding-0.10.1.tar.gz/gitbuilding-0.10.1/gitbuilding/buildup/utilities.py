"""
A collection of generally useful functions.
"""

import logging
from fnmatch import fnmatch
from copy import copy
from pathlib import PureWindowsPath
import posixpath

import regex as re

_LOGGER = logging.getLogger('BuildUp')

def as_posix(path, warn=False):
    """
    Returns the input path as a posix path.

    By posix path we mean something that will work with python "posixpath" library.
    This includes URLs with internal links. This is done so that all file paths within
    buildup are the same on any OS to reduce the number of file path bugs when changing
    systems.
    """

    if path == "":
        return path
    if warn:
        pos_path = as_posix(path)
        if path not in [pos_path, './'+pos_path]:
            _LOGGER.warning('"%s" is not a normalised posixpath. This may cause '
                            'unexpected results. Using "%s"',
                            path, pos_path)
        return pos_path
    return posixpath.normpath(PureWindowsPath(path).as_posix())

def strip_internal_links(path):
    """
    Remove internal links from a path. i.e. Links ending with #ID
    For example:
    Input: page/subpage.md#section
    Output: page/subpage.md
    """
    return path.split('#')[0]

def clean_id(id_in):
    """
    Input a string and output is a string that can be used an an ID in HTML
    """
    id_out = id_in.replace(' ', '-')
    id_out = id_out.lower()
    return re.sub(r'[^a-z0-9\_\-]', '', id_out)

def nav_order_from_nav_pagelist(nav_pagelist):
    """
    Uses the nav_pagelist, which is a list of tuples to create a page ordering for
    the navigation. The result is a list of file paths
    """

    nav_order = []
    # Page ordering are the pages (first element for each item in the nav_pagelist)
    # and the BOM pages for these pages (third element in the tuple)
    for page_tuple in nav_pagelist:
        nav_order.append(page_tuple[0])
        if page_tuple[2] is not None:
            nav_order.append(page_tuple[2])
    return nav_order

def contains_wildcards(filepath):
    "Return whether the filepath contains * ? or [] wildcards"
    return re.search(r'(?:\*|\?|\[.*\])', filepath) is not None

def match_files(pattern, files):
    "Return the files from a list of FileInfo objects that match the input glob pattern"
    matches = []
    for file_obj in files:
        if fnmatch(file_obj.path, pattern):
            matches.append(copy(file_obj))
    return matches

def raise_validation_error_as_warning(err):
    """
    Raise a validation error as a BuildUp logger warning after tidying up
    the message.
    """
    validation_issue = re.sub(r"""[\'\"\[\]\{\}\.]""", "", str(err))
    _LOGGER.warning('Validating link data failed. %s', validation_issue)
