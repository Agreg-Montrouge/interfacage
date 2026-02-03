from .instrument import get_all_connected_devices

__version__ = '2025.01.r0'

plot_engine = 'pyqtgraph'

# Appliquer les patches PyQtGraph pour la compatibilité avec NumPy/Qt récents
try:
    from .pyqtgraph_patches import apply_patches
    apply_patches()
except Exception as e:
    import warnings
    warnings.warn(f"Could not apply PyQtGraph patches: {e}")

# Filtrer certains warnings non critiques pour une meilleure lisibilité
import warnings

# Supprimer le warning matplotlib sur xlim non-positive (se produit lors de l'initialisation)
warnings.filterwarnings('ignore', message='Attempt to set non-positive xlim', category=UserWarning)

# Supprimer le warning NumPy/PyQtGraph sur dtype align
warnings.filterwarnings('ignore', message='.*align should be passed as Python or NumPy boolean.*', category=DeprecationWarning)

# Supprimer le warning multiprocessing fork (warning système qu'on ne peut pas corriger)
warnings.filterwarnings('ignore', message='.*This process.*is multi-threaded.*', category=DeprecationWarning)


