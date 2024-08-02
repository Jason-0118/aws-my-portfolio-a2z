#!/bin/bash
echo ">>> Download the installation file using curl"
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"

echo ">>> Unzip the installer"
unzip awscliv2.zip

echo ">>> Run the install program"
sudo ./aws/install

echo ">>> Verify "
aws help
