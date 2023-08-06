#Beetroot, a general purpose library for all sorts of uses.

#Imports
import sys

from .exception import *

if not str(sys.version).startswith("3"):
    #HOW DARE YOU USE PYTHON2 IDIOT. or python4, if that ever exists
    #well I mean, if it's like a massive database or smth and you don't wanna migrate 1k+ lines of code then I understand, BUT STILL.
    #And if you're using Python1, then the following emoji is for you. 😲
    raise VersionError("Python version is not supported.")

#More imports
import platform
import getpass
import socket
import uuid
import datetime
import os
import shutil
import subprocess
import requests

try:
    from setuptools import setup
    
except (ModuleNotFoundError, ImportError):
    pass

try:
    import keyboard
    
except (ModuleNotFoundError, ImportError):
    pass

from pathlib import Path as p
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from struct import Struct

from .metadata import __version__, __author__, __authoremail__, __url__
from .random import *
from .stopwatch import *
from .file import *
from .tts import *
from .objtype import *
from .obf import *
from .mem import *
from .yt import *
from .hashl import *
from .text import *
from .comp import *
from .pkl import *
from .math import *
from .static import typed

#Constants
__str__ = lambda: "beetroot"
maxint = (
    1<<(
        Struct(
            'i'
        ).size * 8 - 1
    )
) - 1

try:
    ss_req = requests.get(
        "https://ipinfo.io/json",
        verify=True
    )
    
    reee = ss_req.json()["ip"] if ss_req.status_code == 200 else "err"
    
except requests.exceptions.ConnectTimeout:
    reee = "err"
    
sys_stats = [
    getpass.getuser(),
    platform.system(),
    platform.version(),
    platform.machine(),
    platform.node(),
    socket.gethostbyname(socket.gethostname()),
    reee,
    ':'.join(
        (
            "%012X" % uuid.getnode()
        )[i:i+2] for i in range(
            0,
            12,
            2
        )
    ).lower()
]
with suppress():
    import tkinter
    root = tkinter.Tk()
    try:
        root.attributes("-alpha", 0)
        
    except:
        pass
    
    screen_size = (
        root.winfo_screenwidth(),
        root.winfo_screenheight()
    )
    root.update()
    root.destroy()
    
    del root

class recursion:
    """
    A recursion context manager.
    Be careful when using this, settings a recursionlimit
    too high can literally crash python. To use, do
    with beetroot.recursion(<some recursion limit here>):
        <do something here>
        
    Warning, you can cause Python to segfault if recursion limit
    is set too high.
    """
    def __init__(self, limit):
        self.limit = limit
        self.old_limit = sys.getrecursionlimit()
        
    def __enter__(self):
        self.old_limit = sys.getrecursionlimit()
        sys.setrecursionlimit(self.limit)
        
    def __exit__(self, type, value, tb):
        sys.setrecursionlimit(self.old_limit)
        
#def GC():
    #"""Literally deletes EVERY variable in your program"""
    #nvm, only works on file level, doesn't work when imported.
    #copy paste below code if needed
    #Note: all variables starting on "__" will be spared the GC
    #global todel;todel=[];[(exec(f"todel.append(\"{item}\")",globals())if(not item.startswith("__"))else 1)for item in globals()];[exec(f"del {item}",globals())for item in todel]
    
def segfault():
    """Forces python to segfault"""
    import sys
    
    sys.setrecursionlimit(maxint)
    f = lambda a: f(a)
    f(f)
    
def tree(size):
    """Generates little text trees and returns them."""
    a = 1
    b = 2 * size - 1
    out = ""
    size = int(size)
    for i in range(0, size):
        out += "".join(["*" for j in range(0, a)]).center(b) + "\n"
        a += 2
        
    for i in range(0, int(mmath.ceil(size / 20))):
        out += "*".center(b) + "\n"
    
    return out[:-1]
    
def retargs(func):
    """Return all args in function in a list."""
    from inspect import signature
    return list(
        map(
            str,
            str(
                signature(
                    func
                )
            )[1:-1].split(
                ", "
            )
        )
    )

def func(obj):
    """Converts an object into a function."""
    return lambda: obj

def analyze(f):
    """Analyzes a function to check how random it is.
    Should take 2 arguments for the range.
    """
    
    import math as mmath
    
    if callable(f):
        yay = []
        a, b = 0, 10000
        
        for i in range(
            int(
                round(
                    mmath.sqrt(a)
                )
            ),
            int(
                round(
                    mmath.sqrt(b)
                )
            )
        ):
            dum = f(a, b)
            yay.append(dum)
            print(dum)
            
        whee = Counter(yay)
        whee = [whee[item] for item in whee]
        whee = 1 / ((sum(whee) - len(whee)) + 1)
        
        return round(
            100 * whee,
            2
        )
    
    else:
        raise InvalidTypeError("You must input a function to beetroot.analyze().")
        
def delayWrite(*args, **kwargs):
    """Writes things to stdout with a delay."""
    
    import time
    
    delay = float(
        kwargs.get(
            "delay",
            0.1
        )
    )
    out = kwargs.get(
        "out",
        sys.stdout
    )
    yay = "".join(
        strlist(
            args
        )
    )
    
    for i in range(0, len(yay)):
        out.write(yay[i])
        time.sleep(delay)
        
    out.write("\n")
        
def speed(f=None, **kwargs):
    """Memoization and Cython compiling for python functions.
    If you are using this for a random function, pass the nocache=True argument."""
    
    from functools import cache, lru_cache, wraps
    
    if not callable(f) and f != None:
        raise FunctionError("\"f\" must be callable.")
    
    maxsize = kwargs.get(
        "maxsize",
        None
    )
    typ = bool(
        kwargs.get(
            "typed",
            True
        )
    )
    nocache = bool(
        kwargs.get(
            "nocache",
            False
        )
    )
    nocython = bool(
        kwargs.get(
            "nocython",
            False
        )
    )
    def inner(func):
        if not nocython:
            func = typed(func)
            
        if not nocache:
            func = lru_cache(
                maxsize=maxsize,
                typed=typ
            )(
                func
            )
        
        @wraps(func)
        def out(*args, **kwargs):
            return func(*args, **kwargs)
            
        return out
    
    if callable(f):
        return inner(f)
    
    else:
        return inner

def cython(filepath:"filepath to .py or .pyx file", **kwargs) -> "Cython File":
    """Builds a cython extension thingy."""
    try:
        pypath = kwargs.get(
            "pypath",
            sys.executable
        ).replace(
            "\\",
            r"\\"
        )
        
        if pypath == sys.executable:
            pass
        
        else:
            pypath = os.path.abspath(pypath)
            
        #print(pypath)
            
        file.dump("./setup.py", rf"""#Generated by python-beetroot
try:
    from setuptools import setup
    from Cython.Build import cythonize
    
    setup(
        ext_modules=cythonize(
            r"{os.path.abspath(str(filepath))}"
        )
    )
    
except (ModuleNotFoundError, ImportError):
    raise ModuleNotFoundError("setuptools and Cython must be installed. Try pip install setuptools Cython or pip install beetroot[cython].")
        """)
        
        outdir = str(
            ".".join(
                os.path.basename(
                    filepath
                ).split(
                    "."
                )[:-1]
            )
        )
        subprocess.call(pypath + " " + os.path.abspath("setup.py") + " build_ext --build-lib " + outdir)
        
        try:
            shutil.rmtree(os.path.abspath("build"))
            
        except FileNotFoundError:
            pass
        
        try:
            file.delete(os.path.abspath("setup.py"))
            
        except FileNotFoundError:
            pass
        
        for filename in os.listdir(os.path.abspath(".")):
            if (filename.endswith(".exp") or filename.endswith(".lib") or filename.endswith(".obj")) and (filename.startswith(outdir)):
                try:
                    file.delete(os.path.abspath(".") + filename)
                    
                except FileNotFoundError:
                    pass
                    
        try:
            c = str(p("".join(["./", outdir, ".c"])))
            file.move(c, str(p("".join(["./", outdir, "/", c]))))
            
        except FileNotFoundError:
            pass
        
    except NameError:
        raise ModuleError("setuptools and Cython must be installed. Try `pip install setuptools Cython` or `pip install beetroot[cython]`.")

def printn(*args):
    """Prints a string without a trailing newline"""
    errprint("This is deprecated. Use default print(end=\"\") instead.")
    for i in range(0, len(args)):
        args = list(args)
        if objtype(args[i]) == "bytes":
            args[i] = str(args[i].decode("iso-8859-1"))
            
        else:
            args[i] = str(args[i])
            
    print(" ".join(args), end="", flush=True)

def getch(str_:"string to print before getch()ing"="") -> "Single Char":
    """input() but it only waits for one character."""
    try:
        printn(str_)
        alphabet = [chr(i) for i in range(97, 123)]
        
        lett = {
            "1": "!",
            "2": "@",
            "3": "#",
            "4": "$",
            "5": "%",
            "6": "^",
            "7": "&",
            "8": "*",
            "9": "(",
            "0": ")"
        }
        syms = list("-=[]\\;',./")
        dictsym = {
            "-": "_",
            "=": "+",
            "[": "{",
            "]": "}",
            "\\": "|",
            ";": ":",
            "'": "\"",
            ",": "<",
            ".": ">",
            "/": "?"
        }
        cchars = {
            "tab": "\t",
            "enter": "\n"
        }
        
        while True:
            if (not keyboard.is_pressed("ctrl")) or (not keyboard.is_pressed("alt")):
                for letter in alphabet:
                    if keyboard.is_pressed(letter):
                        print()
                        if keyboard.is_pressed("shift"):
                            return letter.upper()
                        
                        else:
                            return letter
                    
                for num in range(0, 10):
                    if keyboard.is_pressed(str(num)):
                        print()
                        if keyboard.is_pressed("shift"):
                            for item in lett:
                                if str(num) == item:
                                    return lett[item]
                                
                        else:
                            return str(num)
                        
                for sym in syms:
                    if keyboard.is_pressed(sym):
                        if keyboard.is_pressed("shift"):
                            for item in dictsym:
                                if sym == item:
                                    return dictsym[item]
                                
                        else:
                            return sym
                        
                for char in cchars:
                    if keyboard.is_pressed(char):
                        return cchars[char]
    
    except NameError:
        raise ModuleError("keyboard must be installed. Try `pip install keyboard` or `pip install beetroot[keyboard]`.")

def delchar(char=" "):
    """Deletes char from stdout"""
    sys.stdout.write(f"\b{char}\b")

def isAdmin() -> "UAC Admin perms in Windows":
    """Checks if python program has administrator prviliges."""
    
    import ctypes
    
    if platform.system() == "Windows":
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        
        except:
            return False
        
    else:
        raise OSError("beetroot.isAdmin() only works for windows.")

def admin():
    """Requests UAC Admin on Windows"""
    
    import ctypes
    
    if platform.system() == "Windows":
        ctypes.windll.shell32.ShellExecuteW(
            None,
            'runas',
            sys.executable,
            ' '.join(sys.argv),
            None,
            None
        )
        
        return isAdmin()
        
    else:
        raise OSError("beetroot.admin() only works for windows.")
      
def test() -> "Hello, world!":
    """Test"""
    print("Hello, world!")
    return 0

def locate():
    """I literally made this cuz I was tired of looking for my python folder."""
    assert 1 > 2

def remove(str_:"a string", ting:"also a string"):
    """Removes all occurences of "ting" in str_"""
    return str_.replace(str(ting), "")

def siteize(str_:"a string"):
    """Turns the string into a malformed url so you can talk
    in a weird way. For example, "Hello, world!", gets
    turned into "www.HelloWorld.com"."""
    a = list(str_)
    b = []
    
    for item in a:
        if item.isalnum() or item == " ":
            b.append(item)
            
    b = remove("".join(b).title(), " ")
    return "".join(["www.", b, ".com"])
    
def taskkill(tasque, **kwargs):
    """Kills a task by name with psutil."""
    try:
        import psutil
        
    except (ModuleNotFoundError, ImportError):
        raise ModuleError("psutil must be installed to use beetroot.taskkill(). Use pip install psutil or pip install beetroot[ram].")

    ka = int(
        kwargs.get(
            "killamount",
            -1
        )
    )
    for proc in psutil.process_iter():
        if proc.name() == tasque:
            proc.kill()
            if ka == -1:
                pass
            
            else:
                ka -= 1
                if ka <= 0:
                    return
                
def crash() -> "Crashes python or smth idk":
    """This causes python to cra- cra- cra- cras- cra- crash."""
    
    taskkill(os.path.basename(sys.executable).replace(".EXE", ".exe"))    
    
    with recursion(1<<30):
        f = lambda a : f(a)
        f(f)
    
    return 1
    
def quicksort(array:"Unsorted array") -> "Sorted array":
    """Quicksort algorithm"""
    try:
        with recursion(1500):
            less = []
            equal = []
            greater = []

            if len(array) > 1:
                pivot = array[0]
                
                for x in array:
                    if x < pivot:
                        less.append(x)
                        
                    elif x == pivot:
                        equal.append(x)
                        
                    elif x > pivot:
                        greater.append(x)
                        
                return quicksort(less) + equal + quicksort(greater)
            
            else:
                return array
        
    except TypeError:
        raise InvalidTypeError(f"Cannot sort type {objtype(array)}.")
    
def cyclesort(array:"Unsorted Array") -> "Sorted Array":
    """Cyclesort, much slower than quicksort but uses less RAM"""
    try:
        for cycleStart in range(0, len(array) - 1):
            item = array[cycleStart]
            pos = cycleStart
            
            for i in range(cycleStart + 1, len(array)):
                if array[i] < item:
                    pos += 1
                
            if pos == cycleStart:
                continue
            
            while item == array[pos]:
                pos += 1
             
            array[pos], item = item, array[pos]
          
            while pos != cycleStart:
                pos = cycleStart
             
                for i in range(cycleStart + 1, len(array)):
                    if array[i] < item:
                        pos += 1
                   
                while item == array[pos]:
                    pos += 1
                
                array[pos], item = item, array[pos]
             
        return array
    
    except TypeError:
        raise InvalidTypeError(f"Cannot sort type {objtype(array)}.")

def swap(array, ia, ib):
    """Swap 2 items in a list."""
    array[ia], array[ib] = array[ib], array[ia]
    return array

def isSorted(array):
    """Checks if an array is sorted without actually sorting it."""
    all(a <= b for a, b in zip(array, array[1:]))

def maplist(args, f=str):
    """Wrapper function for map(). Returns a regular list instead of a map object."""
            
    return list(map(str, args))

def strlist(args):
    """Runs str() on all item in list.
    Now that I think about it, I could'a used map(str, list)
    but i'm an idiot and also lazy so here ya go.
    ...
    Wait, this can handle bytestrings. Yeah."""
    args = list(args)
    for i in range(0, len(args)):
        if objtype(args[i]) == "bytes":
            args[i] = args[i].decode("iso-8859-1")
            
        else:
            args[i] = str(args[i])
            
    return args

def errprint(*args, **kwargs):
    """Like print(), but outputs to stderr instead."""
    end = str(
        kwargs.get(
            "end",
            "\n"
        )
    )
    out = kwargs.get(
        "out",
        sys.stderr
    )
    out.write(
        " ".join(
            maplist(
                list(
                    args
                ),
                f=str
            )
        ) + end
    )
    
def errprintn(*args):
    """Deprecated."""
    errprint("This is deprecated. Use errprint(end=\"\") instead.")
    end = str(
        kwargs.get(
            "end",
            ""
        )
    )
    sys.stderr.write(
        " ".join(
            maplist(
                list(
                    args
                ),
                f=str
            )
        ) + end
    )

def execfile(file:"a filepath to a .py file"):
    """Executes a python .py script"""
    with open(p(file), "r", encoding="iso-8859-1") as f:
        exec(f.read())
        f.close()

def unline(str_:"a string"):
    """Makes multi-line strings single-line"""
    return str(str_).replace("\n", "\\n").replace("\t", "\\t").replace("\r", "\\r").replace("\a", "\\a").replace("\b", "\\b")

def reline(str_:"a string"):
    """Reverses beetroot.unline()"""
    return str(str_).replace("\\n", "\n").replace("\\t", "\t").replace("\\r", "\r").replace("\\a", "\a").replace("\\b", "\b")

def pixelgrab(i_x:"x coordinate", i_y:"y coordinate"):
    """Grabs colour of pixel at (i_x, i_y)"""

    try:
        import PIL.ImageGrab
        return PIL.ImageGrab.grab().load()[int(i_x), int(i_y)]
    
    except (ModuleNotFoundError, ImportError):
        raise ModuleError("PIL most be installed to use beetroot.pixelgrab(). Try pip install pillow.")
    
    except ValueError:
        raise InvalidTypeError("Arguement \"i_x\" and \"i_y\" must be ints or floats")
    
def mousepixelgrab():
    """Grabs colour of pixel at mouse-pointer"""
    try:
        import PIL.ImageGrab
        import pyautogui
        
        pos = pyautogui.position()
        return PIL.ImageGrab.grab().load()[pos.x, pos.y]

    except (ModuleNotFoundError, ImportError):
        raise ModuleError("PIL and pyautogui most be installed to use beetroot.mousepixelgrab(). Try pip install pillow pyautogui.")

def totally_not_a_rickroll() -> "definitely not a rickroll >:)":
    """Definitely absolutely 100% totally completely not a rickroll"""
    
    import webbrowser
    
    for i in range(0, 100):
        rickrolled = True
        
    webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ", new=0)
    return "".join(["U JUST GOT RICKROLLED IN ", str(datetime.datetime.now().year)])