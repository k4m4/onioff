#!/usr/bin/env python
# -.- coding: utf-8 -.-
# onioff.py

"""
Copyright (C) 2016-2017 Nikolaos Kamarinakis (nikolaskam@gmail.com)
See License at nikolaskama.me (https://nikolaskama.me/onioffproject)
"""

import socket, socks, requests, sys, os, optparse, time, httplib, datetime, re
from termcolor import colored
from bs4 import BeautifulSoup
from time import sleep

BLUE, RED, WHITE, YELLOW, END = '\33[94m', '\033[91m', '\33[97m', '\33[93m', '\033[0m'
sys.stdout.write(RED + """
 ██████╗ ███╗   ██╗██╗ ██████╗ ███████╗███████╗
██╔═══██╗████╗  ██║██║██╔═══██╗██╔════╝██╔════╝
██║   ██║██╔██╗ ██║██║██║   ██║█████╗  █████╗
██║   ██║██║╚██╗██║██║██║   ██║██╔══╝  ██╔══╝
╚██████╔╝██║ ╚████║██║╚██████╔╝██║     ██║
 ╚═════╝ ╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═╝     ╚═╝ v0.1
"""  + END + BLUE +
'\n' + '{0}Onion URL Inspector ({1}ONIOFF{2}){3}'.format(YELLOW, RED, YELLOW, BLUE).center(67) +
'\n' + 'Made With <3 by: {0}Nikolaos Kamarinakis ({1}k4m4{2}){3}'.format(YELLOW, RED, YELLOW, BLUE).center(67) +
'\n' + 'Version: {0}2.0{1}'.format(YELLOW, END).center(57) + '\n')

def flushPrint(msg, error=False, ext=False, heavy=False):
    if ext:
        msg, msg_e = msg.split(' --> ')
        msg += ' --> '

    if options.fast:
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
    else:
        if error:
            for char in msg:
                sleep(0.03)
                sys.stdout.write(colored(char, 'red'))
                sys.stdout.flush()
            if ext:
                for char in msg_e:
                    sleep(0.03)
                    sys.stdout.write(colored(char, 'red', attrs = ['bold']))
                    sys.stdout.flush()
        elif heavy:
            for char in msg:
                sleep(0.03)
                sys.stdout.write(colored(char, 'yellow'))
                sys.stdout.flush()
            if ext:
                for char in msg_e:
                    sleep(0.03)
                    sys.stdout.write(colored(char, 'yellow', attrs = ['bold']))
                    sys.stdout.flush()
        else:
            for char in msg:
                sleep(0.03)
                sys.stdout.write(colored(char, 'green'))
                sys.stdout.flush()
            if ext:
                for char in msg_e:
                    sleep(0.03)
                    sys.stdout.write(colored(char, 'green', attrs = ['bold']))
                    sys.stdout.flush()

def create_connection(address, timeout=None, source_address=None):
    sock = socks.socksocket()
    sock.connect(address)
    return sock

def verifyTor(): # Verify Tor Is Running
    global pure_ip
    ipcheck_url = 'http://checkip.amazonaws.com/'
    pure_ip = requests.get(ipcheck_url).text.replace('\n','')
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 9050)
    socket.socket = socks.socksocket
    socket.create_connection = create_connection

    global urllib2
    import urllib2

    tor_ip = urllib2.urlopen(ipcheck_url).read().replace('\n','') # Tor IP
    if pure_ip == tor_ip:
        flushPrint("\n[-] Unsuccessful Tor Connection", True)
       	flushPrint("\n[-] System Exit\n", True)
       	sys.exit(1)
    else:
        flushPrint("\n[+] Tor Running Normally") # PRINT VERSION

def checkOnion(onion): # Check Onion Status
    global gathered, response, outFile

    inspect_msg = "\n[!] Inspecting Onion --> " + str(onion)
    flushPrint(inspect_msg, False, True, True)
    ipcheck_url = 'http://checkip.amazonaws.com/'
    check_ip = urllib2.urlopen(ipcheck_url).read().replace('\n','')
    if check_ip != pure_ip:
        flushPrint('\n[+] Sending Request')
        try:
            response = urllib2.urlopen(onion).getcode()
        except urllib2.URLError as e:
            response = 'INACTIVE (' + str(e.reason) + ')'
        except urllib2.HTTPError as e:
            response = 'INACTIVE (' + str(e.code) + ')'
        except httplib.HTTPException as e:
            response = 'INACTIVE (HTTPException)'
        except socks.SOCKS5Error as e:
            response = 'INACTIVE (Host Unreachable)'
        except Exception:
            import traceback
            response = 'INACTIVE (' + traceback.format_exc() + ')'

       	if response == 200:
            flushPrint("\n[+] Onion Up & Running --> ACTIVE", False, True)
            response = 'ACTIVE (Code' + str(response) + ')'
       	else:
       	    flushPrint("\n[-] Onion Down --> INACTIVE", True, True)
       	    response = 'INACTIVE'

        if 'INACTIVE' not in response:
            try:
                flushPrint("\n[+] Retrieving Onion Title")
                soup = BeautifulSoup(urllib2.urlopen(onion), 'html.parser')
                response2 = soup.title.string
                onion_title = "\n[+] Onion Title --> " + str(response2)
                flushPrint(onion_title, False, True, False)
            except:
                import traceback
                response2 = 'UNAVAILABLE'
                flushPrint("\n[-] Onion Title Is Unavailable", True)
        else:
            response2 = 'UNAVAILABLE (Onion Inactive)'

        gathered[onion] = response, response2


    else:
       	flushPrint("\n[-] Connection Anonymity Lost", True)
       	flushPrint("\n[-] System Exit\n", True)
       	sys.exit(1)

def readFile(file): # Read Onion File
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
                        checkOnion(onion)

            else:
                flushPrint("\n[-] Dictionary Is Empty --> Please Enter A Valid File", True, True)
                flushPrint("\n[-]System Exit\n", True)

       	myFile.close()
    except IOError:
       	flushPrint("\n[-] Invalid Onion File --> Please Enter A Valid File Path", True, True)
       	flushPrint("\n[-] System Exit\n", True)
       	sys.exit(1)

def uniqueOutFile(checkFile): # Create A Unique Filename
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

        flushPrint("\n[+] Commencing Onion Inspection")
        try:
            verifyTor()
        except KeyboardInterrupt:
            print '\nHave A Great Day! :)'
            sys.exit(1)

        except:
            flushPrint("\n[-] Tor Offline --> Please Make Sure Tor Is Running", True, True)
            flushPrint("\n[-] System Exit\n", True)
            sys.exit(1)

        for onion in argv:
            if not onion.startswith('http') and not onion.startswith('https'):
                flushPrint("\n[-] No Onion URL Found --> Please Enter A Valid URL", True, True)
                flushPrint("\n[-] System Exit\n", True)
                sys.exit(1)
            else:
                checkOnion(onion)

        if options.file != None:
            file = options.file
            try:
                readFile(file)
            except KeyboardInterrupt:
                print '\nHave A Great Day! :)'
                sys.exit(1)

        try:
            outFile = uniqueOutFile(options.output_file)
            with open(outFile, 'a') as OutFile:
                for k, v in gathered.items():
                    # output format {some_link.onion} - {page_title}
                    if 'Code200' in v[0]:
                        OutFile.write('{0} - {1}'.format(k, v[1]) + '\n')
                    else:
                        OutFile.write('{0} - {1}'.format(k, v[0]) + '\n')
        except IOError:
            flushPrint("\n[-] Invalid Path To Out File Given --> Please Enter a Valid Path", True, True)
            flushPrint("\n[-] System Exit\n", True)
            sys.exit(1)
        except KeyboardInterrupt:
            print '\nHave A Great Day! :)'
            sys.exit(1)

        flushPrint("\n[!] Onion Inspection Successfully Complete", False, False, True)
        saved_msg = "\n[!] Inspection Report Saved As --> " + str(outFile)
        flushPrint(saved_msg, False, True, True)
        print "\nComp/tional Time Elapsed:", (time.clock() - start)

    else:
        flushPrint("\n\n[!] Use '-h' or '--help' For Usage Options\n", False, False, True)

if __name__ == '__main__':

    start = time.clock()

    optparse.OptionParser.format_epilog = lambda self, formatter: self.epilog

    info = 'Onioff v2.0 Nikolaos Kamarinakis (nikolaskama.me)'

    examples = ('\nExamples:\n'+
                '  python onioff.py http://xmh57jrzrnw6insl.onion/\n'+
                '  python onioff.py -f ~/onions.txt -o ~/report.txt\n'+
                '  python onioff.py https://facebookcorewwwi.onion/ -o ~/report.txt\n')

    parser = optparse.OptionParser(epilog=examples,
                                   usage='python %prog {onion} [options]',
                                   prog='onioff.py', version=('ONIOFF v2.0'))

    parser.add_option('-f', '--file', action='store',
                      dest='file', help='onion filename')

    default = 'reports/onioff_{}'.format(unicode(datetime.datetime.now())[:-7].replace(' ', '_'))
    parser.add_option('-o', '--output', action='store', default=default,
                      dest='output_file', help='output filename')

    parser.add_option('-F', '--fast', action='store_true', default=False,
                      dest='fast', help='finish investigation asap')

    (options, argv) = parser.parse_args()

    gathered = {}

    main()
