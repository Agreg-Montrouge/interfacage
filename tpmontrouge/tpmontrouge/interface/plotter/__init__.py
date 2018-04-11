from ... import plot_engine

from . import plotter

def get_plotter_window(plot_engine=plot_engine):
#    if plot_engine=='mpl':
#        return bode_plot_mpl.BodeWindows()
    if plot_engine=='pyqtgraph':
        return plotter.PlotterWindow()
    else:
        raise Exception('Plot engine {} not vailable'.format(plot_engine))
