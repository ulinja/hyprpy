FROM archlinux:latest

# Install packages
RUN pacman-key --init && \
    pacman -Syu --noconfirm && \
    pacman -S --noconfirm hyprland python && \
    pacman -Scc --noconfirm

# Create non-root user
ENV CUSTOM_USERNAME="hyprpy"
ENV HOME_DIR="/home/${CUSTOM_USERNAME}"
RUN useradd --user-group --create-home --home-dir ${HOME_DIR} --shell /bin/bash ${CUSTOM_USERNAME}

# Copy context files
COPY --chown=${CUSTOM_USERNAME}:${CUSTOM_USERNAME} --chmod=744 entrypoint.sh ${HOME_DIR}/entrypoint.sh

# Run tests
USER ${CUSTOM_USERNAME}
ENTRYPOINT ${HOME_DIR}/entrypoint.sh
