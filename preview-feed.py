#!/usr/bin/env python

from __future__ import print_function

import logging
import os
import sys
import time
import platform
from subprocess import Popen
from sys import stdout, stdin, stderr

def handle(commands):
    proc_list = []
    for command in commands:
        proc = Popen(command, shell=True, stdin=stdin, stdout=stdout, stderr=stderr)
        proc_list.append(proc)
        time.sleep(3)
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        for proc in proc_list:
            os.kill(proc.pid, signal.SIGKILL)

def create_feed():
    cmds = ['gphoto2 --stdout --capture-movie | gst-launch-1.0 fdsrc ! \
                 decodebin3 name=dec ! queue ! videoconvert ! \
                 v4l2sink device=/dev/video0']
    if "Darwin" in platform.platform():
        cmds.append('/Applications/VLC.app/Contents/MacOS/VLC')
    else:
        cmds.append('cvlc v4l2:///dev/video0')

    if not os.path.exists('/dev/video0'):
        logging.info('Adding virtual device')
        cmds.insert(0, 'modprobe v4l2loopback')
    return cmds



def main():
    logging.basicConfig(
        format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)
    handle(create_feed())
    return True

if __name__ == "__main__":
    sys.exit(main())
