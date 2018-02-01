#!/usr/bin/env python
# -.- coding: utf-8 -.-
# onioff.py
"""
Copyright (C) 2016-2018 Nikolaos Kamarinakis (nikolaskam@gmail.com)
See License at nikolaskama.me (https://nikolaskama.me/onioffproject)
"""

import csv
import json
import os

import click
from logzero import LogFormatter, logger, setup_default_logger

from onioff import VERSION
from utils.tor import Onion

log_format = '%(color)s[%(levelname)1.1s] %(message)s%(end_color)s'
setup_default_logger(formatter=LogFormatter(fmt=log_format))

TIMEOUT_DEFAULT = 20
WORKERS_DEFAULT = 5
SOCKS_PORT_DEFAULT = 7000


def print_banner():
    banner_vars = dict(
        blue='\33[94m',
        red='\033[91m',
        white='\33[97m',
        yellow='\33[93m',
        green='\033[32m',
        end='\033[0m',
        version=VERSION)

    print("""{red}
 ██████╗ ███╗   ██╗██╗ ██████╗ ███████╗███████╗
██╔═══██╗████╗  ██║██║██╔═══██╗██╔════╝██╔════╝
██║   ██║██╔██╗ ██║██║██║   ██║█████╗  █████╗
██║   ██║██║╚██╗██║██║██║   ██║██╔══╝  ██╔══╝
╚██████╔╝██║ ╚████║██║╚██████╔╝██║     ██║
 ╚═════╝ ╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═╝     ╚═╝ v{version}
{end}{blue}
           {yellow}Onion URL Inspector ({red}ONIOFF{yellow}){blue}
  Made with <3 by: {yellow}Nikolaos Kamarinakis ({red}k4m4{yellow}){blue}
                  Version: {yellow}{version}{end}
    """.format(**banner_vars))


def read_file(path):
    with open(path, 'r') as f:
        lines = f.read().splitlines()

    return lines


@click.command()
@click.argument('url', required=False)
@click.option('--input-file', '-f', help='input file name')
@click.option('--output', '-o', help='output file name')
@click.option(
    '--format',
    type=click.Choice(['json', 'tsv']),
    help='output format',
    default='tsv')
@click.option(
    '--socks-port',
    '-p',
    help="Tor instance's port number (default={})".format(SOCKS_PORT_DEFAULT),
    default=SOCKS_PORT_DEFAULT)
@click.option(
    '--timeout',
    '-t',
    help='maximum seconds to wait for a url (default={})'.format(
        TIMEOUT_DEFAULT),
    default=TIMEOUT_DEFAULT)
@click.option(
    '--workers',
    '-w',
    help='number of concurrent workers (default={})'.format(WORKERS_DEFAULT),
    default=WORKERS_DEFAULT)
@click.option(
    '--quite', '-q', help='do not log on stdout', is_flag=True, default=False)
@click.option(
    '--no-banner',
    help='do not display the banner',
    is_flag=True,
    default=False)
def main(url, input_file, output, format, socks_port, timeout, workers, quite,
         no_banner):

    if not no_banner:
        print_banner()

    if not url and not input_file:
        logger.warn(
            "Invalid Options --> Use '-h' or '--help' for usage options")
        os._exit(1)

    url_list = []
    # TODO validate onion url
    if url:
        url_list += url.split()
    if input_file:
        url_list += read_file(input_file)

    invalid_urls = (i for i in url_list if not Onion.verify(i))
    for item in invalid_urls:
        logger.warn('Skipping invalid URL: {}'.format(item))
        del url_list[url_list.index(item)]

    if not url_list:
        logger.error('No onion URL found --> Please enter a valid URL')
        logger.warn("System exit")
        os._exit(1)

    with Onion(socks_port=socks_port) as onion:
        results = onion.check_onions(
            url_list, timeout=timeout, workers=workers)

    logger.debug("[!] Onion inspection successfully complete")
    if not quite:
        for item in results:
            if not item.status:
                logger.error('Failed [{}]: {}'.format(item.url, item.title))
            elif item.active:
                logger.info('Active [{}]: {}'.format(item.url, item.title))
            else:
                logger.warn('Inactive [{}]: Status Code {}'.format(
                    item.url, item.status))

    if output:
        if os.path.exists(output):
            prompt = '{} already exists, can I overwrite?'.format(output)
            if not click.confirm(prompt):
                logger.warn('No output file generated!')
                os._exit(1)

        if format == 'tsv':
            logger.debug('Writing result to {} as TSV.'.format(output))
            header = ['Onion', 'Status Code', 'Active', 'Title/Message']
            with open(output, 'w') as csvfile:
                writer = csv.writer(csvfile, delimiter='\t')
                writer.writerow(header)
                for item in results:
                    writer.writerow(
                        [item.url, item.status, item.active, item.title])
        if format == 'json':
            logger.debug('Writing result to {} as JSON.'.format(output))
            obj = []
            for item in results:
                obj.append({
                    'onion': item.url,
                    'status_code': item.status,
                    'active': item.active,
                    'title': item.title
                })
            with open(output, 'w') as fp:
                json.dump(obj, fp)


if __name__ == '__main__':
    main()
