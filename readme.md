<!-- <h1 align="center">
    <img width="650" src="https://nikolaskama.me/content/images/2017/05/_1023323.png" alt="ONIOFF Logo">
</h1> -->

```
 ██████╗ ███╗   ██╗██╗ ██████╗ ███████╗███████╗
██╔═══██╗████╗  ██║██║██╔═══██╗██╔════╝██╔════╝
██║   ██║██╔██╗ ██║██║██║   ██║█████╗  █████╗
██║   ██║██║╚██╗██║██║██║   ██║██╔══╝  ██╔══╝
╚██████╔╝██║ ╚████║██║╚██████╔╝██║     ██║
 ╚═════╝ ╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═╝     ╚═╝ v2.0
```

[![Build Status](https://travis-ci.org/k4m4/onioff.svg?branch=master)](https://travis-ci.org/k4m4/onioff)
[![License Badge](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/k4m4/onioff/blob/master/license)
[![Compatibility](https://img.shields.io/badge/python-3-brightgreen.svg)](https://github.com/k4m4/onioff)
[![Say Thanks](https://img.shields.io/badge/say-thanks-ff69b4.svg)](https://saythanks.io/to/k4m4)
[![GitHub Stars](https://img.shields.io/github/stars/k4m4/onioff.svg)](https://github.com/k4m4/onioff/stargazers)

> A simple tool - written in pure python - for inspecting Deep Web URLs (or onions). 

- Compatible with Python 3🎉.
- Author: [Nikolaos Kamarinakis](mailto:nikolaskam@gmail.com) ([nikolaskama.me](https://nikolaskama.me/))

---

<p align="center">✨Read my latest post: <a href="http://resources.infosecinstitute.com/inspecting-deep-web-links"><i>Inspecting Deep Web Links.</i></a>✨</p>

---

<p align="center">
    <sub>Visit <a href="https://nikolaskama.me/onioffproject/"><code>nikolaskama.me/onioffproject</code></a> for more information. Check out my <a href="https://nikolaskama.me">blog</a> and follow me on <a href="https://twitter.com/nikolaskama">Twitter</a>.</sub>
</p>

<br>

# Installation 

You can download ONIOFF by cloning the [Git Repo](https://github.com/k4m4/onioff) and simply installing its requirements:

```
~ ❯❯❯ git clone https://github.com/k4m4/onioff.git
~ ❯❯❯ cd onioff
~/onioff ❯❯❯ pip3 install -r requirements.txt
~/onioff ❯❯❯ python3 onioff.py
```

**NOTE**: In order for ONIOFF to work, Tor must be correctly configured and running.

<br>

# Usage

```
Usage: python3 onioff.py {onion} [options]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -f FILE, --file=FILE  name of onion file
  -o OUTPUT_FILE, --output=OUTPUT_FILE
                        output filename
  -a, --active          log active onions only to output file

Examples:
  python3 onioff.py http://xmh57jrzrnw6insl.onion/
  python3 onioff.py -f ~/onions.txt -o ~/report.txt -a
  python3 onioff.py https://facebookcorewwwi.onion/ -o ~/report.txt
```

To view all available options run:

```
~/onioff ❯❯❯ python3 onioff.py -h
```

<br>

# Demo

Here's a short demo:

[![ONIOFF Demo](https://nikolaskama.me/content/images/2016/09/onioff_demo.png)](https://asciinema.org/a/87557?autoplay=1)

(For more demos click [here](https://asciinema.org/~k4m4))

<br>

# Developer

- **Nikolaos Kamarinakis** (k4m4) - [@nikolaskama](https://twitter.com/nikolaskama)

<br>

# License

Copyright 2016-2017 by [Nikolaos Kamarinakis](mailto:nikolaskam@gmail.com). Some rights reserved.

ONIOFF is under the terms of the [MIT License](https://www.tldrlegal.com/l/mit), following all clarifications stated in the [license file](https://raw.githubusercontent.com/k4m4/onioff/master/license).

<br>

For more information head over to the [official project page](https://nikolaskama.me/onioffproject/).
You can also go ahead and email me anytime at **nikolaskam{at}gmail{dot}com**. 
