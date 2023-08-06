import os
import subprocess

from .exception import *
from .objtype import *

class logger(object):
    def debug(self, msg):
        pass
    
    def warning(self, msg):
        pass
    
    def error(self, msg):
        print(msg)

class yt:
    """YT Trash yay"""
    def search(self, term):
        """Searches a term on youtube and returns first link.
        Beware of using this function, it may accidentally
        return an instance of "Search Domination", where
        one video (for example, extended version, 1hr, 8hrs, 10hrs)
        overtakes the original in search.
        If this happens, you may accidentally download the 10hr version
        of some music and DoS yourself. If this happens,
        just delete the .part file in the current directory."""

        try:
            from youtube_search import YoutubeSearch
            
        except (ModuleNotFoundError, ImportError):
            raise ModuleError("youtube-search must be installed to use beetroot.yt.search(). Try pip install youtube-search or pip install beetroot[yt].")
        
        results = YoutubeSearch(f"{term}", max_results=1).to_dict()
        results = results[0]
        u = "https://www.youtube.com" + results["url_suffix"]
        return u
    
    def dl(self, url, **kwargs):
        """Downloads video from link"""
        
        try:
            import youtube_dl
            
        except (ModuleNotFoundError, ImportError):
            raise ModuleError("youtube-dl must be installed. Use pip install youtube-dl or pip install beetroot[yt].")

        auds = ["mp3", "vorbis", "wav", "m4a", "aac", "flac", "opus"]
        defvids = ["mp4", "webm"]
        ffmvids = ["avi", "mkv", "mov", "flv", "aiff", "wma"]
        codec = kwargs.get(
            "fileformat",
            "webm"
        )
        
        fname = str(
            kwargs.get(
                "filename",
                "a"
            )
        )
        
        mode = kwargs.get(
            "playlist",
            False
        )
        
        exten = codec
        if codec == "ogg":
            codec = "vorbis"
        
        if objtype(mode) != "bool":
            raise InvalidTypeError("Argument \"playlist\" must be bool")
        
        if not codec in auds and not codec in defvids and not codec in ffmvids:
            raise InvalidFormat("Format \"" + codec + "\" is not a valid format.")
        
        if codec in auds:
            if not mode:
                ydl_opts = {
                    "format": "bestaudio/best",
                    "postprocessors": [
                        {
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": codec,
                            "preferredquality": "256"
                        }
                    ],
                    "logger": logger(),
                    "outtmpl": rf".\\{fname}.%(ext)s",
                    "noplaylist": True
                }
                
            elif mode:
                ydl_opts = {
                    "format": "bestaudio/best",
                    "postprocessors": [
                        {
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": codec,
                            "preferredquality": "256"
                        }
                    ],
                    "logger": logger(),
                    "outtmpl": rf".\\{fname}\\%(title)s.%(ext)s",
                    "noplaylist": False
                }
                
            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                    
            except Exception as error:
                raise FFmpegError("FFmpeg must be installed. There may be uncertainty, the original stack trace was \"" + str(error) + "\".")
        
        elif codec in defvids:
            if not mode:
                ydl_opts = {
                    "format": f"bestvideo[ext={codec}]+bestaudio[ext={codec}]/best[ext={codec}]/{codec}",
                    "outtmpl": rf".\\{fname}.{exten}",
                    "noplaylist": True,
                    "logger": logger(),
                }
                
            elif mode:
                ydl_opts = {
                    "format": f"bestvideo[ext={codec}]+bestaudio[ext={codec}]/best[ext={codec}]/{codec}",
                    "outtmpl": rf".\\{fname}\\%(title)s.{exten}",
                    "noplaylist": False,
                    "logger": logger(),
                }
                
            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                    
            except Exception as error:
                raise FFmpegError("FFmpeg must be installed. There may be uncertainty, the original stack trace was \"" + str(error) + "\".")
                
        elif codec in ffmvids:
            if not mode:
                ydl_opts = {
                    "format": f"bestvideo[ext=webm]+bestaudio[ext=webm]/best[ext=webm]/webm",
                    "outtmpl": rf".\\{fname}.webm",
                    "noplaylist": True,
                    "logger": logger(),
                }
                
            elif mode:
                ydl_opts = {
                    "format": f"bestvideo[ext=webm]+bestaudio[ext=webm]/best[ext=webm]/webm",
                    "outtmpl": rf".\\{fname}\\%(title)s.{exten}",
                    "logger": logger(),
                    "noplaylist": False
                }
                
            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                    
            except Exception as error:
                raise FFmpegError("FFmpeg must be installed. There may be uncertainty, the original stack trace was \"" + str(error) + "\".")
            
            result = subprocess.call(f"ffmpeg -i \"" + os.path.abspath(r".\\\\" + fname + r".webm") + "\" \"" + os.path.abspath(r".\\\\" + fname + "." + exten) + "\" -hide_banner -loglevel error")
            os.remove(rf".\\{fname}.webm")
            
            if result != 0:
                raise FFmpegError("FFmpeg must be installed. There may be uncertainty, subprocess.call() failed.")
                    
yt = yt()