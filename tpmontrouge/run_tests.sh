#!/bin/bash
# Script pour exécuter les tests avec suppression des warnings non critiques

# Supprimer les warnings Python non critiques
export PYTHONWARNINGS="ignore::DeprecationWarning,ignore::UserWarning"

# Exécuter les tests
python -m unittest discover "$@"
