#!/usr/bin/env python
import os
import sys
import time
import logging
import tempfile

# The camera interface library
import gphoto2 as gp

PHOTOS_FOLDER = os.environ.get('PHOTOS_FOLDER', '/tmp')
logger = logging.getLogger(__name__)


class CameraActions:

    def get_summary(self):
        context = gp.Context()
        camera = gp.Camera()
        camera.init(context)
        text = camera.get_summary(context)
        logging.debug(str(text))
        camera.exit(context)
        return str(text)

    def capture_image(self, *args, **kwargs):
        camera = gp.check_result(gp.gp_camera_new())
        gp.check_result(gp.gp_camera_init(camera))
        file_path = gp.check_result(gp.gp_camera_capture(camera, gp.GP_CAPTURE_IMAGE))
        logger.debug('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
        target = os.path.join(PHOTOS_FOLDER, "photo_{}.jpg".format(
                time.strftime("%Y%m%d-%H%M%S", time.localtime())))
        logger.debug('Copying image to {}'.format(target))
        camera_file = gp.check_result(gp.gp_camera_file_get(camera, file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL))
        gp.check_result(gp.gp_file_save(camera_file, target))
        gp.check_result(gp.gp_camera_exit(camera))
        with open(target, 'rb') as photo:
            photo_file = photo.read()
        return photo_file, target
