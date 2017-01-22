"""
clover-config - A clover efi bootloader configuration utility.
Copyright (C) 2017  Fin Christensen <christensen.fin@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import logging
import logging.handlers
import os.path

from colorlog import ColoredFormatter

HAS_SYSTEMD = True
try:
    from systemd.journal import JournalHandler
except ImportError as e:
    HAS_SYSTEMD = False

class LogManager:
    def __init__ (self):
        self.root = None
        self._file_formatter = None
        self._syslog_formatter = None
        self._console_formatter = None
        self._log_handler = None
        self._console_handler = None

    def init (self, log_level):
        self._file_formatter = logging.Formatter ("{asctime} [{name:<15.15}] [{levelname:<8.8}]: {message}", style = "{")
        self._syslog_formatter = logging.Formatter ("[{name:>15.15}] [{levelname:<8.8}]: {message}", style = "{")
        self._console_formatter = ColoredFormatter (
            "{log_color} * {reset}{message}", style = "{",
            log_colors={
                'DEBUG':    'bold_cyan',
                'INFO':     'bold_blue',
                'WARNING':  'bold_yellow',
                'ERROR':    'bold_red'
            }
        )

        if HAS_SYSTEMD:
            self._log_handler = JournalHandler (SYSLOG_IDENTIFIER = "clover-config")
            self._log_handler.setFormatter (self._syslog_formatter)
        else:
            log_path = os.path.join (os.path.expanduser ("~"), ".local", "share", "clover-config")
            if not os.path.exists (log_path):
                os.makedirs (log_path)
            log_file = os.path.join (log_path, "clover-config.log")
            self._log_handler = logging.handlers.RotatingFileHandler (
                log_file,
                # 1MB size and 10 files
                maxBytes = 1048576, backupCount = 9
            )
            self._log_handler.setFormatter (self._file_formatter)

        self._log_handler.setLevel (logging.INFO)

        self._console_handler = logging.StreamHandler ()
        self._console_handler.setFormatter (self._console_formatter)
        self.set_log_level (log_level)

        self.root = logging.getLogger ()
        self.root.name = "clover-config"
        self.root.setLevel (logging.DEBUG)
        self.root.addHandler (self._log_handler)
        self.root.addHandler (self._console_handler)

        if HAS_SYSTEMD:
            self.root.debug ("Using journald logging system...")
        else:
            self.root.debug ("Logging to `{}`".format (log_file))

    def __getattr__ (self, name):
        return logging.getLogger (name)

    def die (self, code, message = "An error occured during the execution of the current action"):
        self.root.error ("%s - aborting...", message)
        self.root.debug ("Exiting with exit code %d", code)
        sys.exit (code.value)

    def set_log_level (self, log_level):
        log_levels = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warning": logging.WARNING,
            "error": logging.ERROR
        }
        level = log_levels[log_level]
        self._console_handler.setLevel (level)

Log = LogManager ()
