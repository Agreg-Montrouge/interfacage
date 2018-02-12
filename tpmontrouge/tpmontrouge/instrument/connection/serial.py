try:
    from ._serial import Serial, auto_detect
except ImportError:
    Serial = None
