"""
This module constains the flask server for viewing the documentation and for live editing.
The server is lunched with `gitbuilding serve` and runs on port 6178.
"""

import posixpath
import logging
from copy import deepcopy
from uuid import uuid4 as uuid
import socket
import flask
from flask import request, jsonify
import requests
import waitress
from gitbuilding import utilities
from gitbuilding import example
from gitbuilding.buildup import Documentation, read_directory, FileInfo
from gitbuilding.buildup.page import Page
from gitbuilding.buildup.files import is_filepath_safe
from gitbuilding.buildup.utilities import as_posix
from gitbuilding import render
from gitbuilding.previewers import gitbuilding_previewers
from gitbuilding.config import load_config_from_file
from gitbuilding.native_file_operations import (GBPATH,
                                                TMPDIR,
                                                is_local_file,
                                                make_dir_if_needed,
                                                as_native_path,
                                                write_local_file,
                                                create_zip,
                                                delete_local_file,
                                                copy_local_files)

_LOGGER = logging.getLogger('BuildUp.GitBuilding')

# This module is only the server. It makes more sense for all flask calls
# to be methods. As such disabling no-self-use
# pylint: disable=no-self-use

class GBWebPath():
    """
    GBWebPath is a class that parses paths from the server and can return either the
    corresponding local path or the correct special path.
    """

    def __init__(self, rawpath, doc):
        self._web_path = rawpath
        self._gb_path = None
        self._gb_file = None
        self._missing_page = False
        self._homepage = False

        self._process_path(rawpath, doc)

    def _process_path(self, rawpath, doc):
        """
        Check for special cases then process path as normal
        """
        if rawpath is None:
            self._homepage = True
            self._web_path = 'index.html'
            self._gb_path = doc.config.landing_page
            if self._gb_path is not None:
                self._gb_file = doc.get_file(self._gb_path)
        elif rawpath == "missing":
            self._missing_page = True
        else:
            self._process_standard_path(rawpath, doc)

    def _process_standard_path(self, rawpath, doc):
        base_path, ext = posixpath.splitext(rawpath)
        if ext == '':
            self._web_path += '.html'
            ext = '.html'

        if ext.lower() == '.html':
            self._gb_path = base_path + '.md'
        else:
            self._gb_path = rawpath

        self._gb_file = doc.get_file(self._gb_path)


    @property
    def is_homepage(self):
        """
        Return true if the link is to the homepage
        """
        return self._homepage

    @property
    def is_empty_homepage(self):
        """
        Return true if the link is to the homepage but no homepage is set
        """
        return self._homepage and self._gb_path is None

    @property
    def is_missing_page(self):
        """
        Return true if the link the GitBuilding special page "missing"
        """
        return self._missing_page

    @property
    def is_markdown(self):
        """
        Return true if the GitBuilding expects this file to be markdown. Returns true
        even if the file cannot be found
        """
        return self._gb_path.endswith('.md')

    @property
    def web_path(self):
        """
        Return the html path
        """
        return self._web_path

    @property
    def gb_path(self):
        """
        Return the path to the corresponding gitbuilding file.
        """
        return self._gb_path

    @property
    def gb_path_deduplicated(self):
        """
        Return the path to the corresponding gitbuilding file. If the file is a
        duplicate created by multiple paths through the documentation this will
        return the orignal
        """
        if self._gb_file is None:
            return self._gb_path
        if self._gb_file.duplicate_of is None:
            return self._gb_path
        return self._gb_file.duplicate_of

    @property
    def gb_file(self):
        """
        Return the gitbuilding file object for this path
        """
        return self._gb_file

    @property
    def os_path(self):
        """
        Return the git building file path in the native os format
        """
        return as_native_path(self._gb_path)

class GBServer(flask.Flask):
    """
    GBServer is the GitBuilding server it is a child class of flask.Flask. It can be
    used to provide a preview of the documentation and to serve the live editor.
    """

    def __init__(self, conf, handler):

        rules = render.URLRulesHTML()
        self._handler = handler
        log_length = self._handler.log_length
        configuration = load_config_from_file(conf)
        configuration.remove_landing_title = True
        self._license_file = utilities.handle_licenses(configuration)
        self.doc = Documentation(configuration, rules, gitbuilding_previewers())
        file_list = read_directory('.', exclude_list=configuration.exclude)
        if self._license_file is not None:
            file_list.append(self._license_file)
        self.doc.buildall(file_list)
        self._read_config()
        self._global_log = self._handler.log_from(log_length)

        # Two render objects, one for static one for live
        self.renderer = render.GBRenderer(self._config, rules, static=False)
        self.renderer.set_warning_count(self._global_log)
        # The live renderer shows the static rendering as static=False
        # is used show the header buttons.
        self.live_renderer = render.GBRenderer(deepcopy(self._config), rules)
        self._unsaved_dropped_files = DroppedFiles()
        super().__init__(__name__)

        # Define URL rules!
        self.add_url_rule("/", "render", self._render_page)
        self.add_url_rule("/-/render_markdown",
                          "live_render",
                          self._live_render,
                          methods=["POST"])
        self.add_url_rule("/<path:rawsubpath>", "render", self._render_page)
        self.add_url_rule("/-/<path:rawsubpath>", "undef_special", self._undefined_special_page)
        self.add_url_rule("/assets/<path:rawsubpath>", "assets", self._return_assets)
        self.add_url_rule("/-/new-page/", "new_page", self._new_page)
        self.add_url_rule("/-/new-template/<path:template>", "new_template", self._new_template)
        self.add_url_rule("/-/create-from-template/<path:template>",
                          "create_from_template",
                          self._create_from_template)
        self.add_url_rule("/-/warnings", "warning_page", self._warning_page)
        self.add_url_rule("/-/editor/", "editor", self._edit_page)
        self.add_url_rule("/-/editor/save", "save", self._save_edit, methods=["POST"])
        self.add_url_rule("/-/editor/raw", "raw", self._raw_md)
        self.add_url_rule("/-/create-homepage/", "create_homepage", self._create_homepage)
        self.add_url_rule("/-/contents-page", "contents_page", self._contents_page)

        self.add_url_rule("/<path:rawsubpath>/-/editor/", "editor", self._edit_page)
        self.add_url_rule("/<path:rawsubpath>/-/editor/raw", "raw", self._raw_md)
        self.add_url_rule("/<path:rawsubpath>/-/editor/save",
                          "save",
                          self._save_edit,
                          methods=["POST"])

        self.add_url_rule("/<path:rawsubpath>/-/editor/dropped-file",
                          "droppedfile",
                          self._dropped_file,
                          methods=["POST"])

        self.add_url_rule("/-/editor/dropped-file",
                          "droppedfile",
                          self._dropped_file,
                          methods=["POST"])

    def _read_config(self):
        """
        Reads the project data generated when converting BuildUp to markdown
        """
        self._config = self.doc.config

    def _get_docpage(self, path):
        """
        Gets a Page object from the Documentation object
        """
        if path.gb_path_deduplicated in self.doc.pages:
            return self.doc.get_page_by_path(path.gb_path_deduplicated)

        file_obj = FileInfo(path.gb_path, dynamic_content=True, content='# Empty page\n\nEdit me')
        return Page(file_obj, self.doc)

    def _raw_md(self, rawsubpath=None):
        """
        Get the raw markdown for pages in the documentation
        Returns this in JSON
        """

        path = GBWebPath(rawsubpath, self.doc)

        page = self._get_docpage(path)
        md = ""
        if page is not None:
            md = page.get_raw()

        duplicated_by = []
        if path.gb_path_deduplicated in self.doc.page_order.duplicates:
            duplicates = self.doc.page_order.duplicates[path.gb_path_deduplicated]
            for duplicate in duplicates:
                duplicate_path = GBWebPath(duplicate, self.doc)
                duplicated_by.append(self._get_docpage(duplicate_path).title)

        # return the markdown
        if rawsubpath is None:
            return jsonify({"md": md})
        return jsonify({"md": md, "page": rawsubpath, "duplicated_by": duplicated_by})


    def _save_edit(self, rawsubpath=None):
        """
        Saves the edits from the live editor and full rebuilds the documentation
        """

        path = GBWebPath(rawsubpath, self.doc)

        #Get the JSON from the request
        content = request.get_json()

        if content["md"] is None:
            return jsonify({"saved": False})

        self._save_uploaded_files(content)
        saved = self._save_page(path, content["md"])
        if saved:
            self._rebuild_docs()
        return jsonify({"saved": saved})

    def _save_uploaded_files(self, content):
        """
        Save each uploaded file listed in the json request if they are used in the markdown
        """
        for uploaded_file in content["uploadedFiles"]:
            # Check if file is still there. It may already have been removed
            # if multiple copies of the same file were dropped.
            if self._unsaved_dropped_files.contains(uploaded_file):
                if uploaded_file in content["md"]:
                    try:
                        make_dir_if_needed(uploaded_file, isfile=True)
                        copy_local_files(self._unsaved_dropped_files.get(uploaded_file),
                                         uploaded_file)
                    except FileNotFoundError:
                        _LOGGER.warning("Uploaded file %s may have been deleted",
                                        uploaded_file)
                    #Only remove if copied as multiple editors could have added same file
                    self._unsaved_dropped_files.remove(uploaded_file)

    def _save_page(self, path, md):

        if path.gb_path is None:
            return False

        save_path = path.gb_path_deduplicated
        make_dir_if_needed(save_path, isfile=True)
        try:
            write_local_file(save_path, md)
            return True
        except IOError:
            return False

    def _create_homepage(self):
        md = "# Project title\nSome text for this page"
        self._save_page(GBWebPath('index.md', self.doc), md)
        self._rebuild_docs()
        return flask.redirect('/-/editor/')

    def _create_from_template(self, template):
        input_data = request.args.to_dict()
        if 'pagename' not in input_data:
            message = flask.escape('No page name given')
            return flask.redirect(f'/-/new-template/{template}?msg={message}')
        pagename = input_data['pagename']
        if not is_filepath_safe(pagename, allow_external=False):
            message = flask.escape(f'Page name "{pagename}" contains unsafe characters')
            return flask.redirect(f'/-/new-template/{template}?msg={message}')

        path = GBWebPath(pagename, self.doc)

        if path.gb_file is not None:
            message = flask.escape(f'Page "{pagename}" already exists')
            return flask.redirect(f'/-/new-template/{template}?msg={message}')

        if template == 'empty':
            md = ""
        elif template == 'stepbystep':
            md = example.testpage("Example instructions")
        else:
            message = flask.escape(f'Unknown template specified: "{template}"')
            return flask.redirect(f'/-/new-page?msg={message}')

        self._save_page(path, md)
        self._rebuild_docs()
        return flask.redirect(f'/{path.web_path}/-/editor/')

    def _contents_page(self):
        return self.renderer.contents_page(self.doc.output_files)

    def _warning_page(self):
        return self.renderer.warning_page(self._global_log)

    def _rebuild_docs(self):
        log_length = self._handler.log_length
        file_list = read_directory('.', exclude_list=self.doc.config.exclude)
        if self._license_file is not None:
            file_list.append(self._license_file)
        self.doc.buildall(file_list)
        self._read_config()
        self.renderer.config = self._config
        self.renderer.populate_vars()
        self._global_log = self._handler.log_from(log_length)
        self.renderer.set_warning_count(self._global_log)

    def _dropped_file(self, rawsubpath=None):
        """
        This gets run if a file gets dragged and dropped into the editor
        """
        files = request.files
        if rawsubpath is None:
            folder_depth = 0
        else:
            path = GBWebPath(rawsubpath, self.doc)
            folder_depth = len(path.gb_path_deduplicated.split('/')) - 1
        out_filenames = []
        md_line = ''
        # loop through all files and save images
        for file_id in files:
            file_obj = files[file_id]
            if file_obj.mimetype.startswith("image"):
                filename, md = self._process_dropped_file(file_obj, "images", folder_depth)
                out_filenames.append(filename)
                md_line += md
            elif self.doc.previewer_for_uri(file_obj.filename) is not None:
                save_dir = self.doc.previewer_for_uri(file_obj.filename).dir_for_dropped_files
                filename, md = self._process_dropped_file(file_obj, save_dir, folder_depth)
                out_filenames.append(filename)
                md_line += md
            else:
                _LOGGER.warning("Cannot upload file of mimetype: %s", file_obj.mimetype)

        if len(out_filenames) > 0:
            return jsonify({"received": True,
                            "filenames": out_filenames,
                            "md_line": md_line})
        return flask.abort(405)

    def _process_dropped_file(self, file_obj, save_dir, folder_depth):

        filename = as_posix(file_obj.filename.replace(" ", ""))

        #This is going into the markdown so we always use unix paths.
        file_path = f"{save_dir}/{filename}"
        i = 0
        while is_local_file(file_path):
            if i == 0:
                path_no_ext, ext = posixpath.splitext(file_path)
            i += 1
            file_path = f'{path_no_ext}{i:03d}{ext}'

        _, ext = posixpath.splitext(filename)
        temp_path = TMPDIR + "/" + str(uuid()) + ext
        file_obj.save(temp_path)
        self._unsaved_dropped_files.add_file(file_path, temp_path)
        md_file_path = '../'*folder_depth + file_path
        md = f'![]({md_file_path})\n'
        return file_path, md


    def _undefined_special_page(self, rawsubpath=None):
        # pylint: disable=unused-argument
        return flask.abort(404)

    def _live_render(self):
        """
        Runs the live renderer and returns the html as well as warnings
        in JSON format
        """

        content = request.get_json()
        if content["md"] is None:
            return jsonify({"html": "", "log": "", "number": 0})

        log_length = self._handler.log_length
        overloaded_path = None
        if not "page" in content: # Live render landing page
            if self.doc.config.landing_page is not None:
                page = self.doc.landing_page
                overloaded_path = '-/editor/index'
                processed_text = page.rebuild(content["md"], overloaded_path)
                title = page.title
                self.live_renderer.config.title = title
                self.live_renderer.populate_vars()
        else:
            path = GBWebPath(content["page"], self.doc)
            page = self._get_docpage(path)
            overloaded_path = path.web_path+'/-/editor/index'
            if page is None:
                return jsonify({"html": "", "log": "", "number": 0})
            processed_text = page.rebuild(content["md"], overloaded_path)

        html = self.live_renderer.render_md(processed_text,
                                            link=overloaded_path,
                                            template=self.live_renderer.IFRAME,
                                            nav=False)
        log = self._handler.log_from(log_length)

        return jsonify({"html": html,
                        "log": render.format_warnings(log),
                        "number": len(log)})

    def _new_page(self):
        """
        Brings up the new page creation page
        """
        input_data = request.args.to_dict()
        if 'msg' in input_data:
            msg = input_data['msg']
        else:
            msg = None
        html = self.renderer.new_page(error_message=msg)
        return html

    def _new_template(self, template):
        """
        Brings up the form to complete the new page creation
        """
        input_data = request.args.to_dict()
        if 'msg' in input_data:
            msg = input_data['msg']
        else:
            msg = None
        html = self.renderer.new_page_form(template, error_message=msg)
        return html

    def _edit_page(self, rawsubpath=None):
        """
        Starts the live editor for a particular page
        """
        path = GBWebPath(rawsubpath, self.doc)
        if path.is_markdown:
            self.live_renderer.config = deepcopy(self._config)
            self.live_renderer.populate_vars()

            page = GBPATH + "/static/live-editor/index.html"
            return flask.send_file(as_native_path(page, absolute=True))

        html = self.renderer.render("<h1>Sorry. Cannot edit this file!</h1>",
                                    link=rawsubpath)
        return html

    def _render_page(self, rawsubpath=None):
        """
        Renders the static version of a page
        """
        path = GBWebPath(rawsubpath, self.doc)
        if path.is_empty_homepage:
            return self.renderer.empty_homepage()
        if path.is_missing_page:
            return self.renderer.missing_page()
        if path.gb_file is None:
            # If the file requested is not chached in the documentation
            # try other means to render it
            return self._render_missing_file(path)

        if path.is_markdown and path.gb_file.dynamic_content:
            return self._render_markdown_page(path)

        return self._send_file_obj(path.gb_file)

    def _render_markdown_page(self, path):
        editorbutton = False
        if path.gb_path_deduplicated in self.doc.pages:
            editorbutton = True
        if path.is_homepage:
            link = None
        else:
            link = path.web_path
        return self.renderer.render_md(path.gb_file.content,
                                       link,
                                       meta_info=path.gb_file.meta_info,
                                       editorbutton=editorbutton)

    def _render_missing_file(self, path):
        """
        Render a file that is not found in the GitBuilding documentation object. This could be
        a recently dragged and dropped file, or a file that is in
        the gitbuilding directory but was not processed during the last full build
        """

        if path.is_markdown:

            # Else give option to create the page.
            return self.renderer.render_md("# Page not found\n Do you want to "
                                           f"[create it](/{path.web_path}/-/editor)?",
                                           path.web_path,
                                           editorbutton=True)

        # For missing files that are not markdown check the temporary
        # files that were drag and dropped.
        temp_file = self._unsaved_dropped_files.get(path.web_path)
        if temp_file is not None:
            return flask.send_file(as_native_path(temp_file, absolute=True))

        # If file still missing it may be in the input directory this should only
        # happen when live editing a file
        file_list = read_directory('.', exclude_list=self._config.exclude)
        if path.os_path in file_list:
            file_obj = file_list[file_list.index(path.os_path)]
            return self._send_file_obj(file_obj)

        return self._404_or_missing_image(path.web_path)

    def _send_file_obj(self, file_obj):
        if file_obj.dynamic_content:
            return self._send_dynamic_file_obj(file_obj)
        return self._send_static_file_obj(file_obj)

    def _send_static_file_obj(self, file_obj):
        path = file_obj.location_on_disk
        if is_local_file(path):
            return flask.send_file(as_native_path(path, absolute=True))
        return self._404_or_missing_image(file_obj.path)

    def _send_dynamic_file_obj(self, file_obj):
        file_dir = TMPDIR + "/.gbserver"
        make_dir_if_needed(file_dir)
        filename = file_dir + "/" + posixpath.basename(file_obj.path)
        if file_obj.files_to_zip is not None:
            create_zip(filename, file_obj.files_to_zip)
        else:
            write_local_file(filename,
                             file_obj.content,
                             ensure_relative=False,
                             allow_external=True)
        return flask.send_file(as_native_path(filename, absolute=True))

    def _404_or_missing_image(self, web_path):
        if web_path.lower().endswith((".jpg", ".jpeg", ".png", ".gif", '.svg',
                                     ".tif", ".tiff", '.webp')):
            image = GBPATH + "/static/local-server/Missing_image.png"
            return flask.send_file(as_native_path(image, absolute=True))
        return flask.abort(404)

    def _return_assets(self, rawsubpath):
        """
        returns file from the assets directory
        """
        page = "assets/" + rawsubpath
        if is_local_file(page):
            return flask.send_file(as_native_path(page, absolute=True))

        return flask.abort(404)

    def run(self, host="localhost", port=6178, use_waitress=True): # pylint: disable=arguments-differ
        """
        Starts the flask server
        """
        try:
            # Check the server isn't already running (only needed on Windows)
            sock = socket.create_connection((host, port), timeout=0.5)
            sock.close()
            # If we have made it past this, there is a server running - so we
            # should fail
            raise ServerAlreadyRunningError(f'A server is already running on "{host}"'
                                            f' port {port}.')
        except socket.timeout:
            pass  # If we couldn't connect, ignore the error
        except ConnectionError:
            pass # If we couldn't connect, ignore the error

        if use_waitress:
            print('GitBuilding server running on http://localhost:6178/ (Press CTRL+C to quit)')
            waitress.serve(self, host=host, port=port)
        else:
            super().run(host, port)

class ServerAlreadyRunningError(Exception):
    """
    Custom exception for if the GitBuilding server is already running.
    """

class DevServer(GBServer):
    """
    Child class of GBServer, this server allows hot-reloading of live-editor for
    development.
    """

    def __init__(self, conf, handler):

        super().__init__(conf, handler)

        self.add_url_rule("/static/live-editor/<path:subpath>",
                          "dev_editor_static",
                          self._dev_editor_static)
        self.add_url_rule("/static/<path:subpath>",
                          "dev_other_static",
                          self._dev_other_static)
        self.add_url_rule("/sockjs-node/<path:subpath>",
                          "dev_editor_sockjs",
                          self._dev_editor_sockjs)

        self.add_url_rule("/__webpack_dev_server__/<path:subpath>",
                          "dev_editor_webpack",
                          self._dev_editor_webpack)

    def _edit_page(self, rawsubpath=None):
        """
        Starts the live editor for a particular page
        """
        path = GBWebPath(rawsubpath, self.doc)
        if path.is_markdown:
            self.live_renderer.config = deepcopy(self._config)
            self.live_renderer.populate_vars()

            url = "http://localhost:8080/static/live-editor/"
            try:
                req = requests.get(url)
            except requests.exceptions.RequestException:
                msg = (f"ERROR: Could not connect to live-editor dev server"
                       f" on '{url}', did you forget to start it?")
                return flask.abort(flask.Response(msg, status=500))
            return req.text

        html = self.renderer.render("<h1>Sorry. Cannot edit this file!</h1>",
                                    link=rawsubpath)
        return html


    def _dev_editor_static(self, subpath):
        url = "http://localhost:8080/static/live-editor/" + subpath
        try:
            req = requests.request(flask.request.method, url)
        except requests.exceptions.RequestException:
            msg = (f"ERROR: Could not connect to live-editor dev server for '{url}',"
                   " did you forget to start it?")
            return flask.abort(flask.Response(msg, status=500))
        return req.text

    def _dev_editor_sockjs(self, subpath):
        url = ("http://localhost:8080/sockjs-node/"
               + subpath
               + flask.request.query_string.decode())
        try:
            req = requests.request(flask.request.method, url)
        except requests.exceptions.RequestException:
            msg = (f"ERROR: Could not connect to live-editor dev server for '{url}',"
                   " did you forget to start it?")
            return flask.abort(flask.Response(msg, status=500))
        return req.text

    def _dev_editor_webpack(self, subpath):
        url = ("http://localhost:8080/__webpack_dev_server__/"
               + subpath
               + flask.request.query_string.decode())
        try:
            req = requests.request(flask.request.method, url)
        except requests.exceptions.RequestException:
            msg = (f"ERROR: Could not connect to live-editor dev server for '{url}',"
                   " did you forget to start it?")
            return flask.abort(flask.Response(msg, status=500))
        return req.text

    def _dev_other_static(self, subpath):
        return flask.send_from_directory("static", subpath)

class DroppedFiles:
    """
    Pretty simple class for handling the files dropped into the editor. This
    could be handled with a list of dictionaries but the syntax for checking
    and finding the correct file gets really ugly.
    """

    def __init__(self):
        self._files = []

    def add_file(self, output_file, temp_file):
        """
        Add a dropped file to be tracked. Inputs are the filename in the
        output, and the temporary filename
        """
        if not self.contains(output_file):
            self._files.append({'output_path':output_file,
                                'temp_path':temp_file})

    @property
    def _out_paths(self):
        return [fdict['output_path'] for fdict in self._files]

    def get(self, filename):
        """
        Get the temp file for location for `filename`. Returns None if the
        filename does not exist
        """

        out_paths = self._out_paths
        if filename in out_paths:
            return self._files[out_paths.index(filename)]['temp_path']
        return None

    def contains(self, filename):
        """
        Returns true if `filename` is listed as an output filename.
        """
        return self.get(filename) is not None

    def remove(self, filename):
        """
        Removes the record for the dropped file and deletes the temporary file
        from disk
        """
        out_paths = self._out_paths
        if filename in out_paths:
            ind = out_paths.index(filename)
            temp_file = self._files[ind]['temp_path']
            delete_local_file(temp_file)
            self._files.pop(ind)
            return True
        return False
