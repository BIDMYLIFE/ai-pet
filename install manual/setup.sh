#!/bin/bash

# This script sets up the environment for the AI Pet project.

# Update package list and install necessary packages
echo "Updating package list..."
sudo apt-get update

echo "Installing required packages..."
sudo apt-get install -y \
    python3 \
    python3-pip \
    sox \
    pulseaudio-utils \
    arecord \
    ffmpeg

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r ../requirements.txt

echo "Setup complete!"