# Hyprpy testing

Testing Hyprpy is a bit tricky.
Since running any kind of realistic unit or integration test requires a reproducable, running
instance of Hyprland, running the tests inside virtual machines with a graphical session
is required.

> If you can get Hyprland to run reliably, and independently of the host system inside a Docker container, please let me know!

## Dependencies

To create, modify and run the virtual machines, some dependencies are required on your system.
Make sure you enable KVM in your UEFI/BIOS.

If you are using NixOS, you can use the provided `shell.nix` to install all required dependencies
in an ephemeral shell.
To do this, simply run `nix-shell` while inside the `tests` directory.

If you are using a different distribution, instructions are listed below.

### Qemu

`qemu` is the virtualization software required to launch the virtual machines.
You can install it using your package manager.

The tests use the `virtio` graphics driver, without which Hyprland will not launch.
For performance reasons, they also run `qemu` in `KVM` mode, which must be enabled in your
UEFI/BIOS for the tests to work.

### libguestfs

The [libguestfs](https://libguestfs.org/) suite is required to modify the VMs for testing.
Your distribution's package manager should let you install the package.

For Arch Linux, you need to install [extra/libguestfs](https://www.archlinux.org/packages/extra/x86_64/libguestfs/).

On NixOS, if you are not using the provided `shell.nix` environment, you have to install
[libguestfs-with-appliance](https://search.nixos.org/packages?channel=unstable&from=0&size=50&sort=relevance&type=packages&query=libguestfs-with-appliance).

On Debian and Ubuntu, install [libguestfs-tools](https://packages.ubuntu.com/kinetic/libguestfs-tools).

### Python requests

The Python [requests](https://pypi.org/project/requests/) library is required to fetch VM images.
Install it via your package manager or using `pip`.

On Arch Linux, install [extra/python-requests](https://archlinux.org/packages/extra/any/python-requests/).

On NixOS, if not using the provided `shell.nix` environment, install [python311Packages.requests](https://search.nixos.org/packages?channel=unstable&from=0&size=50&sort=relevance&type=packages&query=python311Packages.requests).

On Debian and Ubuntu, install [python3-requests](https://packages.ubuntu.com/kinetic/python3-requests).

If you want to use pip, run the following:

```bash
pip install requests
```
