[[ -f ~/.bashrc ]] && . ~/.bashrc

# Initialze the pacman keyring
sleep 2 ; sudo pacman-key --init
# Pull in latest packages and update
sudo pacman -Syu --noconfirm
# Install Hyprland and Python
sudo pacman -S --noconfirm hyprland python kitty
# Clean out package cache
sudo pacman -Scc --noconfirm
# Shut down
sudo shutdown now
