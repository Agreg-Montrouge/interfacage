Package Python pour les TPs de Montrouge
========================================

Ce package contient les librairies python pour le matériel de Montrouge

Il est partagé en plusieurs sous package : 

* Instrument : qui contient les drivers des differents instruments
* Analyse : package permettant d'analyser des données
* Experiment : dépend de analyse et instrument : permet de réaliser une experience, comme un diagramme de Bode
* Interface : inerface graphique

Installation
------------

Il est possible d'installer le package à l'aide de la commande::

    pip install tpmontrouge

Interface
---------

Il existe une interface graphique pour faire un diagramme de Bode et pour visualiser un oscilloscope. Elle est accessible, après installation, depuis une des commandes suivantes::s

    tpmontrouge full-gui
    tpmontrouge scope
    tpmontrouge bode

Il existe aussi des fichiers executable directement sous Windows. 


Instrument
----------

L'idée est d'avoir une interface commune à chaque type d'instrument, ce qui nécessite d'adapter ou d'écrire un driver specifique. Cette interface sera indépendante de la marque de l'instrument et de la connection utilisée. 

* Oscilloscope (scope)
* Générateur basse fréquence (gbf)

Exemple :: 
    
    from tpmontrouge.instrument import scope_factory

    scope = scope_factory('GPIB0::1::INSTR')

    scope.autoset()
    wfm = scope.channel1.get_waveform()
    wfm.plot()

    scope.channel[1].scale = .2


Analyse 
-------

Librairie permettant d'enregistrer et analyser des données dans un but précis. 

Exemple ::

    from tpmontrouge.experiment.bode_plot import BodePoint # point sur le diagramme de Bode

    t = np.linspace(0, 1, 10001)
    ref = np.sin(2*np.pi*freq*t)
    signal = .2*np.sin(2*np.pi*freq*t+1.54)
    point = BodePoint(t, ref, signal, freq=freq)
    print(point.delta_phi)
    print(point.gain)



Experiment
----------

L'objectif de ce sous package est de fournir des fonctions simplifiées pour réaliser une expérience. 

Par exemple :: 

    from tpmontrouge.instrument import scope_factory, gbf_factory
    from tpmontrouge.experiment import BodeExperiment

    scope = scope_factory('GPIB0::1::INSTR')
    gbf = gbf_factory('GPIB0::10::INSTR')

    bode_experiment = BodeExperiment(gbf, scope, input_channel=scope.channel2, reference_channel=scope.channel1, disp=True)
    bode_plot = bode_experiment.record_bode_diagramm(start=10000, stop=10000000, step=30)

    bode_plot.plot()
    draw()
