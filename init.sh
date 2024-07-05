#!/bin/sh

export TERM=xterm # docker run -t hack
while true; do
    python3 main.py
    sleep ${INTERVAL:-60}
done