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

from clover_config.log import Log
from clover_config.efibootmgr import EFIBootManager
from clover_config.config import Config

EFI_ENTRY_LABEL = "Clover"
EFI_ENTRY_LOADER = "/EFI/CLOVER/CLOVERX64.efi"

def install ():
    EFIBootManager.try_remove_boot_entry (EFI_ENTRY_LABEL)

    if Config.EFIDefault:
        boot_order = EFIBootManager.get_boot_order ()

    EFIBootManager.add_boot_entry (EFI_ENTRY_LABEL, EFI_ENTRY_LOADER)

    if Config.EFIDefault:
        bootnum = EFIBootManager.get_bootnum (EFI_ENTRY_LABEL)
        Log.install.info ("Setting clover as the default EFI boot entry...")
        if boot_order is None:
            boot_order = bootnum
        else:
            boot_order = "{},{}".format (bootnum, boot_order)
        EFIBootManager.set_boot_order (boot_order)

def remove ():
    EFIBootManager.try_remove_boot_entry (EFI_ENTRY_LABEL)

def status ():
    pass

def update ():
    pass

def efi_check ():
    EFIBootManager.efi_check ()

Actions = {
    "status": status,
    "install": install,
    "remove": remove,
    "update": update,
    "efi-check": efi_check
}
