#!/bin/bash
lpstat
lpstat|awk '{print $1 }'|xargs cancel
echo "Killed!"
lpstat
