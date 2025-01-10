#!/usr/bin/env bash
# Install Chrome
apt-get update
apt-get install -y wget unzip
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
#!/usr/bin/env bash
# Download and set up prebuilt Chrome
mkdir -p /opt/chrome
curl -L https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o /tmp/google-chrome.deb
dpkg-deb -x /tmp/google-chrome.deb /opt/chrome
ln -sf /opt/chrome/opt/google/chrome/google-chrome /usr/bin/google-chrome
