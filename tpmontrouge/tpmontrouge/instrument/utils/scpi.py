def is_equal(a, b): 
    """ Test if the two values are equal within the SCPI convention

    For example : 
        'FIF'=='FIFty' shouf be true
    """
    # optimistic implementation
    if len(a)>len(b):
        b, a = a, b
    return b.lower().startswith(a.lower())
    

