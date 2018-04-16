Utilisation
===========

Exemple d'utilisation d'un voltmetre ::

    from tpmontrouge.instrument import get_all_connected_devices
    from tpmontrouge.instrument import Voltmeter

    all_voltmeters = get_all_connected_devices(kind_of_model=Voltmeter)

    inst = all_voltmeters[0].instrument

    print inst.get_value()

On peut alors laisser cours à son imagination pour enregistrer automatiquement des données ::

    from time import sleep

    data = []

    for _ in range(100):
        data.append(inst.get_value())
        sleep(1)

    data = np.array(data)

Dans cet exemple, il y a deux tâches qui sont automatisées : 1/ détecter les connections et installer l'interface qui permet de communiquer avec l'instrument et 2/ instancier la classe qui hérite de Voltmeter spécifique à la marque de l'instrument. 



Bas niveau
----------

    
On aurait pu le faire à la main ::

    # etape 1 
    import visa
    rm = visa.ResourceManager()
    print(rm.list_resources())
    conn = rm.open_resource('GPIB0::1')

    # etape 2
    from tpmontrouge.instrument import voltmeter

    inst = voltmeter.Agilent(conn)

Et si on connait uniquement l'addresse physique de l'instrument ::

    from tpmontrouge.instrument import auto_connect

    inst = auto_connect('GPIB0::1')




