from .exception import *
from .objtype import *

class mem:
    """Memory shtuff"""
    def mem(self):
        """Returns total, used and available memory."""
        
        try:
            from psutil import virtual_memory, swap_memory
            
        except (ModuleNotFoundError, ImportError):
            raise ModuleError("psutil must be installed to use beetroot.mem.mem(). Use pip install psutil or pip install beetroot[ram].")
        
        yee = virtual_memory()
        return [yee.total, yee.used, yee.free]
        
    def swapmem(self):
        """Returns total, used and available swap memory."""
        
        try:
            from psutil import virtual_memory, swap_memory
            
        except (ModuleNotFoundError, ImportError):
            raise ModuleError("psutil must be installed to use beetroot.mem.mem(). Use pip install psutil or pip install beetroot[ram].")
        
        yee = swap_memory()
        return [yee.total, yee.used, yee.free]
                
mem = mem()