#!/bin/sh
#
# https://github.com/aicodix/modem/issues/16
#
# while true ; do arecord -c 1 -f S16_LE -r 8000 - | ./decode - - ; done
#

AUDIODEVICE=snd/0 # openbsd
DECODE=/home/barf/radio/modem-short/decode

while true
do
	# T=`date +%s`
	#aucat -f $AUDIODEVICE -o - | $DECODE - -;
	#cat out/$T.dat
	echo 'Starting decoder...'
	date
	arecord -c 1 -f S16_LE -r 8000 - | $DECODE - -
	echo
done
