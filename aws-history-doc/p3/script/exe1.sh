#!/bin/bash
echo ">>> Create a dir name lab_files"
read dirName
mkdir $dirName
echo ">>> original permission"
ls -l | grep $dirName
echo ">>> after modified"
chmod 754 $dirName
ls -l | grep $dirName

echo ">>> Create data.txt in lab_files folder"
read fileName
mkdir lab_files/$fileName

echo ">>> original ownership"
ls -l lab_files | grep $fileName

echo ">>> create a new user"
read userName
sudo useradd -d /usr/$userName -c "new user for lab" -g ec2-user -p secret -s /usr/bin/bash $userName
sudo chown -R $userName lab_files/data.txt

echo ">>> new ownership"
ls -l lab_files | grep $fileName

echo ">>> set sticky bit on lab_files dir"
chmod +t lab_files
ls -l | grep lab_files

echo ">>> find files with .txt extension in lab_files"
find lab_files -name "*.txt"
