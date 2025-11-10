#!/bin/sh
#
# args=("$@")
#

export XDG_RUNTIME_DIR=/run/user/1000

WORKDIR="/home/barf/radio/"
# CFO=1700
# CALLSIGN="1984NZ"
#CALLSIGN="NZCH1984"
# CALLSIGN="ZL3TUX"
RATE=8000
BITS=16
CHANNELS=1
MODE=0 	# 0=PING
VOLUME=100

rm -f /home/barf/radio/out.wav /home/barf/radio/msg.wav /home/barf/radio/out_trim.wav /home/barf/radio/out_mono.wav

# modem-next:
# usage: encode OUTPUT RATE BITS CHANNELS OFFSET MODE CALLSIGN INPUT..
# ./encode encoded.wav 8000 16 1 1500 23 CALLSIGN uncoded.dat
ENCODE=/home/barf/radio/modem-next/encode
$ENCODE /home/barf/radio/out.wav $RATE $BITS $CHANNELS $CFO $MODE $CALLSIGN

# assemble and play
ffmpeg -loglevel quiet -y -i /home/barf/radio/out.wav -ac 1 /home/barf/radio/out_mono.wav
sox /home/barf/radio/out_mono.wav /home/barf/radio/out_trim.wav silence 1 0.0 0.0% -1 0 1%
sox /home/barf/radio/1700_start.wav /home/barf/radio/out_trim.wav /home/barf/radio/1700_end.wav /home/barf/radio/msg.wav
# sox /home/barf/radio/1700_start.wav /home/barf/radio/out_trim.wav /home/barf/radio/msg.wav
#aplay /tmp/msg.wav
mpv --volume=$VOLUME /home/barf/radio/msg.wav
