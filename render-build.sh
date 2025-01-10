#!/usr/bin/env bash
# Download and extract Chromium Portable
mkdir -p /opt/chromium
curl -L https://commondatastorage.googleapis.com/chromium-browser-snapshots/Linux_x64/1085174/chrome-linux.zip -o /tmp/chrome-linux.zip
unzip /tmp/chrome-linux.zip -d /opt/chromium
