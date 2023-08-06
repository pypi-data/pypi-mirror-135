"""
This contains GBRenderer, the class responsible for rendering processed markdown into HTML
It also contains the URLRules GitBuilding uses for HTML and some other helper functions.
"""

import posixpath
import datetime
from copy import copy, deepcopy
import logging
import regex as re
from markdown import markdown
from jinja2 import Environment, FileSystemLoader
from markdown_katex.wrapper import KatexError
from gitbuilding.buildup import URLRules
from gitbuilding import utilities
from gitbuilding.buildup.buildup import IMAGE_REGEX
from gitbuilding.native_file_operations import (GBPATH,
                                                exists_on_disk,
                                                get_matches_from_dir,
                                                read_local_file)

_LOGGER = logging.getLogger('BuildUp.GitBuilding')

class URLRulesHTML(URLRules):
    """
    The BuildUp URLRules used in GitBuilding for both the server and the static HTML.
    This is a child-class of buildup.URLRules with functions to strip off '.md' file
    extensions, rerouted stl links (for parts only) to markdown pages, and to replace
    empty links with "missing".
    """
    def __init__(self, rel_to_root=False, no_server=False):

        super().__init__(rel_to_root=rel_to_root)
        def fix_missing(url, anchor):
            if url == "" and  anchor == "":
                return "missing", anchor
            return url, anchor

        def stl_to_page(url, anchor):
            if url.endswith('.stl'):
                return url[:-4]+'.html', anchor
            return url, anchor

        def md_to_page(url, anchor):
            if url.endswith('.md'):
                return url[:-3]+'.html', anchor
            return url, anchor

        self.add_modifier(fix_missing)
        self.add_modifier(md_to_page)
        if not no_server:
            self.add_part_modifier(stl_to_page)

class URLRulesPDF(URLRules):
    """
    The BuildUp URLRules used in GitBuilding PDF generation (via single pageHTML).
    This is a child-class of buildup.URLRules with functions to strip off '.md' file
    """
    def __init__(self, rel_to_root=True):

        super().__init__(rel_to_root=rel_to_root)

        def md_to_inside_page(url, anchor):
            if url.endswith('.md'):
                url = url[:-3]
                url = url.replace('/', '__')
                if anchor != '':
                    anchor = url + '---' + anchor
                else:
                    anchor = url
                url = ''
            return url, anchor

        def jpg_to_png(url, anchor):
            if url.lower().endswith((".jpg", ".jpeg")):
                url = '.'.join(url.split('.')[:-1])+'.png'
            return url, anchor

        self.add_modifier(md_to_inside_page)
        self.add_modifier(jpg_to_png)


def _is_active_nav_item(nav_item, link):
    """
    Checks if the item in the navigation dictionary or any of the
     terms in the sub-navigation are the active page
    """
    if nav_item["link"] == link:
        return True
    if "subnavigation" in nav_item:
        for sub_nav_item in nav_item["subnavigation"]:
            if _is_active_nav_item(sub_nav_item, link):
                return True
    return False

def format_warnings(warnings, show_page=False):
    """
    Returns warnings for the live renderer to display
    """
    output = ""
    for warning in warnings:
        if warning["fussy"]:
            cssclass = "fussywarning"
            warntype = "FussyWarning"
        else:
            cssclass = "warning"
            warntype = "Warning"

        if show_page:
            if isinstance(warning["active_page"], str) and warning["active_page"].endswith('.md'):
                page = warning["active_page"][:-2] + "html"
                active_txt = f'<a href="/{page}">{page}</a> -- '
            else:
                active_txt = ""
        else:
            active_txt = ""

        output += f'<p class="{cssclass}">{active_txt}{warntype}: {warning["message"]}</p>\n'
    return output



class GBRenderer:
    """
    This class is the renderer for GitBuilding HTML
    """
    FULLPAGE = 0
    IFRAME = 1
    PDFPAGE = 2

    def __init__(self, config, url_rules, root="/", static=True, no_server=False):
        """
        `static` sets whether it is generating a static site or a page for the live editor
        `no_server` is only used for static sites, sets whether the site is designed to work
                without a server running
        """

        self.config = config
        self._static = static
        self._no_server = no_server
        self._root = root
        self.custom_stylesheets = []
        self.custom_favicons = {'ico': [], 'png': []}
        self._warning_count = [0,0]

        # Variables that can be accessed by jinja templates
        self.populate_vars()
        self.scan_assets()
        self._url_rules = url_rules

        custom_path = "./_templates"
        template_path = GBPATH + "/templates"
        static_path = GBPATH + "/static"
        loader = FileSystemLoader([custom_path, template_path, static_path])
        self.env = Environment(loader=loader, trim_blocks=True)

    def set_warning_count(self, warnings):
        """
        Set the global warning count to be displayed on all pages
        """
        warning_count = [0,0]
        for warning in warnings:
            if warning["fussy"]:
                warning_count[1] += 1
            else:
                warning_count[0] += 1
        self._warning_count = warning_count

    def populate_vars(self):
        """
        This function populates a partial list of variables that can be used in
        templates. Some variables (with urls) are dynamically calculated later.
        To include dynamically calculated variables, make sure to use the
        _get_variables function.
        """
        self._variables = {"title": self.config.title,
                           "year": datetime.datetime.now().year,
                           "root": self._root}

        self._variables["authors"] = utilities.author_list(self.config)
        self._variables["email"] = self.config.email
        self._variables["affiliation"] = self.config.affiliation
        #Note licence is calculated dynamically

        for key in self.config.variables.keys():
            self._variables[key] = self.config.variables[key]

    def _get_variables(self, link=None):
        """
        link is used to change the url roots to relatative. Set link=None to use WebsiteRoot from
        the configuration file.
        """
        variables = copy(self._variables)
        if link is not None:
            relative_root = posixpath.relpath('.', posixpath.dirname(link)) + "/"
            variables['root'] = relative_root
        else:
            variables['root'] = "./"
        if self._no_server:
            url_translator = self._url_rules.create_translator(link)
            variables['landing'] = url_translator.simple_translate('index.md')
        else:
            variables['landing'] = variables['root']
        variables['license'] = self._get_license(link)
        return variables

    def _get_license(self, link):
        '''Returns the licence name or licence link. The variable link is the
        url of the page this text will go on. This allows relative links to be calculated
        '''
        if self.config.license is None:
            return None

        if self.config.license_file is None:
            return self.config.license

        if self.config.license_file.endswith('.md'):
            url_translator = self._url_rules.create_translator(link)
            licence_url = url_translator.simple_translate(self.config.license_file)
        return f'<a href="{licence_url}">{self.config.license}</a>'

    def scan_assets(self):
        """
        This scans the assets folder of the project to look for custom CSS and favicons
        """
        if exists_on_disk("assets"):
            css_files = get_matches_from_dir("assets", r"^.+\.css$")
            self.custom_stylesheets += css_files
            ico_favicons = get_matches_from_dir("assets", r"^favicon\.ico$")
            self.custom_favicons['ico'] += ico_favicons
            png_regex = r"favicon-([0-9]+)x[0-9]+\.png$"
            png_favicons = get_matches_from_dir("assets", r"^"+png_regex)
            for png_favicon in png_favicons:
                pixels = re.match(r".*"+png_regex, png_favicon).group(1)
                self.custom_favicons['png'].append((png_favicon, pixels))

    def nav_links(self, link=None):
        """
        This function returns the side navigation
        """

        navigation = deepcopy(self.config.navigation)
        for nav_item in navigation:
            if _is_active_nav_item(nav_item, link):
                nav_item['class'] = 'active'
                if "subnavigation" in nav_item:
                    for sub_nav_item in nav_item["subnavigation"]:
                        if _is_active_nav_item(sub_nav_item, link):
                            sub_nav_item['class'] = 'active'
                        else:
                            sub_nav_item['class'] = 'not-active'
            else:
                nav_item['class'] = 'not-active'
                if "subnavigation" in nav_item:
                    del nav_item["subnavigation"]

        tmpl = self.env.get_template("nav.html.jinja")
        html = tmpl.render(navigation=navigation, **self._get_variables(link))
        return html

    def project_header(self, subtitle=None, link=None):
        """
        This is the project header that can be customised.
        """
        tmpl = self.env.get_template("header.html.jinja")
        html = tmpl.render(subtitle=subtitle, **self._get_variables(link))
        return html

    def project_footer(self, link=None):
        """
        This returns either the standard project footer or the customised footer
        """
        tmpl = self.env.get_template("footer.html.jinja")
        html = tmpl.render(**self._get_variables(link))
        return html

    def favicon_html(self, link):
        """
        This returns the HTML for the favicon. Generates multiple PNG as well
        as ico favicon references based on the custom favicons found.
        """
        tmpl = self.env.get_template("favicon.html.jinja")
        num_custom_favicons = (len(self.custom_favicons['ico'])
                               + len(self.custom_favicons['png']))
        if num_custom_favicons == 0:
            ico_favicons = ["static/Logo/favicon.ico"]
            png_favicons = [("static/Logo/favicon-32x32.png", 32),
                            ("static/Logo/favicon-16x16.png", 16)]
        else:
            ico_favicons = self.custom_favicons['ico']
            png_favicons = self.custom_favicons['png']
        output = tmpl.render(ico_favicons=ico_favicons,
                             png_favicons=png_favicons,
                             **self._get_variables(link))
        return output

    def _replace_galleries(self, md):
        """
        Find galleries in the markdown a line with only images (must be more than
        one image) replace with gallery HTML
        """

        tmpl = self.env.get_template("gallery.html.jinja")
        imlines = re.findall(r'^((?:[ \t]*'+IMAGE_REGEX+'[ \t]*(?:\n|\r\n)?){2,})$',
                             md,
                             re.MULTILINE)
        # imlines uses the IMAGE_REGEX which matches lots of groups. First is the whole line.
        imlines = [line[0] for line in imlines]

        for gallery_number, imline in enumerate(imlines):
            images = re.findall(IMAGE_REGEX, imline)
            gallery_html = tmpl.render(gallery_number=gallery_number,
                                       images=images)
            md = md.replace(imline, gallery_html)
        return md

    def render_md(self, md, link, **kwargs):
        """
        This function returns the rendered HTML for input markdown
        """
        template = kwargs.get('template', self.FULLPAGE)
        if template != self.PDFPAGE:
            md = self._replace_galleries(md)

        base_extensions = ["markdown.extensions.tables",
                           "markdown.extensions.attr_list",
                           "markdown.extensions.fenced_code",
                           "markdown.extensions.toc"]
        extensions = base_extensions + ["markdown_katex", "codehilite"]

        extension_configs={'markdown_katex': {'no_inline_svg': True,
                                              'insert_fonts_css': True}}

        try:
            content_html = markdown(md,
                                    extensions=extensions,
                                    extension_configs=extension_configs)
        except KatexError:
            _LOGGER.warning("Latex Error, disabling katex")
            content_html = markdown(md, extensions=base_extensions)
        return self.render(content_html, link=link, **kwargs)

    def render(self, html, link, **kwargs):
        """
        This function creates the full HTML page from the input HTML generated from BuildUp
        """
        template = kwargs.get('template', self.FULLPAGE)
        nav = kwargs.get('nav', True)
        editorbutton = kwargs.get('editorbutton', False)
        meta_info = kwargs.get('meta_info', {})

        if link is None:
            editor_link = "-/editor"
        else:
            editor_link = f"/{link}/-/editor"

        input_dictionary = {'favicon_html': self.favicon_html(link),
                            'content': html,
                            'nav': nav,
                            'nav_links': self.nav_links(link),
                            'project_header': self.project_header(link=link),
                            'project_footer': self.project_footer(link),
                            'static': self._static,
                            'warning_count': self._warning_count,
                            'editorbutton': editorbutton,
                            'editor_link': editor_link,
                            'previewers_used': meta_info.get('previewers_used', [])}

        if template == self.FULLPAGE:
            tmpl = self.env.get_template("full_page.html.jinja")
            input_dictionary['custom_stylesheets'] = self.custom_stylesheets
        elif template == self.IFRAME:
            tmpl = self.env.get_template("iframe.html.jinja")
            custom_style = []
            for sheet in self.custom_stylesheets:
                custom_style.append(read_local_file(sheet))
            input_dictionary['custom_style'] = custom_style
        elif template == self.PDFPAGE:
            page_id = link.replace('/', '__')
            tmpl = self.env.get_template("pdfpage.html.jinja")
            input_dictionary['page_id'] = page_id
        else:
            raise ValueError(f'Unknown pdf template type: {template}')
        output = tmpl.render(**input_dictionary, **self._get_variables(link))

        return output

    def missing_page(self):
        """
        This returns an HTML page for missing parts.
        """

        missing_html = ("<h1>Missing Part</h1>\n\n"
                        "<p>This documentation has specified a part,"
                        " but not provided a link or further data.</p>")
        return self.render(missing_html, link="missing")

    def empty_homepage(self):
        """
        This returns an HTML page for the homepage if missing. This is only
        shown on the live server.
        """
        html = (r'<h1>No homepage set</h1>'
                r'<h2><a href="/-/create-homepage/">Create homepage</a></h2>')
        return self.render(html, editorbutton=False, link=None)

    def contents_page(self, file_list):
        """
        Returns an HTML page that lists all the documentation pages in the project.
        """
        url_translator = self._url_rules.create_translator('-/contents-page')
        md_pages = []
        for file_obj in file_list:
            if file_obj.path.endswith('.md'):
                web_path = url_translator.simple_translate(file_obj.path)
                md_pages.append([file_obj.path, web_path])
        md_pages.sort(key=lambda x: (len(x[1].split('/')), x[0].lower()))
        tmpl = self.env.get_template("contents.html.jinja")
        html = tmpl.render(md_pages=md_pages)
        return self.render(html, editorbutton=False, link="-/contents-page")

    def warning_page(self, log):
        """
        Return page with warnings for the entire documentation.
        """
        log_html = format_warnings(log, show_page=True)
        style_html = ("<style>\n"
                      "p.fussywarning {background: #fbe09e;}\n"
                      "p.fussywarning a{color: black; font-weight: bold;}\n"
                      "p.warning {background: #fb9e9e;}\n"
                      "p.warning a{color: black; font-weight: bold;}\n"
                      "</style>\n\n")
        return self.render(style_html+"<h1>Documentation warnings</h1>\n\n"+log_html, link="-/warnings")

    def new_page(self, error_message=None):
        """
        Returns the page for creating new pages
        """
        tmpl = self.env.get_template("new1.html.jinja")
        html = tmpl.render(error_message=error_message, **self._get_variables())
        return self.render(html, editorbutton=False, link="-/new-page/")

    def new_page_form(self, template, error_message=None):
        """
        Returns the form for creating a new page with the given template
        """
        tmpl = self.env.get_template("new2.html.jinja")
        html = tmpl.render(template=template, error_message=error_message, **self._get_variables())
        return self.render(html, editorbutton=False, link=f'-/new-template/{template}')

    def full_pdf(self, html_content, subtitle):
        """
        This method takes all pages as a combined block of html. It then uses the
        full_pdf template to generate an HTML file that WeasyPrint can use to create
        a PDF file.
        """
        pdf_title = self._variables['title']
        if pdf_title is not None and subtitle is not None:
            pdf_title += f' -- {subtitle}'
        tmpl = self.env.get_template("full_pdf.html.jinja")
        html = tmpl.render(content=html_content,
                           project_header=self.project_header(subtitle=subtitle),
                           project_footer=self.project_footer(),
                           pdf_title=pdf_title,
                           **self._get_variables())
        return html
