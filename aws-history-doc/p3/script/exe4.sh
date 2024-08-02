#!/bin/bash
echo ">>> Display network interface configuration"
ip addr show

echo ">>> Test connectivity to google.com"
ping -c 5 google.com

echo ">>> Query DNS servers for info about google.com domain name"
#host google.com
dig google.com
