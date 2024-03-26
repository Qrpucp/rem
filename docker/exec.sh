#!/bin/bash

# get user name through /etc/group
exec su $(tail -n 1 /etc/group | awk -F':' '{print $1}')

# exec newgrp rem
