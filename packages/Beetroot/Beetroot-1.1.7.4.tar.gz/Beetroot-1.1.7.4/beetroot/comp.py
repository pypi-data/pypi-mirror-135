from .exception import *
from .objtype import objtype

class comp:
    def compress(self, str_):
        """Compresses a strings with hybrid zlib/lzma"""
        
        import lzma
        import zlib
        import sys
        
        if objtype(str_) == "bytes":
            a = str_.decode("iso-8859-1")
            
        else:
            a = str(str_)
            
        aa = "n" + a
        ab = "z" + zlib.compress(a.encode("utf-8")).decode("iso-8859-1")
        ac = "l" + lzma.compress(a.encode("utf-8")).decode("iso-8859-1")
        
        yay = [aa, ab, ac]
        yay2 = [sys.getsizeof(aa), sys.getsizeof(ab), sys.getsizeof(ac)]
        
        return yay[yay2.index(min(yay2))]
    
    def decompress(self, str_):
        """Decompresses a strings with hybrid zlib/lzma"""
        
        import lzma
        import zlib
        import sys
        
        if objtype(str_) == "bytes":
            str_ = str_.decode("iso-8859-1")
            
        else:
            str_ = str(str_)
            
        if str(str_).startswith("n"):
            return str(str_)[1:]
        
        elif str(str_).startswith("z"):
            return zlib.decompress(str(str_)[1:].encode("iso-8859-1")).decode("utf-8")
        
        elif str(str_).startswith("l"):
            return lzma.decompress(str(str_)[1:].encode("iso-8859-1")).decode("utf-8")
        
        else:
            raise StringError("This string could not be properly decompressed.")
        
comp = comp()