from ..connection import auto_connect
from .tektronix.generic import Tektronix


def scope_factory(info):
    """ Factory function to create a Scope instance

    parameter:
        info : information such a visa_resource, an IP, ...
     """
    conn = auto_connect(info)
    idn = conn.ask('*IDN?')
    if tektronix in idn:
        return Tektronix(conn)
    raise ValueError('Unkwown instrument with ID : {}'.format(idn))



