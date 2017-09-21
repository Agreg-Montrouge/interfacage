Package Python pour les TPs de Montrouge
========================================

Ce package contient les librairies python pour le matériel de Montrouge

Il est partagé en plusieurs sous package : 

* Instrument : qui contient les drivers des differents instruments
* Analyse : package permettant d'analyser des donner
* Experiment : dépent de analyse et instrument : permet de réaliser une experience, comme un diagramme de Bode

Instrument
----------

L'idée est d'avoir une interface commune à chaque type d'instrument, ce qui necessite d'adapter ou d'écrire un driver specifique. Cette interface sera indépendante de la marque et de la connection utilisée. 

    * Oscilloscope (scope)
    * Générateur basse fréquence (gbf)

Analyse 
-------

Librairie permettant d'enregistrer et analyser des donnée dans un but précis. 

Experiment
----------

L'objectif de ce sous package est de fournir des fonctions simplifiée pour réaliser une expérience. 

Par exemple : 

    from tpmontrouge.instrument import scope_factory, gbf_factory
    from tpmontrouge.experiment import BodeExperiment

    scope = scope_factory('GPIB0::1::INSTR')
    gbf = gbf_factory('GPIB0::10::INSTR')

    bode_experiment = BodeExperiment(gbf, scope, input_channel=scope.channel2, reference_channel=scope.channel1, disp=True)
    bode_plot = bode_experiment.record_bode_diagramm(start=10000, stop=10000000, step=30)

    bode_plot.plot()
    draw()
