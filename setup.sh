#!/bin/bash

# Update and install system dependencies
sudo apt-get update
sudo apt-get install -y python3 python3-pip git

# Install Python dependencies
pip3 install -r requirements.txt

# Run Fabric setup
fabric --setup

echo "Setup complete. You can now run the application with:"
echo "python3 app.py"