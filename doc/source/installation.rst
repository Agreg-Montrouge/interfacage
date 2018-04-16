Installation
============

Installer anaconda. Il faut ensuite utiliser une console dans laquelle anaconda est activée . Sous windows utilisé la console disponible dans le sous-menu anaconda. Sous linux, il faut suivre les indications donnée au moment de l'installation. Si anaconda n'est pas activé par défaut, il faut faire quelque chose comme ``source /path/to/anaconda/bin/activate root``. 

Ensuite, il faut installer les packages suivants en utilisant la commande ``conda install xxx``: 

- numpy
- cached-property
- pyqtgraph
- scipy
- matplotlib
- pyvisa

Ensuite, il faut télécharger le package tpmontrouge, ce qui peut se faire depuis la page github soit en téléchargeant le zip, soit en utilisant git. Il faut executer la commande : 

    pip install tpmontrouge

Normalement, la librairie sera accessible depuis python et les scripts aussi. On pourra donc lancer la commande : 

    tpmontouge-all 

qui devrait ouvrir l'interface graphique avec toutes les expériences. 


