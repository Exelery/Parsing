# Copyright (C) 2013 by Aivars Kalvans <aivars.kalvans@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import re
import random
import base64
import logging

proxy_regex = r'(\w+://)([^:]+?:.+@)?(.+)'
log = logging.getLogger('scrapy.proxies')


class Mode:
    RANDOMIZE_PROXY_EVERY_REQUESTS, RANDOMIZE_PROXY_ONCE, SET_CUSTOM_PROXY = range(3)


class RandomProxy(object):
    def __init__(self, settings):
        self.mode = settings.get('PROXY_MODE')
        self.proxy_list = settings.get('PROXY_LIST')
        self.chosen_proxy = ''

        if self.mode == Mode.RANDOMIZE_PROXY_EVERY_REQUESTS or self.mode == Mode.RANDOMIZE_PROXY_ONCE:
            if self.proxy_list is None:
                raise KeyError('PROXY_LIST setting is missing')
            self.proxies = {}
            fin = open(self.proxy_list)
            try:
                for line in fin.readlines():
                    #parts = re.match('(\w+://)([^:]+?:[^@]+?@)?(.+)', line.strip())
                    parts = re.match(proxy_regex, line.strip())
                    if not parts:
                        continue

                    # Cut trailing @
                    if parts.group(2):
                        user_pass = parts.group(2)[:-1]
                    else:
                        user_pass = ''

                    self.proxies[parts.group(1) + parts.group(3)] = user_pass
            finally:
                fin.close()
            if self.mode == Mode.RANDOMIZE_PROXY_ONCE:
                self.chosen_proxy = random.choice(list(self.proxies.keys()))
        elif self.mode == Mode.SET_CUSTOM_PROXY:
            custom_proxy = settings.get('CUSTOM_PROXY')
            self.proxies = {}
            #parts = re.match('(\w+://)([^:]+?:[^@]+?@)?(.+)', custom_proxy.strip())
            parts = re.match(proxy_regex, custom_proxy.strip())
            if not parts:
                raise ValueError('CUSTOM_PROXY is not well formatted')

            if parts.group(2):
                user_pass = parts.group(2)[:-1]
            else:
                user_pass = ''

            self.proxies[parts.group(1) + parts.group(3)] = user_pass
            self.chosen_proxy = parts.group(1) + parts.group(3)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        # Don't overwrite with a random one (server-side state for IP)
       # if 'proxy' in request.meta:
         #   if request.meta["exception"] is False:
          #      return
        if self.mode < 0:
            log.warning("Skipping Random Proxy selection(disabled)!")
            return
        if 'proxy' in request.meta or ('splash' in request.meta and 'proxy' in request.meta['splash']['args']):
            if request.meta.get("exception", False) is False:
                return

        request.meta["exception"] = False
        if len(self.proxies) == 0:
            raise ValueError('All proxies are unusable, cannot proceed')

        if self.mode == Mode.RANDOMIZE_PROXY_EVERY_REQUESTS:
            proxy_address = random.choice(list(self.proxies.keys()))
        else:
            proxy_address = self.chosen_proxy

        proxy_user_pass = self.proxies[proxy_address]

        #if proxy_user_pass:
        #    request.meta['proxy'] = proxy_address
        #    basic_auth = 'Basic ' + base64.b64encode(proxy_user_pass.encode()).decode()
         #   request.headers['Proxy-Authorization'] = basic_auth
       # else:
         #   log.debug('Proxy user pass not found')
        self.add_scrapy_proxy(request, proxy_address, proxy_user_pass)

        log.debug('Using proxy <%s>, %d proxies left' % (
                proxy_address, len(self.proxies)))

    def process_exception(self, request, exception, spider):
     #   if 'proxy' not in request.meta:
        if self.mode < 0 or ('proxy' not in request.meta and not (
             'splash' in request.meta and 'proxy' in request.meta['splash']['args'])):
            return
        if self.mode == Mode.RANDOMIZE_PROXY_EVERY_REQUESTS or self.mode == Mode.RANDOMIZE_PROXY_ONCE:
           # proxy = request.meta['proxy']
            if ('splash' in request.meta and 'proxy' in request.meta['splash']['args']):
               parts = re.match(proxy_regex, request.meta['splash']['args']['proxy'].strip())
               proxy = parts.group(1) + parts.group(3)
            else:
               proxy = request.meta['proxy']
            try:
                del self.proxies[proxy]
            except KeyError:
                pass
            request.meta["exception"] = True
            if self.mode == Mode.RANDOMIZE_PROXY_ONCE:
                self.chosen_proxy = random.choice(list(self.proxies.keys()))
            log.info('Removing failed proxy <%s>, %d proxies left' % (
                proxy, len(self.proxies)))

    def add_scrapy_proxy(self, request, address, user_pass=None):

        if ('splash' in request.meta):
            # In case there is splash, just forward the proxy to it
            parts = re.match('(\w+://)([\w\W]+)', address.strip())
            request.meta['splash']['args']['proxy'] = parts.group(1) + (
                (user_pass + '@') if len(user_pass) > 0 else '') + parts.group(2)
        else:
            request.meta['proxy'] = address
            if user_pass:
                basic_auth = 'Basic ' + base64.b64encode(user_pass.encode()).decode()
                request.headers['Proxy-Authorization'] = basic_auth
