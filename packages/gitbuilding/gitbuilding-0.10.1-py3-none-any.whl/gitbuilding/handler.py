"""
This submodule deals with the logging handler that GitBuilding uses to pretty print
warnings into the terminal and to forward warnings to the server
"""

import logging
from colorama import Fore, Style

class GBHandler(logging.Handler):
    """
    A child class of logging.Handler. This class which handles logging records for
    GitBuilding it logs to std.out in colour and saves a warnings to an internal log
    that that can then be accessed by the server.
    """

    def __init__(self, silent=False):
        super().__init__(level=logging.DEBUG)
        self._active_page = None
        self._log = []
        self._silent = silent

    @property
    def log_length(self):
        """
        Returns the current length of the warning log
        """
        return len(self._log)

    def log_from(self, position):
        """
        Return a slice of the warning log from `position` onwards
        """
        return self._log[position:]

    @property
    def _active_string(self):
        """
        Read only property for the output string for the active page.
        """
        if self._active_page is not None:
            return f' - when scanning page {self._active_page}'
        return ''

    def emit(self, record):
        """
        Emit will both save the logged record to the log and print the
        record if it is a warning or above.
        Info messages are used to set the active page but they are neither
        printed or logged.
        """
        try:
            # Default is -1 because need to be able to send string or None
            if getattr(record, "set_active_page", -1) != -1:
                if isinstance(record.set_active_page, str):
                    self._active_page = record.set_active_page
                else:
                    self._active_page = None

            if getattr(record, "fussy", None) is not None:
                fussy = record.fussy
            else:
                fussy = False

            if record.levelno > 20:

                message = self.format(record)
                self._pretty_print_message(message, fussy)
                self._log.append({"message": message,
                                  "active_page": self._active_page,
                                  "fussy": fussy})
        except RecursionError:
            raise
        except Exception: # pylint: disable=broad-except
            self.handleError(record)

    def _pretty_print_message(self, message, fussy):
        if not self._silent:
            full_message = message+self._active_string
            if fussy:
                print(Fore.YELLOW+"Fussy Warning: "+full_message+Style.RESET_ALL)
            else:
                print(Fore.RED+"Warning: "+full_message+Style.RESET_ALL)
