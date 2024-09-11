from datetime import date

class Asignatura:
    """Representa una asignatura o materia dentro de un nivel educativo."""

    def __init__(self, id, descripcion, nivel, active):
        self._id = id
        self._descripcion = descripcion
        self._nivel = nivel
        self._fecha_creacion = date.today()
        self._active = active

    @property
    def id(self):
        """Obtiene el identificador único de la asignatura."""
        return self._id

    @property
    def descripcion(self):
        """Obtiene la descripción de la asignatura."""
        return self._descripcion

    @property
    def nivel(self):
        """Obtiene el nivel educativo al que pertenece la asignatura."""
        return self._nivel
    
    @property
    def fecha_creacion(self):
        """Obtiene la fecha de creación del registro de la asignatura."""
        return self._fecha_creacion
    
    @property
    def active(self):
        """Obtiene el estado de actividad de la asignatura."""
        return self._active
    
    def activar(self):
        """Activa el nivel."""
        self._active = True

    def desactivar(self):
        """Desactiva el nivel."""
        self._active = False
