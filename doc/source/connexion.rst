=========================
Connexion à un instrument
=========================

Il existe plusieurs type de connexion : GPIB, RS232 (série), USB ou ethernet. Sous windows, la plupart des connexions sont gérées par VISA, ce qui simplifie le problème. 

Méthode automatique
===================

Chaque instrument est défini par une chaine de caractère. A partir de cette chaîne, on peut déterminer automatiquement le type de connexion (voir la suite) et l'ouvrir. Cette fonction se trouve dans le module :mod:`tpmontrouge.instrument.connection.auto_connect`. 

Par exemple ::

    my_instrument = auto_connect("GPIB0::1::INSTR")

Lister les instruments
======================

On peut lister tous les instruments à l'aide de la ligne de la fonction  :: 

    from tpmontrouge.instrument import AllDevices

    all_devices = AllDevices()
    print(all_devices.list_of_devices)

On peut aussi filtrer par type d'instrument : 

    print(list(all_devices.get_all_connected_devices(Scope)))



VISA
====

Sous windows, en générale il est possible de connecter un instrument en utilisant VISA. C'est une machine à gaz fournit par National Instruments. Un insrument est alors repéré par un nom de resource, souvent du type : ``GPIB0::1::INSTR`` pour un instrument GPIB ou ``USB0::0x1AB1::0x0640::DG5A142600040::INSTR`` pour un instrument USB. Il est aussi possible de connecter un instrument en ethernet. Pour connaitre le nom de la resource, on peut soit utiliser python (ci-dessous) ou le logiciel NI-MAX

Pour utiliser driver de National Instruments sous Python, il faut installer le package pyvisa (``pip install pyvisa``)

Pour ouvrir un connexion on utilise les commandes suivante :: 

    import visa

    rm = visa.ResourceManager()
    conn = rm.open_resource("GPIB0::1::INSTR")

Notez qu'il est possible de lister toutes les resources disponibles à l'aide de la commande ``rm.list_resources()``

..note ::

    En théorie, il est possible d'installer VISA sous Linux. Mais, en pratique il faut faire attention d'avoir la version bein spécifique du noyau pour lequel le driver a été installé. 



Serial
======

On parle de port série ou RS232. 

Sous windows, on peut utiliser soit VISA soit le modue serial de Python que l'on utilisera sous Linux. Cette section inclu aussi les instrument série équipée d'un adptateur USB-RS232 ::

    import serial

    conn = serial.Serial('/dev/ttyUSB0')

USBTMC
======

(Utiliser VISA sous windows)

C'est le cas de instruments Rigol connecté en USB. Une resource ``/dev/usbtmc`` est crée. Il faut faire attention aux droit d'accés si on n'est pas root. 

Voir le module :mod:`tpmontrouge.instrument.connection.usbtmc`. 


VXI11
=====

(Utiliser VISA sous windows)

Pour les connexion ethernet de certains instruments (en particulier les oscillos Tektronix). ::

    pip install python-vxi11

    conn = vxi11.Instrument('adresse.ip')


