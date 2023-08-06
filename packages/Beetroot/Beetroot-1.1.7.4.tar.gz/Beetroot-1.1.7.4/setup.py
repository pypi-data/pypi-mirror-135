#Imports
import sys

#Python2 and Python1 are absolutely illegal
if not sys.version.startswith("3"):
    raise VersionError("Python version is not supported.")

import codecs
import os.path

from setuptools import setup
from pathlib import Path as p

#Exception classes
class VersionError(Exception):
    pass

class AuthorError(Exception):
    pass

#Function to read data from metadata.py
def ga():
    with open(p("./beetroot/metadata.py"), "r", encoding="iso-8859-1") as f:
        code = f.read().split("\n")
        
        version = ""
        author = ""
        ae = ""
        url = ""
        for item in code:
            if item.startswith("__author__"):
                yeet = item.split("\"")
                author = str(yeet[1])
                
            elif item.startswith("__version__"):
                yeet = item.split("\"")
                version = str(yeet[1])
                
            elif item.startswith("__authoremail__"):
                yeet = item.split("\"")
                ae = str(yeet[1])
                
            elif item.startswith("__url__"):
                yeet = item.split("\"")
                url = str(yeet[1])
            
        return [version, author, ae, url]
    
#Reads REAMDE.rst
def readme():
    with open(p("./README.rst"), "r", encoding="iso-8859-1") as f:
        return str(f.read())

#Setting up...
yee = ga()
setup(
    name="Beetroot",
    version=yee[0],
    packages=[
        "beetroot"
    ],
    description="A General Purpose Utility package for Python 3",
    url=yee[3],
    author=yee[1],
    author_email=yee[2],
    license="GNU GPLv3",
    install_requires=[
    ],
    python_requires=">=3.6",
    long_description=readme(),
    long_description_content_type="text/x-rst",
    extras_require={
        "tts": [
            "pyttsx3>=2.90"
        ],
        "img": [
            "pillow>=8.4.0",
            "pyautogui>=0.9.53"
        ],
        "ram": [
            "psutil>=5.8.0"
        ],
        "yt": [
            "youtube-search>=2.1.0",
            "youtube-dl>=2021.6.6"
        ],
        "text": [
            "upsidedown>=0.4",
            "zalgo-text>=0.6",
            "nltk>=3.6.5",
            "base65536>=0.1.1"
        ],
        "cython": [
            "Cython>=0.29.24",
            "setuptools>=58.3.0"
        ],
        "keyboard": [
            "keyboard>=0.13.5"
        ],
        "speed": [
            "Cython>=0.29.24"
        ],
        "all": [
            "pyttsx3>=2.90",
            "pillow>=8.4.0",
            "pyautogui>=0.9.53",
            "psutil>=5.8.0",
            "youtube-search>=2.1.0",
            "youtube-dl>=2021.6.6",
            "upsidedown>=0.4",
            "zalgo-text>=0.6",
            "Cython>=0.29.24",
            "setuptools>=58.3.0",
            "nltk>=3.6.5",
            "keyboard>=0.13.5",
            "base65536>=0.1.1"
        ]
    }
)