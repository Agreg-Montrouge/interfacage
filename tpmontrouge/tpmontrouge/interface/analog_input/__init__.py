from ... import plot_engine

from . import analog_input

def get_ai_window(plot_engine=plot_engine, **kwd):
#    if plot_engine=='mpl':
#        return bode_plot_mpl.BodeWindows()
    if plot_engine=='pyqtgraph':
        return analog_input.AIWindow(**kwd)
    else:
        raise Exception('Plot engine {} not vailable'.format(plot_engine))
