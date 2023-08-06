import math as mmath

from decimal import Decimal as d

from .exception import *
from .objtype import objtype

class math:
    def __init__(self):
        self.mole = self.prec(
            self.prec(
                6.023
            ) * self.prec(
                10
            ) ** self.prec(
                23
            )
        )
        
    def prec(self, n):
        return d(str(n))
    
    def increment(self, n):
        try:
            return n + 1
        
        except TypeError:
            raise InvalidTypeError("Object " + objtype(n) + " is not incrementable.")
            
    def double(self, n):
        try:
            return n * 2
        
        except TypeError:
            raise InvalidTypeError("Object " + objtype(n) + " is not incrementable.")
    
    def square(self, n):
        try:
            return n ** 2
        
        except TypeError:
            raise InvalidTypeError("Object " + objtype(n) + " is not incrementable.")
        
    def sqrt(self, n):
        try:
            if n == 0:
                return 0
            
            elif n < 0:
                return (-n ** 0.5) * 1j
            
            elif n > 0:
                return n ** 0.5
        
        except TypeError:
            raise InvalidTypeError("Object " + objtype(n) + " is not incrementable.")
    
    def factorial(self, n):
        if objtype(n) == "complex":
            raise NumberError("Complex numbers are not supported yet.")
        
        if n == 0:
            return 1
        
        elif n > 0:
            return mmath.gamma(n + 1)
        
    def b_round(self, n, a=0, *args, **kwargs):
        """Better rounding. More accurate."""
        return float(round(self.prec(n), a, *args, **kwargs))
    
    def isPrime(self, n):
        if n > 1:
            for i in range(2, int(n / 2) + 1):
                if n % i == 0:
                    return False
                
            else:
                return True
            
        else:
            return False
        
math = math()
