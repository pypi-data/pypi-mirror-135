'''
A number of miscellaneous functions
'''


import datetime
import logging
from gitbuilding.buildup import FileInfo
from gitbuilding.native_file_operations import GBPATH, is_local_file, read_local_file

_LOGGER = logging.getLogger('BuildUp.GitBuilding')
_LICENSE_DIR = GBPATH+"/licenses"

def handle_licenses(configuration):
    """
    Modifies the configuration to auto include licenses by SPDX. If an extra file is needed then
    a FileInfo object is returned, else None is returned
    """

    if configuration.license_file is not None:
        #A licence file was explicitly specified in the configuration
        if configuration.license is None:
            _LOGGER.warning('License file set in configuration but no license name set.')
            configuration.license = 'Unknown license'
        configuration.force_output.append(configuration.license_file)
        return None
    #No licence file specified in configuration
    if configuration.license is None:
        #if no license or license_file is set just leave as is
        return None
    # Licence file is not specified by a license name is. Try to get the license text by
    # SPDX identifier:
    license_text = _get_license_text(configuration)
    if license_text is None:
        _LOGGER.warning('License %s set configuration. Could not match to licence text.',
                        configuration.license)
        return None
    configuration.license_file = 'license.md'
    configuration.force_output.append('license.md')
    return FileInfo('license.md', dynamic_content=True, content=license_text)

def _get_license_text(configuration):

    # note all license files are in the format '<SPDX_IDN>.txt' where
    # <SPDX_IDN> is the SPDX license identifier

    licence_file =  _LICENSE_DIR+ "/" + configuration.license+".txt"
    if not is_local_file(licence_file):
        return None

    license_text = read_local_file(licence_file)

    this_year = str(datetime.datetime.now().year)
    authors = author_list(configuration, default="Copyright Holders")

    license_text = license_text.replace("[year]", this_year)
    license_text = license_text.replace("[fullname]", authors)
    license_text = f"# License\n```\n{license_text}\n```"
    return license_text

def author_list(configuration, default=None):
    """
    This function returns the list of authors as a string.
    """
    authors = configuration.authors
    if len(authors) == 0:
        return default
    if len(authors) == 1:
        return authors[0]
    if len(authors) == 2:
        return authors[0] + ' and ' + authors[1]
    #if more than two authors make a list
    text = ""
    for i, author in enumerate(authors):
        if i == 0:
            pass
        elif i == len(configuration.authors) - 1:
            text += ", and "
        else:
            text += ", "
        text += f"{author}"
    return text
