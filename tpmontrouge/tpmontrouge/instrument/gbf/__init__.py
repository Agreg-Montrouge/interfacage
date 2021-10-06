from ..connection import auto_connect, get_all_connection
from .gbf import GBF

from .agilent.generic import Agilent
from .rigol.generic import Rigol


def gbf_factory(info):
    """ Factory function to create a GBF instance

    parameter:
        info : information such a visa_resource, an IP, ...
     """
    conn = auto_connect(info)
    idn = conn.ask('*IDN?')
    if "agilent" in idn.lower():
        return Agilent(conn)
    raise ValueError('Unkwown instrument with ID : {}'.format(idn))


def _get_all_gbf():
    for elm in get_all_connection():
        try:
            gbf_factory(elm)
        except Exception:
            pass
        else:
            yield elm

def get_all_gbf():
    return list(_get_all_gbf())
