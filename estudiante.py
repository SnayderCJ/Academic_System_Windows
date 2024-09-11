from datetime import date

class Estudiante:
    """Representa a un estudiante en el sistema académico."""

    def __init__(self, cedula, nombre, apellido, fecha_nacimiento, active=True):
        self._cedula = cedula
        self._nombre = nombre
        self._apellido = apellido
        self._fecha_nacimiento = fecha_nacimiento
        self._fecha_creacion = date.today()
        self._active = active

    @property
    def id(self):
        """Obtiene el identificador único del estudiante."""
        return self._id

    @property
    def nombre(self):
        """Obtiene el nombre del estudiante."""
        return self._nombre

    @property
    def apellido(self):
        """Obtiene el apellido del estudiante."""
        return self._apellido

    @property
    def fecha_nacimiento(self):
        """Obtiene la fecha de nacimiento del estudiante."""
        return self._fecha_nacimiento
    
    @property
    def fecha_creacion(self):
        """Obtiene la fecha de creación del registro del estudiante."""
        return self._fecha_creacion

    @property
    def active(self):
        """Obtiene el estado de actividad del estudiante."""
        return self._active
    