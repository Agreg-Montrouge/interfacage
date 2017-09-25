===================
Créer un instrument
===================

Principes
=========

Il y a deux difficultés : 1/ on souhaite que l'interface soit la même quelque soit la marque de l'instrument. 2/ on souhaite que le driver spécifique à une marque fonctionne indépendament du type de connection (GPIB, ethernet, ...). On suppose ici que l'on dispose d'une interface par passage de message (du type SCPI - Standard command programming interface). 

Il y a donc plusieurs niveaux : 

  * la connection : elle fournit les méthode ``write``, ``read`` et ``ask``.

  * le driver bas niveau de l'instrument : il doit créer un certain nombre de méthode de base. 

  * le driver haut niveau - qui normalement est commun à tous les instruments. Il fournit une interface utilisateur simple d'utilisation. 

Prenons l'exemple d'un oscilloscope Tektronix. On va le connecter en visa. ::

    import visa
    rm = visa.ResourceManager()
    print(rm.list_resources())
    conn = rm.open_resource('GPIB0::1')

Grace à cette connection, on va pouvoir communiquer avec l'oscilloscope. Par exemple :: 

    conn.write('AUTOSET EXECUTE')
    conn.ask('CH1:SCALE 1')
    conn.ask('CH1:SCALE?')

Le driver de bas niveau va réaliser l'interface entre une fonction Python et ces chaînes de caractères. Par exemple :: 

    def get_channel_scale(conn, channel):
        scale = conn.ask('CH{}:SCALE?'.format(channel))
        return float(scale)

Le tout se fait avec des méthode d'objet.  Il existe des méthode pour simplifier faire des conversion automatiquement. Par exemple ::

    def get_horizontal_scale(com):
        return self.scpi_ask_for_float("HORizontal:SCAle")


Enfin, l'objet de haut niveau va fournir l'interface commune à tout le monde. Elle offre un arbre de commande simple a utilisé, basé sur des ``property`` :: 

    scope.horizontal.scale = .5 # call scope.set_horizontal_scale(.5)


Concretement
============

La seule chose qu'il va falloir écrire (ou adapter) est la deuxième étape qui dépend de l'appareil que l'on utilise. Pour se faire, le plus simple est de regarder l'ensemble des méthodes qui sont définies dans l'instrument de test et de les écrire.

Test unitaire
==============

Il existe un test unitaire effectué sur un instrument fictif. Il fait parti de la suite de test du package. On peut créer un test spécifique pour un instrument. Il faut simplement éviter de lui donner un nom commençant par ``test``, afin qu'il ne soit pas exécuté automatiquement. 

On exectute alors directement le module :: 

    python -m tpmontrouge.instrument.scope.test.tektronix 'GPIB0::1::INSTR'


