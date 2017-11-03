from .visa import visa

def get_all_connection():
    out = []
    if visa is not None:
        out.extend(visa.rm.list_resources())
    return out
