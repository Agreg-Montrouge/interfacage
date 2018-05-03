#from .scope import ScopeWindows

from ... import plot_engine
from . import scope_mpl
from . import scope_pyqtgraph

def get_scope_window(plot_engine=plot_engine, **kwd):
    if plot_engine=='mpl':
        return scope_mpl.ScopeWindows(**kwd)
    elif plot_engine=='pyqtgraph':
        return scope_pyqtgraph.ScopeWindows(**kwd)
    else:
        raise Exception('Plot engine {} not vailable'.format(plot_engine))
