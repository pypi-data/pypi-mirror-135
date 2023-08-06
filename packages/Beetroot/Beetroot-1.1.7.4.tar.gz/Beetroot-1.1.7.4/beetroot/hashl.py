from .exception import *
from .objtype import *

class hashl:
    def hashf(self, str_, **kwargs):
        """Hash Function that uses MD5 or SHA512."""
        
        import hashlib
        
        secure = kwargs.get(
            "secure",
            True
        )
        
        if objtype(secure) != "bool":
            raise InvalidHashSecurityValue("Argument \"secure\" can only be boolean")
        
        if secure:
            if objtype(str_) == "bytes":
                return hashlib.sha512(str_).hexdigest()
            
            else:
                return hashlib.sha512(str(str_).encode("iso-8859-1")).hexdigest()
        
        elif not secure:
            if objtype(str_) == "bytes":
                return hashlib.md5(str_).hexdigest()
            
            else:
                return hashlib.md5(str(str_).encode("iso-8859-1")).hexdigest()
            
        else:
            raise UnknownError("¯\_(ツ)_/¯")
        
    def dehash(self, hashobj):
        
        import sys
        
        sys.stderr.write("StupidProgrammerError: You can't dehash hashes, dumb dumb. Unless it's an MD5/SHA1, which I'm too lazy to check for. Also I don't know how to dehash those, so TOO BAD.")
        sys.exit()

hashl = hashl()