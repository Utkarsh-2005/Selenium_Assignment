#!/usr/bin/env bash
# Create a directory for Chromium
mkdir -p /tmp/chromium

# Download Chromium Portable
curl -L https://commondatastorage.googleapis.com/chromium-browser-snapshots/Linux_x64/1085174/chrome-linux.zip -o /tmp/chrome-linux.zip

# Extract the Chromium archive
unzip /tmp/chrome-linux.zip -d /tmp/chromium

# Debug: Check if the binary exists
if [ -f "/tmp/chromium/chrome-linux/chrome" ]; then
  echo "Chromium extracted successfully."
else
  echo "Failed to extract Chromium."
  exit 1
fi
