from .exception import *
from .objtype import objtype

class obf:
    """Obfuscation class, it kinda sucks, for good python
    obfuscation, use beetroot.cython()."""
    def obfuscate(self, str_):
        """Minorly obfuscates a string. While it is unreadable,
        don't expect this to stand up to anyone with a bit
        of python knowledge"""
        
        import lzma
        import codecs
        import base64
        
        try:
            if objtype(str_) == "bytes":
                return lzma.compress(
                    base64.a85encode(
                        codecs.encode(
                            str(
                                str_.decode(
                                    "iso-8859-1"
                                )
                            )[::-1],
                            "rot-13"
                        ).encode(
                            "utf-8"
                        )
                    )
                ).decode(
                    "iso-8859-1"
                )[::-1].encode(
                    "iso-8859-1"
                )
            
            else:
                return lzma.compress(
                    base64.a85encode(
                        codecs.encode(
                            str(
                                str_
                            )[::-1],
                            "rot-13"
                        ).encode(
                            "utf-8"
                        )
                    )
                ).decode(
                    "iso-8859-1"
                )[::-1]
        
        except UnicodeDecodeError:
            return lzma.compress(
                base64.a85encode(
                    codecs.encode(
                        str(
                            str_
                        )[::-1],
                        "rot-13"
                    ).encode(
                        "iso-8859-1"
                    )
                )
            ).decode(
                "iso-8859-1"
            )[::-1]
        
    def deobfuscate(self, str_):
        """Unobfuscates a string obfuscated by beetroot.strobfuscate()"""
        
        import lzma
        import codecs
        import base64
        
        try:
            if objtype(str_) == "bytes":
                return codecs.encode(
                    base64.a85decode(
                        lzma.decompress(
                            str_[::-1]
                        )
                    ).decode(
                        "utf-8"
                    ),
                    "rot-13"
                )[::-1].encode(
                    "utf-8"
                )
            
            else:
                return codecs.encode(
                    base64.a85decode(
                        lzma.decompress(
                            str_[::-1].encode(
                                "iso-8859-1"
                            )
                        )
                    ).decode(
                        "utf-8"
                    ),
                    "rot-13"
                )[::-1]
        
        except UnicodeDecodeError:
            return codecs.encode(
                base64.a85decode(
                    lzma.decompress(
                        str_[::-1].encode(
                            "iso-8859-1"
                        )
                    )
                ).decode(
                    "iso-8859-1"
                ),
                "rot-13"
            )[::-1]
        
obf = obf()