from .visa import visa

def get_all_connection():
    out = []
    if visa is not None:
        from .visa import rm
        out.extend(rm.list_resources())
    return out
