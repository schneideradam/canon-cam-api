#!/usr/bin/env python

import logging
import os
import sys
import time

import gphoto2 as gp

logging.basicConfig(level=logging.DEBUG)

PHOTOS_FOLDER = os.environ.get('PHOTOS_FOLDER', '/tmp')

class CameraActions:

    def get_summary(self):
        context = gp.Context()
        camera = gp.Camera()
        camera.init(context)
        text = camera.get_summary(context)
        logging.debug(str(text))
        camera.exit(context)

    def capture_image(self, *args, **kwargs):
        camera = gp.check_result(gp.gp_camera_new())
        gp.check_result(gp.gp_camera_init(camera))
        file_path = gp.check_result(gp.gp_camera_capture(camera, gp.GP_CAPTURE_IMAGE))
        logging.debug('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
        target = os.path.join(PHOTOS_FOLDER, "photo_{}.jpg".format(
                time.strftime("%Y%m%d-%H%M%S", time.localtime())))
        logging.debug('Copying image to {}'.format(target))
        camera_file = gp.check_result(gp.gp_camera_file_get(camera, file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL))
        gp.check_result(gp.gp_file_save(camera_file, target))
        gp.check_result(gp.gp_camera_exit(camera))
