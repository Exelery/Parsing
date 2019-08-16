# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import re
from scrapy.pipelines.images import ImagesPipeline
import ntpath
import urllib.parse
import os


class TortyPipeline(object):
    def process_item(self, item, spider):
        return item


class TortyImgPipeline(ImagesPipeline):
    CONVERTED_ORIGINAL = re.compile('^full/[0-9,a-f]+.jpg$')
    counter = 0

    # name information coming from the spider, in each item
    # add this information to Requests() for individual images downloads
    # through "meta" dict
    def get_media_requests(self, item, info):
        # print("get_media_requests")
        if item['image_urls'] is not [None]:
            return [scrapy.Request(x, meta={'item': item})
                    for x in item.get('image_urls', [])]

    # this is where the image is extracted from the HTTP response
    # def get_images(self, response, request, info):
    #     print("get_images")
    #
    #     for key, image, buf, in super(StoreImgPipeline, self).get_images(response, request, info):
    #         if self.CONVERTED_ORIGINAL.match(key):
    #             key = self.change_filename(key, response)
    #         yield key, image, buf
    #
    # def change_filename(self, key, response):
    #     return "full/%s.jpg" % response.meta['image_name'][0]

    def file_path(self, request, response=None, info=None):
        filename = ntpath.basename(request.url)
        filename = urllib.parse.unquote(filename)
        filename, file_extension = os.path.splitext(filename)
        item = request.meta['item']
        self.counter = item['counter']
        filename = 'torty-{}{}'.format('{:06}'.format(self.counter), file_extension)
        return filename

    # def file_path(self, request, response=None, info=None):
    #     filename = ntpath.basename(request.url)
    #     return "{}/{}".format(request.meta['sku'], filename)

    def decorate_url(self, urla):
        return '["{}"]'.format(urla)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        # for k, img in enumerate(image_paths):
        #     filename, file_extension = os.path.splitext('img')
        #     self.counter = self.counter + 1
        #     image_paths[k] = 'torty-%.%'.format(self.counter, file_extension)
        item['image_name'] = [ntpath.basename(image_path) for image_path in image_paths]
        item['images'] = image_paths
        return item
