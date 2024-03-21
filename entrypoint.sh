#!/bin/bash

PICOCHESS_DIR=/opt/picochess
INPUT_DIR=/config

echo "============================"
echo " ENTRYPOINT-SCRIPT STARTING"
echo "============================"

cd $PICOCHESS_DIR

# Streaming the content of the mounted config-file into the
# picochess.ini file in the directory to make it readable for the software

if [ -f "$INPUT_DIR/picochess.ini" ]; then
    cat $INPUT_DIR/picochess.ini > $PICOCHESS_DIR/picochess.ini
else
    echo "-> No file $INPUT_DIR/picochess.ini provided!"
    echo "-> Please copy the picochess.ini.example to picochess.ini and edit it to your liking!"
    echo "-> Exiting now..."
    exit -1
fi

echo "-> Generating config files now ..."

# Generate config-files
$PICOCHESS_DIR/build/engines.py
$PICOCHESS_DIR/build/books.py
$PICOCHESS_DIR/build/voices.py

echo "-> Generating of config files done."

dgtpi_config_file_line=$(grep -e "dgtpi" picochess.ini | tr '[:upper:]' '[:lower:]')

echo "-> Starting Bluetooth servies now..."

# Start Bluetooth
service dbus start
bluetoothd &
echo "-> Printing status of Bluetooth now ..."
rfkill list bluetooth

# Create empty log file if none exists
if [ ! -f logs/picochess.log ]; then
    echo "-> Creating empty logfile for picochess ..."
    touch logs/picochess.log
fi

echo "-> Starting GamesDatabase gamesdb..."
# Start gamesdb
cd $PICOCHESS_DIR/gamesdb
./tcscid get_games.tcl --server 7778&

echo "-> Starting Openingbook Server..."
# Start Openingbook Server
cd $PICOCHESS_DIR/openingbookserver
python3 obooksrv.py --host 0.0.0.0 --port 7777 --book opening.data&

echo "-> Starting DGT-Communcation service dgtpi..."
# Start dgtpi Service
# cd $PICOCHESS_DIR/etc
# ./dgtpicom "  DGT  P|  " 1

echo "-> Starting picochess in foreground now."
echo "-> To stop this container, press key combination <CTRL>+<c>"
# Start picochess
cd $PICOCHESS_DIR
tail -f logs/picochess.log&
$PICOCHESS_DIR/picochess.py


# Kill Them All ...
/usr/bin/pkill -f obooksrv
/usr/bin/pkill -f tcscid
