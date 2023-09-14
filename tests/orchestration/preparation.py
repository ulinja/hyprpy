"""Functions for obtaining and preparing a Arch Linux VM disk images as test systems."""

import shutil
from pathlib import Path
from typing import Union, Optional
import subprocess

from tests import PATH_TO_CACHE_DIR
from tests import logger as log
from tests.utils.requests import download


PATH_TO_RAW_IMAGE = PATH_TO_CACHE_DIR/'test-system_raw.qcow2'
PATH_TO_PREPARED_IMAGE = PATH_TO_CACHE_DIR/'test-system_prepared.qcow2'
PATH_TO_ASSETS_DIR = PATH_TO_CACHE_DIR.parent/'orchestration'/'assets'


def get_raw_image():
    """Retrieves a fresh Arch Linux Qcow2 VM image from a mirror.

    Saves it to the cache directory as ``test-system_raw.qcow2``.
    """

    URL = 'http://ftp.uni-hannover.de/archlinux/images/latest/Arch-Linux-x86_64-basic.qcow2'

    log.info("Retrieving a fresh base VM image from mirror...")

    if not PATH_TO_CACHE_DIR.exists():
        PATH_TO_CACHE_DIR.mkdir(parents=True)
    else:
        if not PATH_TO_CACHE_DIR.is_dir():
            raise NotADirectoryError(f"Expected a directory at '{PATH_TO_CACHE_DIR}'.")

    download(URL, PATH_TO_RAW_IMAGE, overwrite=True)

    log.info("Base image retrieved successfully.")


def run_vm(path_to_image: Union[Path, str]) -> None:
    run_command = ["qemu-system-x86_64", "-enable-kvm", "-vga", "virtio", "-m", "4G", f"{path_to_image}"]
    subprocess.run(run_command, text=True, check=True)


def create_prepared_image():
    log.info("Creating a prepared image...")

    if not PATH_TO_RAW_IMAGE.is_file():
        raise FileNotFoundError(f"No raw image found for preparation.")

    log.info("Creating a copy of the raw image...")
    shutil.copy(PATH_TO_RAW_IMAGE, PATH_TO_PREPARED_IMAGE)
    log.info("Raw image copied.")

    log.info("Adding files for initial run...")
    guestfish_input = f"add {PATH_TO_PREPARED_IMAGE}\n" \
        "run\n" \
        "mount /dev/sda3 /\n" \
        "mkdir /etc/systemd/system/getty@tty1.service.d\n" \
        f"copy-in {PATH_TO_ASSETS_DIR/'autologin.conf'} /etc/systemd/system/getty@tty1.service.d/\n" \
        "chown 0 0 /etc/systemd/system/getty@tty1.service.d/autologin.conf\n" \
        f"copy-in {PATH_TO_ASSETS_DIR/'bashprofile-initial.bash'} /home/arch/\n" \
        f"mv /home/arch/bashprofile-initial.bash /home/arch/.bash_profile\n" \
        "chown 1000 1000 /home/arch/.bash_profile\n" \
        "umount-all\n" \
        "quit\n"
    subprocess.run(['guestfish'], input=guestfish_input, text=True, check=True)
    log.info("Files for initial run were added.")

    log.info("Launching VM for initial run.")
    run_vm(PATH_TO_PREPARED_IMAGE)
    # TODO check for errors in first run
    log.info("Initial run successful.")

    log.info("Adding files for final prep...")
    guestfish_input = f"add {PATH_TO_PREPARED_IMAGE}\n" \
        "run\n" \
        "mount /dev/sda3 /\n" \
        "mkdir /home/arch/.config\n" \
        "chown 1000 1000 /home/arch/.config\n" \
        "mkdir /home/arch/.config/hypr\n" \
        "chown 1000 1000 /home/arch/.config/hypr\n" \
        f"copy-in {PATH_TO_ASSETS_DIR/'hyprland.conf'} /home/arch/.config/hypr/\n" \
        "chown 1000 1000 /home/arch/.config/hypr/hyprland.conf\n" \
        f"copy-in {PATH_TO_ASSETS_DIR/'run-tests.sh'} /home/arch/\n" \
        "chown 1000 1000 /home/arch/run-tests.sh\n" \
        f"chmod 0744 /home/arch/run-tests.sh\n" \
        f"copy-in {PATH_TO_ASSETS_DIR/'bashprofile-final.bash'} /home/arch/\n" \
        f"mv /home/arch/bashprofile-final.bash /home/arch/.bash_profile\n" \
        "chown 1000 1000 /home/arch/.bash_profile\n" \
        "umount-all\n" \
        "quit\n"
    subprocess.run(['guestfish'], input=guestfish_input, text=True, check=True)
    log.info("Final prep completed.")

    # TODO remove raw image
