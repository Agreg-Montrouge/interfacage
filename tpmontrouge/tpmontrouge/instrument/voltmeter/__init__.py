from ..connection.device_info import AllDevices

from .voltmeter import Voltmeter

# Here, you should import all the classes
from .agilent.generic import Agilent

def get_all_voltmeter():
    all_devices = AllDevices()
    return all_devices.get_all_connected_devices(Voltmeter)

#def gbf_factory(info):
#    """ Factory function to create a Voltmeter instance

#    parameter:
#        info : information such a visa_resource, an IP, ...
#     """
#    conn = auto_connect(info)
#    idn = conn.ask('*IDN?')
#    if "agilent" in idn.lower():
#        return Agilent(conn)
#    raise ValueError('Unkwown instrument with ID : {}'.format(idn))


#def _get_all_gbf():
#    for elm in get_all_connection():
#        try:
#            gbf_factory(elm)
#        except Exception:
#            pass
#        else:
#            yield elm

#def get_all_gbf():
#    return list(_get_all_gbf())
