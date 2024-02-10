# PicoChess

Stand alone chess computer based on [Raspberry Pi](http://www.raspberrypi.org/). Supports DGT electronic clocks and many electronic chess boards.

## Requirements

- Raspberry Pi 2 or newer
- RaspiOS Bullseye installed and configured

Picochess can run on AMD64/x86 and other platforms, that run Python3.11.

## Installation

Firstly, you have to clone this repository:

```sh
# Clone the repository including the submodules for the first time:
# Download size is about 500 Megabytes!
# Size on disk with all submodules is about 1.1GB!
git clone --recurse-submodules https://github.com/Aurora-Beta/picochess-docker.git

# Update the existing clone of this repo
cd <Local path to this cloned repository>
git pull
git submodule update --init --recursive
```

### Native on Raspberry Pi
Run this command as root on your Raspberry Pi:

```sh
curl -sSL https://raw.githubusercontent.com/ghislainbourgeois/picochess/master/install-picochess.sh | bash
```

If you wish to use engines supported by the Mame emulator, you will also need
to set the GPU Memory Split to 64 Mb minimum.

Once the installation is complete, you can copy the file
`/opt/picochess/picochess.ini.example` to `/opt/picochess/picochess.ini` and
edit it for your specific situation.

### Native on other platforms

The required Python packages and the management of the environment is
done by `poetry`, so you need to install it before.

```sh
# Install poetry and wheel via pip
pip3 install wheel poetry

# Alternativley, if you use Debian 12 "Bookworm",
# you can install by invoking the package manager apt:
apt update && apt install -y python3-poetry
```

Poetry will setup a virtual environment in the folder `.venv` of this repository.
To start the installation of the required packages, execute the following command:

```sh
# Let poetry setup the virtual environment in ./.venv
# and install the packages.
poetry install
```

To start picochess locally, run the following commands:

```sh
# Generating the .ini-files for the Engines, Books and Voices:
poetry run python ./build/engines.py
poetry run python ./build/books.py
poetry run python ./build/voices.py


# Create empty log file if none exists
if [ ! -f logs/picochess.log ]; then
    touch logs/picochess.log
fi


# Start gamesdb in the background
cd $PICOCHESS_DIR/gamesdb
./tcscid get_games.tcl --server 7778&

# Start Openingbook Server in the background
cd $PICOCHESS_DIR/obooksrv/
./obooksrv&

# Optionally: Start dgtpi Service
cd $PICOCHESS_DIR/etc
./dgtpicom "  DGT  P|  " 1

# Start picochess in foreground
$PICOCHESS_DIR/picochess.py
```

### Docker / Container for all supported platforms

Things are a lot simpler using `docker-compose`,
so it is highly recommended to install it before:
<https://docs.docker.com/compose/install/>

With `docker-compose` or the plugin version `docker compose` installed,
you can build and use the image as follows:

```sh
# Clone the repository including the submodules for the first time:
git clone --recurse-submodules https://github.com/Aurora-Beta/picochess-docker.git

# Build the image:
docker-compose build

# Start the stack with the built image:
docker-compose up -d

# Stop the stack:
docker-compose stop

# Remove the created container and network from the system:
docker-compose down
```

## Note

This repository does not contain all engines, books or voice samples the
community has built over the years. Unfortunately, a lot of those files cannot
be easily hosted in this repository. You can find additional content for your
picochess installation in the [Picochess Google Group](https://groups.google.com/g/picochess).
