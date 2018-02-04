from .main import main

from ... import plot_engine
from . import bode_plot_mpl
from . import bode_plot_pyqtgraph

def get_bode_window(plot_engine=plot_engine):
    if plot_engine=='mpl':
        return bode_plot_mpl.BodeWindows()
    elif plot_engine=='pyqtgraph':
        return bode_plot_pyqtgraph.BodeWindows()
    else:
        raise Exception('Plot engine {} not vailable'.format(plot_engine))
