from collections import namedtuple

import requests
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError, HTTPError

onion_status = namedtuple('onion_status', ['active', 'title'])


class Tor:
    def __init__(self, ipcheck_url=None, tor_host='127.0.0.1',
                 tor_port='9050'):

        if ipcheck_url:
            self.ipcheck_url = ipcheck_url
        else:
            self.ipcheck_url = 'https://locate.now.sh/ip'

        self.tor_host = tor_host
        self.tor_port = tor_port
        self.pure_ip = self.get_ip(False)
        self.tor_outgoing_ip = None

    def get_ip(self, proxied=True):
        """ Get outgoing user's IP address using ipcheck_url service
        """
        proxies = {}
        if proxied:
            proxies = self.get_proxies()

        response = requests.get(self.ipcheck_url, proxies=proxies)

        status = response.status_code
        if status == 200:
            return response.text.replace('\n', '')
        else:
            msg = "Can't get the IP, status code = {}".format(status)
            raise HTTPError(msg)

    def get_proxies(self, remote_dns=True):
        protocol = 'socks5h'
        if not remote_dns:
            protocol = 'socks5'

        tor_proxy = '{}://{}:{}'.format(protocol, self.tor_host, self.tor_port)
        return {'http': tor_proxy, 'https': tor_proxy}

    def connect(self):
        """Check if user is connected to Tor network by comparing current IP address to
        the value of self.pure_ip

        """
        self.tor_outgoing_ip = self.get_ip()
        if self.pure_ip == self.tor_outgoing_ip:
            raise ConnectionError('Unsuccessful Tor connection')

    def get(self, url, params=None):
        if not self.tor_outgoing_ip:
            self.connect()

        if not params or not isinstance(params, dict):
            params = {}

        return requests.get(url, params=params, proxies=self.get_proxies())

    def check_onion(self, onion):
        response = self.get(onion)
        status = response.status_code

        if not status == 200:
            active = False
            title = ''
        else:
            active = True
            soup = BeautifulSoup(response.content, 'lxml')
            title = soup.title.string.encode('utf-8')

        return onion_status(active, title)
