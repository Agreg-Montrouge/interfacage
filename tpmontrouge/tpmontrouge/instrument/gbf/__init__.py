from ..connection import auto_connect
from .agilent.generic import Agilent


def gbf_factory(info):
    """ Factory function to create a GBF instance

    parameter:
        info : information such a visa_resource, an IP, ...
     """
    conn = auto_connect(info)
    idn = conn.ask('*IDN?')
    if agilent in idn.lower():
        return Agilent(conn)
    raise ValueError('Unkwown instrument with ID : {}'.format(idn))


