import time
import io
import traceback


from pyqtgraph.Qt import QtGui

import sys

first_error = True
def my_excepthook(excType, excValue, tracebackobj):
    """
    Global function to catch unhandled exceptions.
    
    @param excType exception type
    @param excValue exception value
    @param tracebackobj traceback object
    """
    global first_error
    sys.__excepthook__(excType, excValue, tracebackobj)
    if not first_error:
        return
    first_error = False
    separator = '-' * 80
    notice = """ An unhandled exception occurred. Please report the problem
via email to <pierre.clade@upmc.fr>
"""
#    versionInfo="0.0.1"
    timeString = time.strftime("%Y-%m-%d, %H:%M:%S")

    tbinfofile = io.StringIO()
    traceback.print_tb(tracebackobj, None, tbinfofile)
    tbinfofile.seek(0)
    tbinfo = tbinfofile.read()

    errmsg = '%s: \n%s' % (str(excType), str(excValue))
    sections = [separator, timeString, separator, errmsg, separator, tbinfo]
    msg = '\n'.join(sections)

    errorbox = QtGui.QMessageBox()
    errorbox.setText(str(notice)+str(msg))
    errorbox.exec_()
    sys.exit(1)
    
def activate_error_dialog():
    sys.excepthook = my_excepthook

