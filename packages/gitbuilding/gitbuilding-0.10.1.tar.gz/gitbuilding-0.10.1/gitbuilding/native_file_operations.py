"""
This handles native file operations such as checking if files exists
on disk and writing to them. It is not much more than a simple wrapper
around some os.* functions.

The purpose of this module is to ensure that
all paths in other modules can be trated as posix paths. This is important
otherwise you need to track whether a is in posix style for web url use
or is in native style.
"""

import os
import shutil
import codecs
import re
import zipfile
from tempfile import gettempdir
from gitbuilding.buildup.utilities import as_posix

GBPATH = os.path.dirname(__file__)
TMPDIR = gettempdir()

def _localise(pos_path):
    # Note on Windows os.path.normpath converts posix path seperators to windows ones
    # On Linux os.path.normpath (nor posixpath.normpath) converts from winddows to posix
    return os.path.normpath(pos_path)

def as_native_path(pos_path, absolute=False):
    """
    Returns the input posix style path as a os native path. Note that
    if you enter a Windows style path on Linux this will not change
    to posix.
    """
    if absolute:
        return os.path.abspath(_localise(pos_path))
    return _localise(pos_path)

def exists_on_disk(pos_path):
    """
    Return whether path exists on disk (can be file or dir)
    """
    return os.path.exists(_localise(pos_path))

def is_local_file(pos_path):
    """
    Return whether local file exists and is a file
    """
    return os.path.isfile(_localise(pos_path))

def directory_is_empty(pos_path):
    """
    Return if directory is empty
    """
    return os.listdir(_localise(pos_path)) == []

def make_local_dir(pos_path, remove_existing=False):
    """
    Make a local directory. See also make_dir_if_needed
    """
    path = _localise(pos_path)
    if remove_existing:
        if os.path.exists(path):
            shutil.rmtree(path)
    os.mkdir(path)

def make_dir_if_needed(pos_path, isfile=False):
    """Makes the directory if it doesn't exist.
    Handles empty strings for directory"""
    path = _localise(pos_path)
    if isfile:
        directory = os.path.dirname(path)
    else:
        directory = path
    if not directory == "":
        if not os.path.exists(directory):
            os.makedirs(directory)

def write_local_file(pos_path, contents, ensure_relative=True, allow_external=False):
    """
    Write a file to the local hard drive. Inputs are a posix path (that will be converted
    to a local path)
    """
    if ensure_relative:
        if os.path.isabs(pos_path):
            raise RuntimeError("Attempting to write to an absolute path. "
                               "This should not be possible")

    path = _localise(pos_path)
    if not allow_external:
        if path.startswith('..'):
            raise RuntimeError("Attempting to write to files outside documentation "
                                "directory. Aborting.")

    with codecs.open(path, "w", encoding='utf-8') as file_obj:
        file_obj.write(contents)

def read_local_file(pos_path):
    """
    Return the contents of a local file
    """
    with codecs.open(_localise(pos_path), mode="r", encoding="utf-8") as file_obj:
        content = file_obj.read()
    return content

def delete_local_file(pos_path):
    """
    Delete a local file
    """
    os.remove(_localise(pos_path))

def delete_local_dir(pos_path):
    """
    Delete a local directory
    """
    shutil.rmtree(_localise(pos_path))

def copy_local_files(pos_path1, pos_path2):
    """
    Copy a local file to a new path
    """
    path1 = _localise(pos_path1)
    path2 = _localise(pos_path2)
    shutil.copy(path1, path2)

def copy_local_directory(pos_path1, pos_path2, ignore_dirs=None):
    """
    Copy a local directory into another directory. Optionally can ignore
    given directories
    """
    path1 = _localise(pos_path1)
    path2 = _localise(pos_path2)
    path_rel_to = os.path.split(path1)[0]
    if ignore_dirs is None:
        ignore_dirs = []

    for root, _, files in os.walk(path1):
        for filename in files:
            ignored = False
            for dir_name in ignore_dirs:
                if dir_name in root:
                    ignored = True

            if not ignored:
                filepath = os.path.join(root, filename)
                relative_filepath = os.path.relpath(filepath, path_rel_to)
                out_file = os.path.join(path2, relative_filepath)
                make_dir_if_needed(out_file, isfile=True)
                shutil.copy(filepath, out_file)

def get_matches_from_dir(directory, regex):
    """
    Return all files within the given directory that match a rexex pattern
    """
    matches = []
    directory = _localise(directory)
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            match = re.match(regex, filename)
            if match is not None:
                matches.append(as_posix(filepath))
    return matches


def is_valid_directory_name(path):
    """
    Check if directory name is a valid single directory
    """
    match = re.match(r"^[a-zA-Z0-9 _\-]+$", path)
    return match is not None

def create_zip(zipfilename, files_to_zip):
    """
    Create a zip archive in the local file system
    """
    files_to_zip = [_localise(filename) for filename in files_to_zip]
    zipfilename = _localise(zipfilename)
    with zipfile.ZipFile(zipfilename, 'w') as zipfile_obj:
        for filename in files_to_zip:
            if os.path.isfile(filename):
                zipfile_obj.write(filename)

def clean_documentation_dir():
    """
    Removes the files built by gitbuilding
    """
    dirs_to_remove = ['_build', '_site', '_pdf']
    for directory in dirs_to_remove:
        if exists_on_disk(directory):
            delete_local_dir(directory)
