#!/bin/bash

cat notice.ppm | stdbuf -o64k pnmscale -xysize 128 128 | socat -b64000 STDIO UDP-SENDTO:192.168.86.16:1337
echo "Notification Displayed.."


