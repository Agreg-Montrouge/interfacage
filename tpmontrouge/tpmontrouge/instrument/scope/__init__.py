from ..connection import auto_connect, get_all_connection
from .tektronix.generic import Tektronix


def scope_factory(info):
    """ Factory function to create a Scope instance

    parameter:
        info : information such a visa_resource, an IP, ...
     """
    conn = auto_connect(info)
    idn = conn.ask('*IDN?')
    if "tektronix" in idn.lower():
        return Tektronix(conn)
    raise ValueError('Unkwown instrument with ID : {}'.format(idn))


def _get_all_scopes():
    for elm in get_all_connection():
        try:
            scope_factory(elm)
        except Exception:
            pass
        else:
            yield elm

def get_all_scopes():
    return list(_get_all_gbf())
