from datetime import date

class Nivel:
    """Representa un nivel educativo en el sistema académico."""

    def __init__(self, id, nivel):
        self._id = id
        self._nivel = nivel
        self._fecha_creacion = date.today().strftime('%Y-%m-%d')
        self._active = True

    @property
    def id(self):
        """Obtiene el identificador único del nivel."""
        return self._id

    @property
    def nivel(self):
        """Obtiene el nombre o descripción del nivel."""
        return self._nivel
    
    @property
    def fecha_creacion(self):
        """Obtiene la fecha de creación del nivel."""
        return self._fecha_creacion

    @property
    def active(self):
        """Obtiene el estado de actividad del nivel."""
        return self._active

    def activar(self):
        """Activa el nivel."""
        self._active = True

    def desactivar(self):
        """Desactiva el nivel."""
        self._active = False