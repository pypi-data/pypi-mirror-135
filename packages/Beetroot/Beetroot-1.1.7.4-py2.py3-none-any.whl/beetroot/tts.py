from .exception import *
from .objtype import objtype

class tts:
    """tts yay"""
    def __init__(self):
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            
        except (ModuleNotFoundError, ImportError):
            pass
        
    def say(self, str_):
        """Say something, Beetroot"""
        try:
            if objtype(str_) == "bytes":
                self.engine.say(str_.decode("iso-8859-1"))
                
            else:
                self.engine.say(str(str_))
                
            self.engine.runAndWait()
            
        except (NameError, AttributeError):
            raise ModuleError("You need to install pyttsx3 to use beetroot.tts functions. Try \"pip install pyttsx3\".")
    
    def changeRate(self, rate):
        """Say things faster/slower, Beetroot"""
        try:
            self.engine.setProperty("rate", int(round(float(rate))))
            
        except (NameError, AttributeError):
            raise ModuleError("You need to install pyttsx3 to use beetroot.tts functions. Try \"pip install pyttsx3\".")
        
        except ValueError:
            raise InvalidTypeError("Argument \"rate\" must be int or float")
        
    def changeVoice(self, voice):
        """Say things in different voices, Beetroot
        (you can even do different languages if you install them
        on windows, although I'm not sure how you do it on *nix
        cuz I don't have any *nix computers or VMs.)"""
        try:
            voices = self.engine.getProperty("voices")
            self.engine.setProperty("voice", voices[int(round(float(voice)))].id)
        
        except (NameError, AttributeError):
            raise ModuleError("You need to install pyttsx3 to use beetroot.tts functions. Try \"pip install pyttsx3\".")
        
        except IndexError:
            raise InvalidVoiceError("That voice id doesn't exist.")
        
        except ValueError:
            raise InvalidTypeError("Argument \"voice\" must be int or float")
        
    def changeVolume(self, volume):
        """Talk Louder/Quieter, Beetroot"""
        try:
            self.engine.setProperty("volume", float(voice))
            
        except (NameError, AttributeError):
            raise ModuleError("You need to install pyttsx3 to use beetroot.tts functions. Try \"pip install pyttsx3\".")
        
        except ValueError:
            raise InvalidTypeError("Argument \"volume\" must be int or float")

tts = tts()