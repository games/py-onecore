# coding=utf-8
# funnylab.org
# Date: 11-10-11
# Time: 上午12:16

__author__ = 'valorzhong'

sig_gif = b'GIF'
sig_jpg = b'\xff\xd8\xff'
sig_png = b"\211PNG\r\n\032\n"

class ImageHelper(object):

    @staticmethod
    def get_image_type(data):
        if data[:3] == sig_gif:
            return 'gif'
        elif data[:3] == sig_jpg:
            return 'jpg'
        elif data[:8] == sig_png:
            return 'png'
        else:
            return None