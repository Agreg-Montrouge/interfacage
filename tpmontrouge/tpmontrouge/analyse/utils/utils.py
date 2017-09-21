from numpy import pi, array, cumsum, concatenate

def mod_2pi(val):
    return (val+pi)%(2*pi) - pi

def unwrap_phase(a):
    a = array(a)
    diff = mod_2pi(a[1:] - a[:-1])
    initial_value = mod_2pi(a[0])
    return concatenate(([initial_value], initial_value+cumsum(diff)))
