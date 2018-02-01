from collections import namedtuple
from concurrent.futures import as_completed

import requests
import stem.process
from requests_futures.sessions import FuturesSession
from tqdm import tqdm

from utils.html import get_html_element

onion_status = namedtuple('onion_status', ['url', 'status', 'active', 'title'])


class Tor(object):
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

    def session(self, async=True, max_workers=5):
        if not self._tor_process:
            self.connect()

        if async:
            session = FuturesSession(max_workers=max_workers)
        else:
            session = requests.Session()

        session.proxies = self._proxies
        return session


class Onion(Tor):
    def __init__(self, **kwargs):
        super(Onion, self).__init__(**kwargs)

    def check_onions(self, onions, timeout=20, workers=5, progress=True):
        if not isinstance(onions, list):
            if isinstance(onions, str):
                onions = [onions]
            else:
                raise ValueError('Onions should be an instace of list object')

        session = self.session(async=True, max_workers=workers)
        futures = [session.get(url, timeout=timeout) for url in onions]

        results = set()
        iterable = as_completed(futures)
        if progress:
            iterable = tqdm(
                iterable, total=len(onions), desc='Processing', ncols=100)

        for item in iterable:
            try:
                response = item.result()
                status = response.status_code
            except requests.exceptions.ConnectTimeout as e:
                exp_obj = onion_status(e.request.url, None, False, 'Timeout')
                results.add(exp_obj)
                continue
            except requests.exceptions.ConnectionError as e:
                # Onion URL is invalid and not reachable
                exp_obj = onion_status(e.request.url, None, False, 'Not Found')
                results.add(exp_obj)
                continue

            # Some server is responding, but with an error code
            if not status == 200:
                active = False
                title = ''
            else:
                active = True
                title = get_html_element(response.content, './/title').strip()

            results.add(onion_status(response.url, status, active, title))

        return results
