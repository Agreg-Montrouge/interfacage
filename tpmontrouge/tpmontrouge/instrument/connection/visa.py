from __future__ import absolute_import

try:
    import visa 
except ImportError:
    visa = None


if visa is not None:
    rm = visa.ResourceManager()
    open_resource = rm.open_resource
else:
    def open_resource(*args, **kwd):
        raise Exception('Visa not installed on your computer') 
