#!/usr/bin/bash

find ./ -type f -exec sed -i -e 's/\r$//' {} \;
