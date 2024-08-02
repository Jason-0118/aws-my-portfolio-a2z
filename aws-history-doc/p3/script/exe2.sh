#!/bin/bash
echo ">>> create a new group named developers"
read groupName
sudo groupadd $groupName

echo ">>> create a user name intern and add to the developers group"
read userName
sudo useradd -d /usr/$userName -c "intern user for lab" -g ec2-user -p secret -s /usr/bin/bash $userName
sudo gpasswd -M $userName $groupName

echo ">>> all groups the intern user belongs to:"
#groups $userName -> users : groups
id -Gn $userName

echo ">>> detailed info about the developers group"
getent group $groupName
