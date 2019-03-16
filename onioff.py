#!/usr/bin/env python3
# -.- coding: utf-8 -.-
# onioff.py

"""
Copyright (C) 2016-2018 Nikolaos Kamarinakis (nikolaskam@gmail.com)
See License at nikolaskama.me (https://nikolaskama.me/onioffproject)
"""

import socket, socks, requests, sys, os, optparse, datetime, re
from urllib.request import urlopen
from termcolor import colored
from bs4 import BeautifulSoup
from time import process_time, sleep
from threading import Thread
import queue as queue


BLUE, RED, WHITE, YELLOW, GREEN, END = '\33[94m', '\033[91m', '\33[97m', '\33[93m', '\033[32m', '\033[0m'
sys.stdout.write(RED + """
 ██████╗ ███╗   ██╗██╗ ██████╗ ███████╗███████╗
██╔═══██╗████╗  ██║██║██╔═══██╗██╔════╝██╔════╝
██║   ██║██╔██╗ ██║██║██║   ██║█████╗  █████╗
██║   ██║██║╚██╗██║██║██║   ██║██╔══╝  ██╔══╝
╚██████╔╝██║ ╚████║██║╚██████╔╝██║     ██║
 ╚═════╝ ╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═╝     ╚═╝ v2.1
"""  + END + BLUE +
'\n' + '{}Onion URL Inspector ({}ONIOFF{}){}'.format(YELLOW, RED, YELLOW, BLUE).center(67) +
'\n' + 'Made with <3 by: {}Nikolaos Kamarinakis ({}k4m4{}){}'.format(YELLOW, RED, YELLOW, BLUE).center(67) +
'\n' + 'Version: {}2.1{}'.format(YELLOW, END).center(57) + '\n')


def nowPrint(msg, error=False, ext=False, heavy=False):
    if ext:
        msg, msg_e = msg.split(' --> ')
        msg += ' --> '

    if error:
        sys.stdout.write(colored(msg, 'red'))
        if ext:
            sys.stdout.write(colored(msg_e, 'red', attrs = ['bold']))
    elif heavy:
        sys.stdout.write(colored(msg, 'yellow'))
        if ext:
            sys.stdout.write(colored(msg_e, 'yellow', attrs = ['bold']))
    else:
        sys.stdout.write(colored(msg, 'green'))
        if ext:
            sys.stdout.write(colored(msg_e, 'green', attrs = ['bold']))

    sleep(0.1)



# Create TOR connection
def connectTor():
    global pure_ip

    ipcheck_url = 'https://locate.now.sh/ip'
    pure_ip = requests.get(ipcheck_url).text.replace('\n','')

    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 9050)
    socket.socket = socks.socksocket
    def create_connection(address, timeout=None, source_address=None):
        sock = socks.socksocket()
        sock.connect(address)
        return sock
    socket.create_connection = create_connection

    tor_ip = requests.get(ipcheck_url).text.replace('\n','')
    if pure_ip == tor_ip:
        nowPrint("[-] Unsuccessful Tor connection", True)
        nowPrint("\n[-] Exiting...\n", True)
        os._exit(1)
    else:
        nowPrint("\n[+] Tor running normally\n")



# Perform onion status & title inspection
def checkOnion(onion):
    global gathered, response, outFile

    ipcheck_url = 'https://locate.now.sh/ip'
    check_ip = requests.get(ipcheck_url).text.replace('\n','')
    if check_ip != pure_ip:
        try:
            response = urlopen(onion).getcode()
        except Exception as e:
            response = e

        if response == 200:
            try:
                soup = BeautifulSoup(urlopen(onion), 'lxml')
                response2 = soup.title.string
            except:
                response2 = 'UNAVAILABLE'

            show = ("[O] {} ({}ACTIVE{}) ==> '{}'").format(onion, GREEN, END, response2)
            gathered[onion] = 'ACTIVE', response2
        else:
            response = str(response).strip().replace(':','')
            response2 = 'UNAVAILABLE (Onion Inactive)'
            if len(response) > 2:
                show = ("[O] {} ({}INACTIVE{}) - {}").format(onion, RED, END, str(response).strip())
            else:
                show = ("[O] {} ({}INACTIVE{})").format(onion, RED, END)
            if not options.active:
                gathered[onion] = 'INACTIVE', response2

        return show

    else:
        nowPrint("[-] Lost Tor connection", True)
        nowPrint("\n[-] Exiting...\n", True)
        os._exit(1)



# Extract onion URLs from file
def readFile(file):
    try:
        with open(file, 'r') as myFile:
            if os.path.getsize(file) > 0:
                onions = myFile.readlines()
                for onion in re.findall(r'(?:https?://)?(?:www)?\S*?\.onion', '\n'.join(onions)):
                    onion = onion.replace('\n', '')
                    if not len(onion) > len('.onion'):
                        pass
                    else:
                        if not onion.startswith('http') and not onion.startswith('https'):
                            onion = 'http://'+str(onion)
                        q.put(onion)

            else:
                nowPrint("[-] Onion file is empty --> Please enter a valid file", True)
                nowPrint("\n[-] Exiting...\n", True)
                os._exit(1)

        q.join()
        myFile.close()

    except IOError:
        nowPrint("[-] Invalid onion file --> Please enter a valid file path", True)
        nowPrint("\n[-] Exiting...\n", True)
        os._exit(1)



# Unique output filename generation
def uniqueOutFile(checkFile):
    f = checkFile.split('.')
    if len(f) < 2:
        checkFile += '.txt'
    if os.path.exists(checkFile):
        fName, fType = checkFile.split('.')
        fList = list(fName)
        exists = True
        fName += '-{}'
        i = 1
        while exists:
            tempFile = (str(fName)+'.'+str(fType))
            tempFile = tempFile.format(i)
            if os.path.exists(tempFile):
                i += 1
            else:
                outFile = tempFile
                exists = False
    else:
        outFile = checkFile

    return outFile



def main():

    if len(sys.argv[1:]) > 0:

        if (len(sys.argv[1:]) == 2 and sys.argv[1] == '--output') or (len(sys.argv[1:]) == 1 and sys.argv[1] == '--active') or \
            (len(sys.argv[1:]) == 2 and sys.argv[1] == '--output'):
            nowPrint("\n[!] Invalid Options --> Use '-h' or '--help' for usage options\n", False, False, True)
            os._exit(1)

        nowPrint("\n[+] Commencing onion inspection")
        try:
            connectTor()
        except KeyboardInterrupt:
            print('\nHave a great day! :)')
            os._exit(1)
        except:
            nowPrint("\n[-] Tor offline --> Please make sure Tor is running", True)
            nowPrint("\n[-] Exiting...\n", True)
            os._exit(1)


        def inspect():
            while True:
                onion = q.get()
                response = checkOnion(onion)
                sys.stdout.write(response+'\n')
                sleep(0.1)
                q.task_done()

        for i in range(concurrent):
            t = Thread(target=inspect)
            t.daemon = True
            t.start()

        try:
            for onion in argv:
                if not onion.startswith('http') and not onion.startswith('https'):
                    nowPrint("[-] No onion URL found --> Please enter a valid URL", True)
                    nowPrint("\n[-] Exiting...\n", True)
                    os._exit(1)
                else:
                    q.put(onion)
                    q.join()
        except KeyboardInterrupt:
            print('\nHave a great day! :)')
            os._exit(1)


        if options.file != None:
            file = options.file
            readFile(file)


        try:
            outFile = uniqueOutFile(options.output_file)
            with open(outFile, 'a') as OutFile:
                for k, v in gathered.items():
                    # output format: {some_link.onion} - {page_title}
                    if 'ACTIVE' in v[0]:
                        OutFile.write('{} - {}'.format(k, v[1]) + '\n')
                    else:
                        OutFile.write('{} - {}'.format(k, v[0]) + '\n')
        except IOError:
            nowPrint("[-] Invalid path to out file given --> Please enter a valid path", True)
            nowPrint("\n[-] Exiting...\n", True)
            os._exit(1)
        except KeyboardInterrupt:
            print('\nHave a great day! :)')
            os._exit(1)


        nowPrint("[!] Onion inspection successfully complete", False, False, True)
        saved_msg = "\n[!] Inspection report saved as --> " + str(outFile)
        nowPrint(saved_msg, False, True, True)
        print("\nComp/tional time elapsed:", (process_time() - start))

    else:
        nowPrint("\n[!] Use '-h' or '--help' for usage options\n", False, False, True)



if __name__ == '__main__':

    start = process_time()

    optparse.OptionParser.format_epilog = lambda self, formatter: self.epilog

    info = 'ONIOFF v3.0 Nikolaos Kamarinakis (nikolaskama.me)'

    examples = ('\nExamples:\n'+
                '  python3 onioff.py http://xmh57jrzrnw6insl.onion/\n'+
                '  python3 onioff.py -f ~/onions.txt -o ~/report.txt\n'+
                '  python3 onioff.py https://facebookcorewwwi.onion/ -o ~/report.txt\n')

    parser = optparse.OptionParser(epilog=examples,
                                   usage='python3 %prog {onion} [options]',
                                   prog='onioff.py', version=('ONIOFF v2.1'))

    parser.add_option('-f', '--file', action='store',
                      dest='file', help='name of onion file')

    default = 'reports/onioff_{}'.format(str(datetime.datetime.now())[:-7].replace(' ', '_'))
    parser.add_option('-o', '--output', action='store', default=default,
                      dest='output_file', help='output filename')

    parser.add_option('-a', '--active', action='store_true', default=False,
                      dest='active', help='log active onions only to output file')

    (options, argv) = parser.parse_args()

    gathered = {}

    concurrent = 200
    q = queue.Queue(concurrent * 2)

    main()