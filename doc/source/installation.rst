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

On peut aussi utiliser la librairie, par exemple ::

    from tpmontrouge.instrument import get_all_connected_devices
    from tpmontrouge.instrument import Voltmeter

    all_voltmeters = get_all_connected_devices(kind_of_model=Voltmeter)

    inst = all_voltmeters[0].instrument

    print inst.get_value()

Dans cet exemple, il y a deux tâches qui sont automatisées : 1/ détecter les connections et installer l'interface qui permet de communiquer avec l'instrument et 2/ instancier la classe qui hérite de Voltmeter spécifique à la marque de l'instrument. 
    
On aurait pu le faire à la main ::

    # etape 1 
    import visa
    rm = visa.ResourceManager()
    print(rm.list_resources())
    conn = rm.open_resource('GPIB0::1')

    # etape 2
    from tpmontrouge.instrument import voltmeter

    inst = voltmeter.Agilent(conn)

Et si on connait uniquement l'addresse physique de l'instrument : 

    from tpmontrouge.instrument import auto_connect

    inst = auto_connect('GPIB0::1')


