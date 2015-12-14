#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com timehome@corp.globo.com
# Copyright (c) 2015 Wikimedia Foundation

# TIFF engine

from wikimedia_thumbor_base_engine import BaseWikimediaEngine


BaseWikimediaEngine.add_format(
    'image/tiff',
    '.tiff',
    lambda buffer: buffer.startswith('II*\x00') or buffer.startswith('MM\x00*')
)


class Engine(BaseWikimediaEngine):
    def should_run(self, extension, buffer):
        return extension == '.tiff'

    def create_image(self, buffer):
        self.tiff_buffer = buffer
        img = super(Engine, self).create_image(buffer)

        try:
            page = self.context.request.page
            img.seek(page - 1)
        except (AttributeError, EOFError):
            page = 1
            img.seek(0)

        self.extension = '.jpg'

        return img

    def read(self, extension=None, quality=None):
        if extension == '.tiff' and quality is None:
            # We're saving the source, let's save the TIFF
            return self.tiff_buffer

        # Beyond this point we're saving the JPG result
        if extension == '.tiff':
            extension = '.jpg'

        return super(Engine, self).read(extension, quality)
