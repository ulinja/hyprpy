"""Functions for obtaining and preparing a Arch Linux VM disk images as test systems."""

import shutil
import subprocess
import tempfile
from datetime import datetime

from tests import PATH_TO_CACHE_DIR
from tests import logger as log


PATH_TO_PREPARED_IMAGE = PATH_TO_CACHE_DIR/'test-system_prepared.qcow2'


def run_test_vm() -> None:
    log.info("Creating a test run image...")
    if not PATH_TO_PREPARED_IMAGE.is_file():
        raise FileNotFoundError(f"No prepared image found.")
    path_to_test_image = PATH_TO_CACHE_DIR/f"test-system_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.qcow2"
    shutil.copy(PATH_TO_PREPARED_IMAGE, path_to_test_image)

    # TODO add test files
    log.info("Adding files for test run...")
    guestfish_input = f"add {path_to_test_image}\n" \
        "run\n" \
        "mount /dev/sda3 /\n" \
        "write /home/arch/test.log '[ERROR] Tests did not run!'\n" \
        "chown 1000 1000 /home/arch/test.log\n" \
        "umount-all\n" \
        "quit\n"
    subprocess.run(['guestfish'], input=guestfish_input, text=True, check=True)
    log.info("Files for test run were added.")

    log.info("Launching test run image...")
    run_command = ["qemu-system-x86_64", "-enable-kvm", "-vga", "virtio", "-m", "4G", f"{path_to_test_image}"]
    subprocess.run(run_command, text=True, check=True)

    with tempfile.TemporaryDirectory() as tmp_dir:
        log.info("Retrieving test logs...")
        path_to_logfile = f"{tmp_dir}/test.log"
        guestfish_input = f"add {path_to_test_image}\n" \
            "run\n" \
            "mount /dev/sda3 /\n" \
            f"copy-out /home/arch/test.log {tmp_dir}/\n" \
            "umount-all\n" \
            "quit\n"
        subprocess.run(['guestfish'], input=guestfish_input, text=True, check=True)
        log.info("Test logs retrieved:")

        with open(path_to_logfile, 'r') as logfile:
            for line in logfile.readlines():
                print(line)

    log.info("Purging test run image...")
    path_to_test_image.unlink()
    log.info("Test run completed.")
