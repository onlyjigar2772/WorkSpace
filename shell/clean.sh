#!/usr/bin/bash
#Author - Jigar.
#About - This script uses find command to find all files. Then executes
# a sed command on each file to remove /r. Uses exec to execute the cmd


find ./ -type f -exec sed -i -e 's/\r$//' {} \;
