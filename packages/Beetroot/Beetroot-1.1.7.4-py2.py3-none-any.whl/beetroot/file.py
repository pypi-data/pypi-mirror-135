import shutil
import os

try:
    import ujson as json
    
except (ModuleNotFoundError, ImportError):
    try:
        import simplejson as json
        
    except (ModuleNotFoundError, ImportError):
        import json

from .exception import *
from .objtype import objtype

from pathlib import Path as p

class file:
    """File Manipulation"""
    def move(self, start, end):
        """Moves files"""
        shutil.move(start, end)
        return 0

    def rename(self, orig, new):
        """Renames files, also kinda works to move files, and vice versa"""
        os.rename(p(orig), p(new))
        return 0

    def delete(self, fi, force=False):
        """Deletes files/folders"""
        fi = str(p(fi))
        if os.path.isdir(fi):
            shutil.rmtree(fi)
            
        elif os.path.isfile(fi):
            os.remove(fi)
            
        else:
            if force:
                try:
                    shutil.rmtree(fi)
                    
                except:
                    os.remove(fi)
                    
            else:
                return 1
            
        return 0
    
    def dump(self, fi, data):
        """Dumps data to a file"""
        if objtype(data) == "bytes":
            with open(p(fi), "wb", encoding="iso-8859-1") as f:
                f.write(data)
                f.close()
                
            return 0
        
        else:
            with open(p(fi), "w", encoding="iso-8859-1") as f:
                f.write(data)
                f.close()
                
            return 0
    
    def jdump(self, fi, data, **kwargs):
        """Dumps a dict into a .json file in JSON format
        with or without pretty print."""
        pp = kwargs.get(
            "pp",
            True
        )
        ea = kwargs.get(
            "ensure_ascii",
            False
        )
        with open(p(fi), "w", encoding="iso-8859-1") as f:
            if objtype(pp) != "bool":
                f.close()
                raise InvalidPPBool("Argument \"pp\" must be bool")
            
            if pp:
                json.dump(data, f, indent=4, ensure_ascii=ea)
                
            elif not pp:
                json.dump(data, f, ensure_ascii=ea)
                
            else:
                raise UnknownError("¯\_(ツ)_/¯")
            
        return 0

    def load(self, fi):
        """Reads data from text files."""
        with open(p(fi), "r", encoding="iso-8859-1") as f:
            return f.read()
        
    def bload(self, fi):
        """Reads data from binary (non-text) files."""
        with open(p(fi), "rb", encoding="iso-8859-1") as f:
            return f.read()
        
    def jload(self, fi):
        """Reads data from JSON files."""
        with open(p(fi), "r", encoding="iso-8859-1") as f:
            return json.loads(f.read())
        
    def mkdir(self, path):
        try:
            os.mkdir(path)
            return 0
            
        except (FileExistsError, PermissionError):
            return 1
        
    def rmdir(self, path):
        try:
            shutil.rmtree(path)
            return 0
        
        except (FileNotFoundError, PermissionError):
            return 1
        
    def copydir(self, path, path2):
        try:
            shutil.copytree(path, path2)
            return 0
        
        except (FileNotFoundError, PermissionError):
            return 1

file = file()