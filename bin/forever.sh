#!/bin/sh
#/usr/bin/forever.sh

while true; do
    $@
    echo "Server  crashed with exit code $?. Respawing.." >&2
    sleep 1
done