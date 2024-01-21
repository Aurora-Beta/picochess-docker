FROM    debian:bullseye

WORKDIR /tmp

RUN     apt update
RUN     apt install -y git sox unzip wget python3-pip python3-venv libtcl8.6 telnet libglib2.0-dev stockfish

WORKDIR /opt
RUN     python3 -m venv /opt/picochess_venv

WORKDIR /opt/picochess
COPY    .   .

RUN     ln -sf /opt/picochess/etc/dgtpicom_$(uname -m) /opt/picochess/etc/dgtpicom
RUN     ln -sf /opt/picochess/etc/dgtpicom.$(uname -m).so /opt/picochess/etc/dgtpicom.so

RUN     bash -c "source /opt/picochess_venv/bin/activate && pip3 install wheel && pip3 install --upgrade -r requirements.txt"
RUN     touch picochess.ini

ADD     entrypoint.sh     /
RUN     chmod +x /entrypoint.sh

ENTRYPOINT [ "bash", "-c", "/entrypoint.sh" ]