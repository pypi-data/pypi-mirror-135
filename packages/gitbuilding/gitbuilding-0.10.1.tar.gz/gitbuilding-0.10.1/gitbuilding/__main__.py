#!/usr/bin/env python
"""
The entrypoint of GitBuilding it is run when `gitbuilding` is run from the commandline.
"""

import sys
import argparse
import logging
from colorama import Fore, Style
import pkg_resources
from gitbuilding import example, server
from gitbuilding.handler import GBHandler
from gitbuilding.output import MarkdownBuilder, StaticSiteBuilder, PdfBuilder
from gitbuilding.generate_ci import generate_ci
from gitbuilding.native_file_operations import is_local_file, clean_documentation_dir

class GBParser():
    """
    The GitBuilding commandline (argparse) parser, it has a number of sub-parsers for
    the sub-commands such as `build` or `serve`
    """

    def __init__(self):
        gb_description = "Run GitBuilding to build your documentation"
        self._parser = argparse.ArgumentParser(description=gb_description,
                                               formatter_class=argparse.RawTextHelpFormatter)

        self._parser.add_argument("--version",
                                  action="store_true",
                                  dest="version",
                                  help="Print version information.")

        subparsers = self._parser.add_subparsers(help="Function of command",
                                                 metavar="<command>",
                                                 dest="command")
        buildelp_str = "Converts the documentation to standard markdown"
        self._parser_build = subparsers.add_parser("build", help=buildelp_str)
        self._parser_new = subparsers.add_parser("new", help="New gitbuilding project")

        serve_help_str = "Start local server to view documentation"
        self._parser_serve = subparsers.add_parser("serve",
                                                   help=serve_help_str)

        dev_help_str = "Use npm dev server for live editor. Beware, here be dragons!"
        self._parser_serve.add_argument("--dev",
                                        action="store_true",
                                        dest="dev",
                                        help=dev_help_str)

        self._parser_html = subparsers.add_parser("build-html", help="Build static HTML site")

        no_server_help_str = ("Use this option to create an HTML site that will work without "
                              "requiring a web server.")
        self._parser_html.add_argument("--no-server",
                                       action="store_true",
                                       dest="no_server",
                                       help=no_server_help_str)

        pdf_help_str = "Create PDF of documentation (requires WeasyPrint)"
        self._parser_pdf = subparsers.add_parser("build-pdf",
                                                 help=pdf_help_str)

        hardwarning_help_str = "Exit with a code of 1 instead of 0 if documentation has warnings"
        self._add_arg_to_all_builders("--hardwarnings",
                                      action="store_true",
                                      dest="hardwarnings",
                                      help=hardwarning_help_str)

        promotefussy_help_str = "If hardwarnings are enabled, exit status will also depend on fussy warnings"
        self._add_arg_to_all_builders("--promotefussy",
                                      action="store_true",
                                      dest="promotefussy",
                                      help=promotefussy_help_str)

        self._parser_generate = subparsers.add_parser("generate", help="Generate files, e.g. ci.")
        generate_type_help_str = "Type of files to generate, currently only supports `ci`."
        self._parser_generate.add_argument("generate_file_type",
                                           metavar="<file_type>",
                                           nargs="?",
                                           type=str,
                                           help=generate_type_help_str)

        self._parser_clean = subparsers.add_parser("clean",
                                                   help="Remove files created by GitBuilding")

        help_help_str = "Run 'help <command>' for detailed help"
        self._parser_help = subparsers.add_parser("help",
                                                  help=help_help_str)

        self._parser_help.add_argument("h_command",
                                       metavar="<command>",
                                       nargs="?",
                                       type=str,
                                       help="Command to show help for")

    def _add_arg_to_all_builders(self, *args, **kwargs):
        self._parser_build.add_argument(*args, **kwargs)
        self._parser_html.add_argument(*args, **kwargs)
        self._parser_pdf.add_argument(*args, **kwargs)


    def parse_args(self, args=None, namespace=None):
        """
        Runs parse_args on the main argparse parser
        """
        return self._parser.parse_args(args=args, namespace=namespace)

    def print_help(self, command):
        """
        Can print help for `gitbuilding` or help for each gitbuilding command.
        """
        if command is None:
            self._parser.print_help()
        elif command == "build":
            print("\n`build` will convert the documentation in the current folder\n"
                  "into standard markdown.\n")
            print(self._parser_build.format_help())
        elif command == "build-html":
            print("\n`build-html` will create a static html website using the\n"
                  "documentation in the current folder\n")
            print(self._parser_html.format_help())
        elif command == "build-pdf":
            print("\n`build-pdf` will create a static html website using the\n"
                  "documentation in the current folder. This requires WeasyPrint\n"
                  "to be installed which can be non trivial. We are working on\n"
                  "a better solution.\n")
            print(self._parser_pdf.format_help())
        elif command == "serve":
            print("\n`serve` will create a local webserver to view your built\n"
                  "documentation rendered in HTML.\n")
            print(self._parser_serve.format_help())
        elif command == "new":
            print("\n`new` will create an empty gitbuilding project in the\n"
                  "current folder if empty. If the current folder is not\n"
                  "empty it will ask for a subfolder name for the project\n")
            print(self._parser_new.format_help())
        elif command == "generate":
            print("\n`generate` is used to create special files. Currently\n"
                  "the only option is `ci`.\n"
                  "`generate ci` Will create a continuous integration script\n"
                  "to build the documention into a website.\n")
            print(self._parser_generate.format_help())
        elif command == "clean":
            print("\n`clean` is used to remove all files create by GitBuilding\n")
            print(self._parser_clean.format_help())
        else:
            print(f"Invalid gitbuilding command {command}\n\n")
            self._parser.print_help()

def exit_code(handler, args):
    """
    Check handler for warnings and exit with correct code depending
    on command and hardwarning setting
    """
    if args.command in ["build", "build-html", "build-pdf"]:
        if args.hardwarnings:
            logs = handler.log_from(0)
            if args.promotefussy:
                if len(logs) > 0:
                    return 1
            else:
                warnings = [log for log in logs if not log['fussy']]
                if len(warnings) > 0:
                    return 1
    return 0

def main(input_args=None):
    """This is what runs if you run `gitbuilding` from the terminal
    `input_args` can be used to run main from inside python, else sys.argv[1:]
    is used.
    """

    parser = GBParser()
    args = parser.parse_args(args=input_args)

    if args.version:
        print(pkg_resources.get_distribution("gitbuilding").version)
        return 0

    if is_local_file("buildconf.yaml"):
        config_file = "buildconf.yaml"
    else:
        config_file = None

    handler = GBHandler()

    logger = logging.getLogger('BuildUp')
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.propagate = False

    if args.command == "build":
        md_builder = MarkdownBuilder(config_file)
        md_builder.build()

    elif args.command == "new":
        example.output_example_project()

    elif args.command == "serve":

        if args.dev:
            gbs = server.DevServer(config_file, handler)
            print(Fore.RED+
                  "\n\n   WARNING! You are using the gitbuilding dev server."+
                  "\nHere be dragons!\n\n"+
                  Style.RESET_ALL)
            from flask_cors import CORS # pylint: disable=import-outside-toplevel

            CORS(gbs)
            gbs.run(use_waitress=False)
        else:
            gbs = server.GBServer(config_file, handler)
            gbs.run()

    elif args.command == "build-html":
        site_builder = StaticSiteBuilder(config_file, no_server=args.no_server)
        site_builder.build()

    elif args.command == "build-pdf":
        site_builder = PdfBuilder(config_file)
        site_builder.build()

    elif args.command == "generate":
        if args.generate_file_type == "ci":
            generate_ci()
        else:
            print("Needs an argument for type of file to generate, e.g. `ci`.")

    elif args.command == "clean":
        clean_documentation_dir()

    elif args.command == "help":
        parser.print_help(args.h_command)
    else:
        print(f"Invalid gitbuilding command {args.command}")
    return exit_code(handler, args)


if __name__ == "__main__":
    sys.exit(main())
