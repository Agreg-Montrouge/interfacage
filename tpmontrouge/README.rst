Package Python pour les TPs de Montrouge
========================================

Ce package contient les librairies python pour le matériel de Montrouge

Il est partagé en plusieurs sous package : 

* Instrument : qui contient les drivers des differents instruments
* Analyse : package permettant d'analyser des données
* Experiment : dépend de analyse et instrument; permet de réaliser une experience, comme un diagramme de Bode
* Interface : interface graphique

Installation
------------

Il est possible d'installer le package à l'aide de la commande::

    pip install tpmontrouge

Interface
---------

Il existe une interface graphique pour faire un diagramme de Bode, pour visualiser un oscilloscope ou faire un table traçante. Elle est accessible, après installation, depuis une des commandes suivantes::

    tpmontrouge all
    tpmontrouge scope
    tpmontrouge bode

Il existe aussi des fichiers executables directement sous Windows. 


Instrument
----------

L'idée est d'avoir une interface commune à chaque type d'instrument, ce qui nécessite d'adapter ou d'écrire un driver specifique. Cette interface sera indépendante de la marque de l'instrument et de la connection utilisée. 

* Oscilloscope (scope)
* Générateur basse fréquence (gbf)

Exemple :: 
    
    from tpmontrouge.instrument import auto_connect

    scope = auto_connect('GPIB0::1::INSTR')

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

    scope = auto_connect('GPIB0::1::INSTR')
    gbf = auto_connect('GPIB0::10::INSTR')

    bode_experiment = BodeExperiment(gbf, scope, input_channel=scope.channel2, reference_channel=scope.channel1, disp=True)
    bode_plot = bode_experiment.record_bode_diagramm(start=10000, stop=10000000, step=30)

    bode_plot.plot()
    draw()

Version
-------

Principales modifications

* 2019.05 : Ajout d'un installateur windows. Amélioration de la vitesse de démarrage
* 2019.02 : Support pour les cartes NI et ajout d'une module d'acquisition continue
* 2024.10 : corrections de quelques bugs
* 2024.12 : update de la version de PyDAQmx dans la création de l'exe

Installation
------------

Créer un environnement conda. Par exemple ::

    conda create -n tpmontrouge python=3.12 matplotlib scipy
    conda activate tpmontrouge
    pip install PyQt5
    pip install pyqtgraph==0.11

Installation en mode développement ::

    pip install -e .

Tests
-----

Pour exécuter les tests unitaires ::

    # Linux/macOS
    ./run_tests.sh
    
    # Windows (PowerShell)
    .\run_tests.ps1
    
    # Ou directement
    python -m unittest discover

Note : Le package inclut des patches automatiques pour PyQtGraph afin d'assurer la compatibilité avec les versions récentes de NumPy et Qt.

CI/CD et builds automatiques
-----------------------------

Le projet utilise GitHub Actions pour automatiser les tests et la compilation des exécutables Windows.

**Tests automatiques**

À chaque push sur ``dev2026`` ou ``main``, les tests sont automatiquement exécutés sur :

* Linux (Ubuntu latest) avec Python 3.10, 3.11, 3.12
* Windows (latest) avec Python 3.10, 3.11, 3.12

Voir les résultats : https://github.com/PrepaAgregMontrouge/interfacage/actions

**Builds Windows automatiques**

Pour créer les exécutables Windows (.exe) et l'installateur :

1. Créer et pousser un tag de version ::

    git tag v2025.02.0
    git push origin v2025.02.0

2. GitHub Actions compile automatiquement :
   
   * ``interface-{version}-win64.exe`` : Interface graphique principale
   * ``empty_bode-{version}-win64.exe`` : Utilitaire de test
   * ``interface_agreg_setup-{version}.exe`` : Installateur Windows (Inno Setup)

3. Les exécutables sont disponibles :
   
   * **Artifacts** : Onglet Actions > Build > Download artifacts (conservés 90 jours)
   * **Release** : Onglet Releases avec notes de version automatiques

**Build manuel (déclenchement depuis GitHub)**

Aller sur : Actions > Build Windows Executables > Run workflow

**Développement local**

Pour compiler les .exe localement sur Windows ::

    # Installer PyInstaller et Inno Setup
    pip install pyinstaller
    choco install innosetup
    
    # Build interface.exe
    cd scripts
    pyinstaller -y interface.spec
    
    # Build installateur
    iscc interface_gui.iss

**Migration depuis Sconstruct**

L'ancien système de build via ``scons`` et la machine ``wannier`` est progressivement remplacé par GitHub Actions. Les deux systèmes cohabitent temporairement pour assurer la transition.

