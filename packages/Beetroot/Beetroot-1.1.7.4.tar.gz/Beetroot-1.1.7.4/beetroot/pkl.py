from .exception import *

class pkl:
    def pkl(self, fpath, obj):
        """Pickles an object into a .pkl."""
        
        import os
        
        try:
            import cPickle as pickle
            
        except (ModuleNotFoundError, ImportError):
            import pickle
            
        with open(fpath, "wb") as f:
            pickle.dump(obj, f)
            f.close()
            
        return 0
    
    def unpkl(self, fpath):
        """Unpickles data from a .pkl file."""
        
        import os
        
        try:
            import cPickle as pickle
            
        except (ModuleNotFoundError, ImportError):
            import pickle
            
        with open(fpath, "rb") as f:
            out = pickle.load(f)
            f.close()
            return out
        
pkl = pkl()