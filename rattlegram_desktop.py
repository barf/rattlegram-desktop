#!/usr/bin/env python3
#
# Rattlegram Desktop
# Copyright 2025 
# Stuart MacIntosh ZL3TUX <stuart@macintosh.nz>
#

import argparse
import json
import os
import sys
import subprocess
import zmq
import pickle
import time
import threading
import binascii
import queue

from PyQt6 import QtCore, QtGui, QtWidgets

from rattlegram_desktop_config import RattlegramDesktopConfig
from rattlegram_desktop_main import Ui_MainWindow

import tonegen

from IPython import embed
from pprint import pprint

global rx_enabled, tx_enabled
rx_enabled = True
tx_enabled = True

import pyaudio
import wave
import struct
import tempfile

# def enqueue_output(proc, queue):
#     queue.put(proc.communicate())
#     # queue.put(stdout.read())
#     # for line in iter(stdout.readline, b''):
#     # for line in iter(stdout.readlines, b''):
#         # queue.put(line)
#     # out.close()
#     # process.wait()

# def receiver():
#     print('rx thread')
#     config = RattlegramDesktopConfig()

#     # Audio parameters
#     FORMAT = pyaudio.paInt16
#     CHANNELS = 1
#     RATE = 8000
#     CHUNK = 1024

#     with open('header.wav', 'rb') as header_wav_file:
#         wave_header = header_wav_file.read()
#     # print(wave_header)

#     audio = pyaudio.PyAudio()
#     # Start recording
#     stream = audio.open(format=FORMAT, channels=CHANNELS,
#                     rate=RATE, input=True,
#                     frames_per_buffer=CHUNK)
#     print("audio.open()...")
#     frames = list()
#     frames.append(wave_header)

#     try:
#         rx_process = subprocess.Popen(
#             [config.get_value('decode'), "-", "-"],
#             stdin=subprocess.PIPE,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=False,
#             pipesize=1024,
#             bufsize=0,
#             env=os.environ,
#             shell=False
#         )
#     except subprocess.CalledProcessError as e:
#         print(f"Error executing command: {e}")
#         print(f"Stderr: {e.stderr}")
#         embed()
#         sys.exit(1)

#     # rx_process.stdin.flush()
#     if rx_process.returncode:
#         print('rx_process.returncode: %s' % rx_process.returncode)
#         embed()

#     q = queue.Queue()
#     # t = threading.Thread(target=enqueue_output, args=(rx_process.stdout, q))
#     t = threading.Thread(target=enqueue_output, args=(rx_process, q))
#     t.daemon = True # thread dies with the program
#     t.start()
    
#     # print(rx_process)
#     # print('dir(rx_process): ' % dir(rx_process))
#     # time.sleep(4)
#     # embed()
#     # output = rx_process.stdout.readline()
#     # print(f"rx_process output: {output.strip()}")

#     FRAME_PERIOD = 5
#     while rx_enabled:
#         # stderr = rx_process.stderr.readline()
#         # print('rx_process.stderr: %s' % stderr)
#         # stdout = rx_process.stdout.readline()
#         # print('rx_process.stdout: %s' % stdout)

#         for i in range(0, int(RATE / CHUNK * FRAME_PERIOD)):
#             data = stream.read(CHUNK)
#             frames.append(data)

#         #feed frames[] to the subprocess stdin
#         print('got %s frames (%s seconds)' % (len(frames), FRAME_PERIOD))
#         print('frame[0] len: %s' % len(frames[0]))
#         print('frame[38] len: %s' % len(frames[38]))

#         pipe_data = b''.join(frames)
        
#         if rx_process.returncode:
#             print('rx_process.returncode: %s' % rx_process.returncode)
#             embed()
#             if rx_process.returncode > 0:
#                 sys.exit(rx_process.returncode)

#         try:
#             # send frames to decoder subprocess stdin
#             rx_process.stdin.write(pipe_data)
#             print('WAV stream: %s ...' % binascii.hexlify(pipe_data[0:40]).decode('ascii'))
#             rx_process.stdin.flush() # Ensure the data is sent
#             print('rx_process.stdin.flush()')
#         except Exception as e:
#             # [Errno 32] Broken pipe ?
#             print(e)
#             embed()
#             sys.exit(1)

#         # try:
#         #     # Read output
#         #     output = rx_process.stdout.readline() # blocks?
#         #     print('rx_process.stdout: %s' % output)
#         # except Exception as e:
#         #     print(e)
#         #     embed()
#         #     sys.exit(1)

#         # stderr = rx_process.stderr.read()
#         # print('rx_process.stderr: %s' % stderr)
#         # stdout = rx_process.stdout.readline()
#         # print('rx_process.stdout: %s' % stdout)

#         # output = rx_process.stdout.readline()
#         # for line in output:
#         #     print('decoder output: %s' % line)

#         # print(f"decoder output: {output.strip()}")

#         # print('rx_process.stdout.readall()')
#         # testout = rx_process.stdout.readall()

#         # read line without blocking
#         try:
#             rx_process.stdout.flush()
#             line = q.get_nowait() # or q.get(timeout=.1)
#         except queue.Empty:
#             print('rx_process.stdout empty')
#         else: # got outpu
#             print('rx_process.stdout: %s' % line)
#             # rx_process.wait()

#         frames = [] # empty the frame ring buffer, was sent to decoder

#     rx_process.stdin.close() # Close stdin when no more input is expected
#     stdout_data, stderr_data = rx_process.communicate() # any remaining stdout

#     stream.stop_stream()
#     stream.close()
#     audio.terminate()

#     print("receiver thread finished")

#     # TODO: receiver thread goes here, stdin is audio frames 
#     # arecord -c 1 -f S16_LE -r 8000 - | $DECODE - -

#     # context = zmq.Context()
#     # socket = context.socket(zmq.REQ)
#     # socket.setsockopt(zmq.SNDTIMEO, 1000)
#     # socket.setsockopt(zmq.RCVTIMEO, 2000)
#     # socket.setsockopt(zmq.CONNECT_TIMEOUT, 2000)
#     # socket.connect("tcp://localhost:5555")
#     # socket.send(b"Hello")
#     # message = socket.recv()
#     # print("Received reply %s [ %s ]" % (request, message))

#     # while rx_enabled:
#     #     print('rx thread idle')
#     #     time.sleep(5)

# def transmitter():
#     print('tx thread')
#     # TODO: transmitter thread. socket server calls subprocess
#     context = zmq.Context()
#     socket = context.socket(zmq.REP)
#     socket.bind("tcp://*:5555")
#     while tx_enabled:
#         #  Wait for next request from client
#         recv = socket.recv()
#         rx = pickle.loads(recv)
#         print('tx thread got: %s' % rx)

#         callsign, cfo, message = rx

#         #  Do 'work'
#         _env = os.environ
#         _env['CALLSIGN'] = callsign
#         _env['CFO'] = str(cfo)

#         p0 = subprocess.run(['/home/barf/radio/rattlegram_tx.sh', message], env=_env, capture_output=True)
        
#         if p0.returncode > 0:
#             print(p0)

#         # Send reply back to client
#         socket.send(b"Sent")
#     socket.close()
#     print('tx thread finished')

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
                prog=sys.argv[0],
                description='Rattlegram Desktop GUI by Stuart MacIntosh ZL3TUX <stuart@macintosh.nz>',
                epilog='')

    # parser.add_argument('-f', default=1500, type=int, help='carrier frequency (1500 Hz)')
    # parser.add_argument('-o', '--output', default='out.f32', help='output WAV file (out.f32)')

    # parser.add_argument('-s', '--sample_rate', type=float, default=48000, help='sample rate (48000)')
    # parser.add_argument('-d', '--duration', default=1.0, help='duration (1.0)')
    # parser.add_argument('-a', '--amplitude', default=0.5, help='signal amplitude (0.5)')
    
    args = parser.parse_args()

    # config = RattlegramDesktopConfig()

    # rx_thread = threading.Thread(target=receiver)
    # tx_thread = threading.Thread(target=transmitter)
    # rx_thread.start()
    # tx_thread.start()

    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    # sys.exit(app.exec())
    app_retval = app.exec()
    print('app.exec() finished')

    # rx_enabled = False
    # rx_thread.join()

    # tx_enabled = False
    # tx_thread.join()

    sys.exit(app_retval)