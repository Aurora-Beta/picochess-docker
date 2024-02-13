# BUILD DGTPICOM
FROM    debian:bookworm AS COMPILE

RUN     apt update \
     && apt install -y build-essential tk-dev tcl-dev tk tcl cmake git

# Build dgtpi
WORKDIR /compile/dgtpi
COPY    dgtpi    .
RUN     make

# Build tcscid
WORKDIR /compile/scidvspc
COPY    scidvspc    .
RUN     ./configure TCL_INCLUDE="-I/usr/include/tcl8.6" TCL_VERSION="8.6" && make

# Build obooksrv
WORKDIR /compile/obooksrv
COPY    obooksrv    .
RUN     cmake . && make && make unittests

#
# PICOCHESS IMAGE
#
FROM    debian:bookworm

WORKDIR /tmp

RUN     apt update
RUN     apt install -y \
        git sox unzip wget python3-poetry python-is-python3 \
        libtcl8.6 telnet libglib2.0-dev stockfish \
        sudo bluez bluetooth procps libcap2-bin rfkill

# Setup the virtual environment by poetry
WORKDIR /opt/picochess
COPY    poetry.toml pyproject.toml ./
RUN     poetry install

# Setup the Image to use the venv created by poetry
ENV     PATH           /opt/picochess/.venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV     POETRY_ACTIVE  1
ENV     VIRTUAL_ENV    /opt/picochess/.venv

# Copy the compiled dgtpip program from the earlier stage
COPY    --from=COMPILE /compile/dgtpi/dgtpicom     /opt/picochess/etc/dgtpicom
COPY    --from=COMPILE /compile/dgtpi/dgtpicom.so  /opt/picochess/etc/dgtpicom.so

# Copy the compiled tcscid program from the earlier stage
COPY    --from=COMPILE /compile/scidvspc/tcscid    /opt/picochess/gamesdb/tcscid

# Copy the compiled tcscid program from the earlier stage
COPY    --from=COMPILE /compile/obooksrv/obooksrv  /opt/picochess/obooksrv/

# Copy the rest of the repo
COPY    . .

# Setup the entrypoint script
WORKDIR /opt/picochess
COPY    entrypoint.sh     /
RUN     chmod +x /entrypoint.sh picochess.py

# MANUALLY PATCHING
RUN     sed -i "s/class OptionMap(collections.MutableMapping)/class OptionMap(collections.abc.MutableMapping)/g"     /opt/picochess/.venv/lib/python3.11/site-packages/chess/engine.py
RUN     sed -i "s/import collections/import collections.abc/g"                                                       /opt/picochess/.venv/lib/python3.11/site-packages/chess/engine.py
RUN     sed -i "s/collections.MutableMapping/collections.abc.MutableMapping/g"                                       /opt/picochess/.venv/lib/python3.11/site-packages/chess/pgn.py
RUN     sed -i "s/import collections/import collections.abc/g"                                                       /opt/picochess/.venv/lib/python3.11/site-packages/chess/pgn.py
RUN     sed -i "s/collections.MutableMapping/collections.abc.MutableMapping/g"                                       /opt/picochess/.venv/lib/python3.11/site-packages/tornado/httputil.py
RUN     sed -i "s/import collections/import collections.abc/g"                                                       /opt/picochess/.venv/lib/python3.11/site-packages/tornado/httputil.py
RUN     setcap 'cap_net_raw,cap_net_admin+eip' /opt/picochess/.venv/lib/python3.11/site-packages/bluepy/bluepy-helper

WORKDIR /opt/picochess/obooksrv
RUN     ln -s testdata/opening.data .

ENTRYPOINT [ "bash", "-c", "/entrypoint.sh" ]
