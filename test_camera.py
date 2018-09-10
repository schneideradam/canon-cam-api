#!/usr/bin/env python
import sys

from camera_controller import CameraActions

def main(*args):
    cam = CameraActions()
    try:
        print(cam.get_summary())
    except Exception as e:
        print(str(e))
    cam.capture_image()

if __name__ == '__main__':
    main()
