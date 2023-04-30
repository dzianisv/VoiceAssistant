#!/bin/bash

GIT_REPO=https://github.com/dzianisv/AssistanPlato.git

# Check if the script is run with root privileges
if [ "$(id -u)" -ne 0 ]; then
  echo "This script must be run as root."
  exit 1
fi

apt-get update -yq && apt-get install -y git python3 python3-pip
pip3 install pipenv

# Extract the project name from the repository URL
PROJECT_NAME=$(basename -s .git "$GIT_REPO")

# Clone the Git repository into the /opt directory
git clone "$GIT_REPO" "/opt/$PROJECT_NAME"

# Change to the project directory
cd "/opt/$PROJECT_NAME" || exit

if [ ! -f .env ]; then
    cp env .env
fi

# Install the Python dependencies with Pipenv
pipenv install

# Get the path to the pipenv executable
PIPENV_PATH=$(command -v pipenv)

# Create a systemd service file for the project
SERVICE_FILE="/etc/systemd/system/${PROJECT_NAME}.service"
cat > "$SERVICE_FILE" << EOF
[Unit]
Description=${PROJECT_NAME} Service
After=network.target

[Service]
Type=simple
EnvironmentFile=/opt/${PROJECT_NAME}/.env
WorkingDirectory=/opt/${PROJECT_NAME}
ExecStart=${PIPENV_PATH} run python3 src/main.py
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOF

# Reload the systemd configuration
systemctl daemon-reload

# Enable and start the service
systemctl enable "${PROJECT_NAME}.service"
systemctl start "${PROJECT_NAME}.service"

echo "The ${PROJECT_NAME} service has been installed and started."
