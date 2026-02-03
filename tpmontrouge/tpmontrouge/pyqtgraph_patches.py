"""
Patches pour corriger les incompatibilités de PyQtGraph avec les versions récentes de NumPy/Qt.
Ces patches doivent être importés au début de l'application.
"""

def apply_patches():
    """Applique tous les patches nécessaires pour PyQtGraph"""
    try:
        import pyqtgraph
        from pyqtgraph import QtCore
        
        # Patch pour ThreadsafeTimer.start() qui reçoit des float au lieu d'int
        try:
            from pyqtgraph import ThreadsafeTimer
            original_start = ThreadsafeTimer.ThreadsafeTimer.start
            
            def patched_start(self, timeout=None):
                if timeout is not None:
                    timeout = int(timeout)
                return original_start(self, timeout)
            
            ThreadsafeTimer.ThreadsafeTimer.start = patched_start
        except Exception as e:
            print(f"Warning: Could not patch ThreadsafeTimer: {e}")
        
        # Patch pour GraphicsView.mouseMoveEvent() avec QPoint qui reçoit des float
        try:
            from pyqtgraph.widgets import GraphicsView
            from pyqtgraph import Point
            
            def patched_mouseMoveEvent(self, ev):
                """Version patchée de mouseMoveEvent qui convertit les floats en int"""
                # Implémentation complète sans appel à l'originale pour éviter les erreurs
                if hasattr(self, 'lastMousePos') and self.lastMousePos is not None:
                    try:
                        # Convertir lastMousePos en entiers avant de créer QPoint
                        lastMousePos = (int(self.lastMousePos[0]), int(self.lastMousePos[1]))
                        delta = Point(ev.pos() - QtCore.QPoint(*lastMousePos))
                        
                        # Appeler le reste de la méthode manuellement
                        if hasattr(self, 'mouseDragEnabled') and self.mouseDragEnabled:
                            self.translate(delta)
                    except (TypeError, AttributeError, IndexError):
                        # Si quelque chose échoue, on ne fait rien plutôt que de crasher
                        pass
                
                # Mettre à jour lastMousePos avec les nouvelles coordonnées
                self.lastMousePos = (ev.pos().x(), ev.pos().y())
            
            GraphicsView.GraphicsView.mouseMoveEvent = patched_mouseMoveEvent
        except Exception as e:
            print(f"Warning: Could not patch GraphicsView.mouseMoveEvent: {e}")
            
    except ImportError:
        print("Warning: PyQtGraph not installed, patches not applied")
