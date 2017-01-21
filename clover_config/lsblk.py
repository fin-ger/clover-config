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

from clover_config.log import Log
from clover_config.exit_code import ExitCode

def lsblk (*parameters):
    try:
        process = subprocess.Popen (["lsblk"].extend (parameters), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    except:
        Log.die (ExitCode.NOT_ROOT, "'lsblk' was not found in your PATH! This program must run as root to provide all features")
    out, err = process.communicate ()

    if len (err) > 0:
        Log.efibootmgr.error (err.decode ())

    return out.decode ()

class LsBlk:
    @staticmethod
    def get_efi_device ():
        out = lsblk ("-lpno", "MOUNTPOINT,FSTYPE,PARTTYPE,NAME")
        regex = r"/.+\s+vfat\s+c12a7328-f81f-11d2-ba4b-00a0c93ec93b\s+(.+)"
        m = re.search (regex, out)
        return m.group (1) if m is not None else None

    @staticmethod
    def get_disk_from_device (device):
        out = lsblk ("-lpno", "TYPE,NAME")
        regex = r"disk\s+(.+?)\npart\s+" + re.escape (device)
        m = re.search (regex, out)
        return m.group (1) if m is not None else None

    @staticmethod
    def get_partition_from_device (device):
        out = lsblk ("-no", "MAG:MIN", device)
        regex = r"\d+:(\d+)"
        m = re.search (regex, out)
        return m.group (1) if m is not None else None

    @staticmethod
    def get_mountpoint_from_device (device):
        return lsblk ("-no", "MOUNTPOINT", device)
