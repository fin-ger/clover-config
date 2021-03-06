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

import subprocess
import re
import os.path

from clover_config.log import Log
from clover_config.exit_code import ExitCode
from clover_config.lsblk import LsBlk

def efibootmgr (*parameters, die_on_failure = True):
    Log.efibootmgr.debug ("Calling subprocess: efibootmgr %s", " ".join (parameters))
    try:
        process = subprocess.Popen (["efibootmgr"] + list (parameters),
                                    stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    except FileNotFoundError:
        Log.die (ExitCode.NOT_ROOT, "Executable 'efibootmgr' not found in PATH! Try running this program "
                 "as root or install the package containing this executable with your distributions package manager")

    out, err = process.communicate ()

    Log.efibootmgr.debug ("Subprocess efibootmgr exited with exit code %d", process.returncode)

    if len (err) > 0:
        Log.efibootmgr.error (err.decode ())

    if die_on_failure and process.returncode != 0:
        Log.efibootmgr.error ("An error occured while configuring your EFI setup!")
        Log.efibootmgr.error ("Please check your EFI configuration manually with `efibootmgr`.")
        Log.efibootmgr.error ("This error might have damaged existing boot configurations!")
        Log.die (ExitCode.EFIBOOTMGR_ERROR, "Error while configuring EFI boot!")

    return out.decode ()

class EFIBootManager:
    Device = None
    Disk = None
    Partition = None
    Mountpoint = None
    _initialized = False

    @staticmethod
    def _initialize ():
        if EFIBootManager._initialized:
            return

        EFIBootManager.check_efi ()

        Log.efibootmgr.info ("Checking for a mounted EFI partition...")
        EFIBootManager.Device = LsBlk.get_efi_device ()

        if EFIBootManager.Device is None:
            Log.die (ExitCode.NO_EFI_DEVICE, "No mounted EFI partition found")

        EFIBootManager.Disk = LsBlk.get_disk_from_device (EFIBootManager.Device)
        EFIBootManager.Partition = LsBlk.get_partition_from_device (EFIBootManager.Device)
        EFIBootManager.Mountpoint = LsBlk.get_mountpoint_from_device (EFIBootManager.Device)
        Log.efibootmgr.info ("Using %s as EFI partition mountpoint.", EFIBootManager.Mountpoint)
        EFIBootManager._initialized = True

    @staticmethod
    def get_bootnum (entry):
        EFIBootManager._initialize ()
        regex = r"^Boot(\w{4}).?\s+" + re.escape (entry) + r"$"
        m = re.search (regex, efibootmgr (), re.MULTILINE)
        res = m.group (1) if m is not None else None
        Log.efibootmgr.debug ("Boot entry position of '%s' is %s", entry, res)
        return res

    @staticmethod
    def is_active (entry):
        EFIBootManager._initialize ()
        regex = r"^Boot\w{4}\*\s+" + re.escape (entry) + r"$"
        m = re.search (regex, efibootmgr (), re.MULTILINE)
        res = True if m is not None else None
        Log.efibootmgr.debug ("Boot entry '%s' is %s", entry, "active" if res else "inactive")
        return res

    @staticmethod
    def try_remove_boot_entry (entry):
        EFIBootManager._initialize ()
        Log.efibootmgr.info ("Removing old '%s' boot entry of existing...", entry)
        bootnum = EFIBootManager.get_bootnum (entry)

        if bootnum is not None:
            efibootmgr ("-b", bootnum, "-B")

    @staticmethod
    def get_boot_order ():
        EFIBootManager._initialize ()
        regex = r"BootOrder: (.+)"
        m = re.search (regex, efibootmgr ())
        res = m.group (1) if m is not None else ""
        Log.efibootmgr.debug ("Current EFI boot order is: %s", res)
        return res

    @staticmethod
    def set_boot_order (boot_order):
        EFIBootManager._initialize ()
        Log.efibootmgr.info ("Writing new boot order...")
        Log.efibootmgr.debug ("New EFI boot order is: %s", boot_order)
        efibootmgr ("-o", boot_order)

    @staticmethod
    def add_boot_entry (label, loader):
        EFIBootManager._initialize ()
        Log.efibootmgr.info ("Adding new '%s' boot entry...", label)
        efibootmgr ("-d", EFIBootManager.Disk, "-p", EFIBootManager.Partition, "-c", "-L", label, "-l", loader)

    @staticmethod
    def check_efi ():
        Log.efibootmgr.info ("Checking if system is booted in EFI mode...")
        Log.efibootmgr.debug ("Checking if '/sys/firmware/efi' exists...")

        if not os.path.isdir ("/sys/firmware/efi"):
            Log.efibootmgr.error ("This system is not booted in EFI mode!")
            Log.efibootmgr.error ("")
            Log.efibootmgr.error ("Note: This program currently has no support for BIOS booted systems.")
            Log.efibootmgr.error ("      To install clover on a BIOS system either install it manually or submit")
            Log.efibootmgr.error ("      a pull request on github adding BIOS support to this program.")
            Log.efibootmgr.error ("")
            Log.efibootmgr.error ("GitHub: https://github.com/fin-ger/clover-config")
            Log.die (ExitCode.NOT_IN_EFI_MODE, "System is NOT booted in EFI mode!")
