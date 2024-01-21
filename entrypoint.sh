#!/bin/bash

ACTIVATE_SCRIPT=/opt/picochess_venv/bin/python3
PICOCHESS_DIR=/opt/picochess

cd $PICOCHESS_DIR

# Generate config-files

$ACTIVATE_SCRIPT $PICOCHESS_DIR/build/engines.py
$ACTIVATE_SCRIPT $PICOCHESS_DIR/build/books.py
$ACTIVATE_SCRIPT $PICOCHESS_DIR/build/voices.py

# Start

service dbus start
bluetoothd &

# Create empty log file if none exists
if [ ! -f logs/picochess.log ]; then
    touch logs/picochess.log
fi

tail -f logs/picochess.log&
$ACTIVATE_SCRIPT $PICOCHESS_DIR/picochess.py