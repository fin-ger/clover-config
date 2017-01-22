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

import argparse

from argparse import RawTextHelpFormatter
from clover_config.actions import Actions

description = """A clover efi bootloader configuration utility.

available actions:
  status                show the current status of clover.
  install               install the clover EFI boot entry.
  remove                remove the clover EFI boot entry.
  update                update the boot entries of clover with the
                        configuration given in /etc/clover/menu.conf.
  efi-check             check if the current system is booted in efi
                        mode.
"""

loglevel_help = """set the minimum loglevel a message should have to
appear on the console. The loglevel for the syslog
will be `info` regardless of this setting.
"""

def main ():
    parser = argparse.ArgumentParser (
        prog = "clover-config",
        description = description,
        epilog = "clover-config  Copyright (C) 2017  Fin Christensen",
        formatter_class = RawTextHelpFormatter
    )
    parser.add_argument (
        "action", metavar = "ACTION", choices = ["status", "install", "remove", "update", "check-efi"],
        help = "the action that should be applied on the clover config."
    )
    parser.add_argument (
        "-l", "--loglevel", default = "info", choices = ["debug", "info", "warning", "error"],
        help = loglevel_help
    )
    parser.add_argument (
        "-v", "--version", action = "version", version = "%(prog)s 0.0.1"
    )
    args = parser.parse_args ()

    from clover_config.log import Log

    Log.init (args.loglevel)
    Actions[args.action] ()
