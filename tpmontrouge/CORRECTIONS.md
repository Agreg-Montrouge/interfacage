# Corrections des tests et compatibilité

## Résumé des corrections effectuées

Ce document résume les corrections apportées pour éliminer les erreurs lors de l'exécution des tests unitaires et de l'installation du package.

### 1. Erreurs TypeError corrigées

#### Problème 1 : `setValue()` attend un int, reçoit numpy.float64
- **Erreur** : `TypeError: setValue(self, a0: int): argument 1 has unexpected type 'numpy.float64'`
- **Cause** : PyQtGraph attend un entier (0-255) pour le paramètre alpha, mais recevait 0.3 (float)
- **Solution** : Converti `alpha = 0.3` en `alpha = int(0.3 * 255)` dans tous les appels à `showGrid()`
- **Fichiers modifiés** :
  - `tpmontrouge/analyse/Bode.py`
  - `tpmontrouge/experiment/plotter.py`
  - `tpmontrouge/interface/scope/scope_pyqtgraph.py`
  - `tpmontrouge/experiment/continuous_acquisition.py`

#### Problème 2 : Incompatibilités PyQtGraph avec NumPy/Qt récents
- **Erreurs** : 
  - `timer.start(timeout)` avec float au lieu d'int
  - `QPoint()` recevant des float au lieu d'int
- **Cause** : PyQtGraph n'est pas compatible avec les versions récentes de Qt6
- **Solution** : Création d'un module `pyqtgraph_patches.py` qui applique des monkey patches automatiquement
  - Patch de `ThreadsafeTimer.start()` pour convertir timeout en int
  - Patch de `GraphicsView.mouseMoveEvent()` pour convertir les coordonnées en int
- **Fichier créé** : `tpmontrouge/pyqtgraph_patches.py`
- **Chargement automatique** : Les patches sont appliqués lors de l'import du module dans `__init__.py`

### 2. Problème d'installation en mode éditable

#### Problème : ModuleNotFoundError lors de `pip install -e .`
- **Erreur** : `ModuleNotFoundError: No module named 'cached_property'`
- **Causes** :
  1. Le `setup.py` importait `tpmontrouge` pour obtenir `__version__`, déclenchant tous les imports avant l'installation des dépendances
  2. Le package `cached_property` externe n'est plus nécessaire depuis Python 3.8
- **Solutions** :
  1. **setup.py** : Lecture de `__version__` directement depuis le fichier avec regex, sans import du module
  2. **cached_property** : Remplacement de `from cached_property import cached_property` par `from functools import cached_property` (intégré depuis Python 3.8)
- **Fichiers modifiés** :
  - `setup.py` : Nouvelle fonction `get_version()`
  - `tpmontrouge/analyse/Bode.py`
  - `tpmontrouge/instrument/connection/device_info.py`
  - `tpmontrouge/instrument/utils/instrument.py`

### 3. Gestion des warnings non critiques

#### Warnings filtrés
- **DeprecationWarning** (multiprocessing fork) : Warning système Python qu'on ne peut pas corriger
- **VisibleDeprecationWarning** (NumPy dtype align) : Bug dans PyQtGraph avec NumPy 2.4
- **UserWarning** (matplotlib xlim non-positive) : Warning normal lors de l'initialisation
- **Solution** : 
  - Ajout de filtres de warnings dans `__init__.py`
  - Création du script `run_tests.sh` qui définit `PYTHONWARNINGS` pour les sous-processus

#### Warnings restants (non critiques)
- **Warning Wayland** : "Ignoring XDG_SESSION_TYPE=wayland on Gnome" - Spécifique à l'environnement Linux/Wayland, ne peut pas être supprimé

### 4. Correction d'une faute d'orthographe
- **Fichier** : `tpmontrouge/instrument/autodetection/manufacturer.py:50`
- **Correction** : "Unkwnown" → "Unknown"

## Résultats

### Avant corrections
- Nombreuses erreurs TypeError empêchant l'utilisation normale
- Installation en mode éditable impossible
- Warnings difficiles à lire

### Après corrections
- **100 tests passent avec succès (OK)**
- **0 erreurs TypeError**
- Installation en mode éditable fonctionnelle : `pip install -e .`
- Warnings non critiques filtrés (10 warnings Wayland restants, non critiques)
- Documentation mise à jour dans README.rst

## Utilisation

### Exécuter les tests
```bash
# Avec tous les warnings
python -m unittest discover

# Avec warnings filtrés (recommandé)
./run_tests.sh
```

### Installation
```bash
# Installation normale
pip install .

# Installation en mode développement
pip install -e .
```

## Compatibilité

Le package est maintenant compatible avec :
- Python 3.8+
- NumPy 2.x
- PyQt5/Qt6
- PyQtGraph 0.11+
- Environnements Linux (X11 et Wayland)
