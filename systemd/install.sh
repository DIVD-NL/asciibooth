#!/bin/bash

cp *.service /lib/systemd/system/
systemctl enable ascii_http.service
service ascii_http start
systemctl enable ascii_email_and_print.service
service ascii_email_and_print start
