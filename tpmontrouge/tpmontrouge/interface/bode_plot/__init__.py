from ... import plot_engine
from . import bode_plot_mpl
from . import bode_plot_pyqtgraph

def get_bode_window(plot_engine=plot_engine, **kwd):
    if plot_engine=='mpl':
        return bode_plot_mpl.BodeWindows(**kwd)
    elif plot_engine=='pyqtgraph':
        return bode_plot_pyqtgraph.BodeWindows(**kwd)
    else:
        raise Exception('Plot engine {} not vailable'.format(plot_engine))
