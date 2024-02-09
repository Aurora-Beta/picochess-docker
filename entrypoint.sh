#!/bin/bash

PICOCHESS_DIR=/opt/picochess
INPUT_DIR=/config

cd $PICOCHESS_DIR

# Streaming the content of the mounted config-file into the
# picochess.ini file in the directory to make it readable for the software

if [ -f "$INPUT_DIR/picochess.ini" ]; then
    cat $INPUT_DIR/picochess.ini > $PICOCHESS_DIR/picochess.ini
else
    echo "No file $INPUT_DIR/picochess.ini provided!"
    echo "Exiting now."
    exit -1
fi

# Generate config-files
$PICOCHESS_DIR/build/engines.py
$PICOCHESS_DIR/build/books.py
$PICOCHESS_DIR/build/voices.py


dgtpi_config_file_line=$(grep -e "dgtpi" picochess.ini | tr '[:upper:]' '[:lower:]')


# Start Bluetooth
service dbus start
bluetoothd &

# Create empty log file if none exists
if [ ! -f logs/picochess.log ]; then
    touch logs/picochess.log
fi


# Start gamesdb
cd $PICOCHESS_DIR/gamesdb
./tcscid get_games.tcl --server 7778&

# Start Openingbook Server
cd $PICOCHESS_DIR/obooksrv/
./obooksrv&

# Start dgtpi Service
cd $PICOCHESS_DIR/etc
./dgtpicom "  DGT  P|  " 1

# Start picochess
cd $PICOCHESS_DIR
tail -f logs/picochess.log&
$PICOCHESS_DIR/picochess.py


# Kill Them All ...
/usr/bin/pkill -f obooksrv
/usr/bin/pkill -f tcscid
