#!/usr/bin/env python
import sys

from camera_controller import CameraActions

def main(*args):
    cam = CameraActions()
    try:
        print(cam.get_summary())
    except Exception as e:
        print(str(e))
    photo = cam.capture_image()
    with open('test_image.jpg', 'wb') as img:
        img.write(photo)

if __name__ == '__main__':
    main()
