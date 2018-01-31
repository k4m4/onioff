from collections import namedtuple

import requests
import stem.process

from utils.html import get_html_element

onion_status = namedtuple('onion_status', ['active', 'title'])


class Tor:
    def __init__(self, socks_port='7000', config=None):
        self._tor_process = None
        self._proxies = None

        self.socks_port = socks_port

        if not config or not isinstance(config, dict):
            self.config = {
                'SocksPort': str(self.socks_port),
            }
        else:
            config['SocksPort'] = socks_port
            self.config = config

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        self.disconnect()

    def connect(self):
        def print_bootstrap_lines(line):
            if "Bootstrapped " in line:
                print(line)

        self._tor_process = stem.process.launch_tor_with_config(
            config=self.config,
            init_msg_handler=print_bootstrap_lines,
        )

        tor_proxy = 'socks5h://localhost:{}'.format(self.socks_port)
        self._proxies = {'http': tor_proxy, 'https': tor_proxy}

    def disconnect(self):
        self._tor_process.kill()
        self._proxies = None

    def get(self, url, params=None):
        if not self._tor_process:
            self.connect()

        if not params or not isinstance(params, dict):
            params = {}

        return requests.get(url, params=params, proxies=self._proxies)

    def check_onion(self, onion):
        response = self.get(onion)
        status = response.status_code

        if not status == 200:
            active = False
            title = ''
        else:
            active = True
            title = get_html_element(response.content, './/title')

        return onion_status(active, title)
