{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    nativeBuildInputs = with pkgs; [
      qemu
      libguestfs-with-appliance
      python311Packages.requests
    ];
}
