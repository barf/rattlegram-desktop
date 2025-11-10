#!/bin/sh
#
# simple rattlegram send script
# Stuart MacIntosh ZL3TUX <stuart@macintosh.nz>
#

export XDG_RUNTIME_DIR=/run/user/1000

TONEGEN=/home/barf/radio/tonegen.py

VOLUME=100
CHANNELS=1
SAMPLE_RATE=48000
BITS=16
# CFO=1300
# CALLSIGN='ZL3TUX'

# create if not exists?
WAVOUT=/home/barf/radio/wavout 

MESSAGE=$*
echo $MESSAGE
# args=("$@")

# clean up
rm -vf $WAVOUT/*

# the borken ass rattlegram-cli barf fork
ENCODE=/home/barf/radio/rattlegram-cli/encode
echo $ENCODE "$MESSAGE" $CALLSIGN 4 $CFO $SAMPLE_RATE $BITS 0 4 $WAVOUT/out.wav
$ENCODE "$MESSAGE" $CALLSIGN 4 $CFO $SAMPLE_RATE $BITS 0 4 $WAVOUT/out.wav

# modem-short version
# usage: ./encode OUTPUT SAMPLE_RATE BITS CHANNELS INPUT [OFFSET] [CALLSIGN]
# ENCODE=/home/barf/radio/modem-short/encode
# echo $ENCODE /home/barf/radio/out.wav $SAMPLE_RATE $BITS $CHANNELS "$MESSAGE" $CFO $CALLSIGN
# $ENCODE /home/barf/radio/out.wav $SAMPLE_RATE $BITS $CHANNELS "$MESSAGE" $CFO $CALLSIGN

# generate warmup/VOX delay tone
$TONEGEN -s $SAMPLE_RATE -d 0.5 -o $WAVOUT/tone_0s5.f32 $CFO
sox $WAVOUT/tone_0s5.f32 -b 16 -e signed-integer $WAVOUT/tone_0s5.wav

# generate end-of-message tone
$TONEGEN -s $SAMPLE_RATE -d 0.10 -o $WAVOUT/tone_0s10.f32 $CFO
sox $WAVOUT/tone_0s10.f32 -b 16 -e signed-integer $WAVOUT/tone_0s10.wav

# assemble end of message tone
sox -n -b $BITS -r $SAMPLE_RATE $WAVOUT/silence_0s10.wav trim 0.0 0.10
sox -n -b $BITS -r $SAMPLE_RATE $WAVOUT/silence_1s.wav trim 0.0 1.0
sox $WAVOUT/tone_0s10.wav $WAVOUT/silence_0s10.wav $WAVOUT/tone_0s10.wav $WAVOUT/silence_1s.wav $WAVOUT/tone_end.wav

# assemble and play
ffmpeg -loglevel quiet -y -i $WAVOUT/out.wav -ac 1 $WAVOUT/out_mono.wav 					# downmix to mono
sox $WAVOUT/out_mono.wav $WAVOUT/out_trim.wav silence 1 0.0 0.0% -1 0 1%					# trim silence(?)
sox $WAVOUT/tone_0s5.wav $WAVOUT/out_trim.wav $WAVOUT/tone_end.wav $WAVOUT/msg.wav 			# prepend tone and append tone
# sox $WAVOUT/1700_start.wav $WAVOUT/out_trim.wav $WAVOUT/1700_end.wav $WAVOUT/msg.wav 		# prepend tone and append tone

#
#aplay /tmp/msg.wav
# morseALSA -w 13 -v 1.0 RIB BIT
mpv --volume=$VOLUME $WAVOUT/msg.wav
