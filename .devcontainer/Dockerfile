FROM ubuntu:24.04

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# Configure apt and install packages
RUN apt-get update \
    && apt-get -y install --no-install-recommends \
    apt-utils \
    dialog \
    && apt-get -y install \
    git \
    curl \
    wget \
    ca-certificates \
    build-essential \
    sudo \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Install Python 3.12 (default in Ubuntu 24.04)
RUN apt-get update \
    && apt-get -y install \
    python3.12 \
    python3.12-venv \
    python3.12-dev \
    python3-pip \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3.12 1 \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1 \
    && rm -rf /var/lib/apt/lists/*

# Install UV (Python package manager)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# Create a non-root user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN if getent group $USER_GID > /dev/null 2>&1; then \
        EXISTING_GROUP=$(getent group $USER_GID | cut -d: -f1); \
        if [ "$EXISTING_GROUP" != "$USERNAME" ]; then \
            groupmod -n $USERNAME $EXISTING_GROUP || groupadd --gid $((USER_GID + 1)) $USERNAME; \
        fi; \
    else \
        groupadd --gid $USER_GID $USERNAME; \
    fi \
    && if getent passwd $USER_UID > /dev/null 2>&1; then \
        EXISTING_USER=$(getent passwd $USER_UID | cut -d: -f1); \
        usermod -l $USERNAME -d /home/$USERNAME -m $EXISTING_USER 2>/dev/null || useradd --uid $((USER_UID + 1)) --gid $USERNAME -m $USERNAME -s /bin/bash; \
    else \
        useradd --uid $USER_UID --gid $USERNAME -m $USERNAME -s /bin/bash; \
    fi \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Install UV for the non-root user
USER $USERNAME
RUN curl -LsSf https://astral.sh/uv/install.sh | sh


ENV PATH="/home/${USERNAME}/.local/bin:${PATH}"

# Set working directory
WORKDIR /workspaces/project

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=dialog
