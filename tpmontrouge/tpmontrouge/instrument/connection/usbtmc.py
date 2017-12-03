from sys import platform

if platform=="linux" or platform=="linux2":
    from ._usbtmc import *
else:
    USBTMC = None
