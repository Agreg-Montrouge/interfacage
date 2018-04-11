from pyqtgraph.Qt import QtCore, QtGui

from ..instrument.autodetection.manufacturer import list_of_manufacturer
from ..instrument.scope import Scope
from ..instrument.gbf import GBF
from ..instrument.voltmeter import Voltmeter
from .. import __version__


info="""
<div style="font-size:13pt">
<h1>Interface </h1>

<p>Cette application a été écrite en Python. Elle permet d'interfacer des instruments et d'automatiser des expériences.</p>

<h2>Liste des manips possibles </h2>
<ul>
<li>Diagramme de Bode</li>
<li>Suivu d'un oscilloscope</li>  
</ul>

<h2>Liste des oscilloscopes compatibles</h2>
{scope_html}

<h2>Liste des GBF compatibles</h2>
{gbf_html}

<h2>Liste des enregistreur compatibles</h2>
{voltmeter_html}


<h2>Crédits / Licence </h2>
<p> Application créée par Pierre Cladé pour le Département de Physique de l'École Normale Supérieure. </p>

<p> Ce logiciel est disponible sous licence MIT ou toute autre licence obtenue par l'auteur.</p>

<p style="font-size:10pt;" align="right"><i> Version {__version__} </i></p>
</div>
"""

scopes = list_of_manufacturer.get_all_models(Scope)
gbf = list_of_manufacturer.get_all_models(GBF)
voltmeters = list_of_manufacturer.get_all_models(Voltmeter)

scope_html = """<ul>\n"""
for name, liste in scopes.items():
    for elm in liste:
        scope_html += '<li>{name} : {elm}*</li>\n'.format(**locals())
scope_html += '</ul>'


gbf_html = """<ul>\n"""
for name, liste in gbf.items():
    for elm in liste:
        gbf_html += '<li>{name} : {elm}*</li>\n'.format(**locals())
gbf_html += '</ul>'

voltmeter_html = """<ul>\n"""
for name, liste in voltmeters.items():
    for elm in liste:
        voltmeter_html += '<li>{name} : {elm}*</li>\n'.format(**locals())
voltmeter_html += '</ul>'


info = info.format(**locals())


def get_info():
    box = QtGui.QTextEdit(info)
    box.setReadOnly(True)
    return box
