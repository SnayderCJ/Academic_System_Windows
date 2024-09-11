from datetime import date

# Clase que representa un profesor.
class Profesor:
    def __init__(self, cedula, nombre, active):
        self._cedula = cedula  # Identificador único para el profesor.
        self._nombre = nombre  # Nombre del profesor.
        self._fecha_creacion = date.today().strftime('%Y-%m-%d')  # Fecha de creación del registro del profesor, se asigna la fecha actual.
        self._active = active  # Estado de actividad del profesor (True o False).

    @property
    def cedula(self):
        """Obtiene el identificador único del profesor."""
        return self._cedula

    @property
    def nombre(self):
        """Obtiene el nombre del profesor."""
        return self._nombre
    
    @nombre.setter
    def nombre(self, nuevo_nombre):
        """Establece el nombre del profesor."""
        self._nombre = nuevo_nombre # Actualiza el nombre del profesor.
    
    @property
    def fecha_creacion(self):
        """Obtiene la fecha de creación del profesor."""
        return self._fecha_creacion
    
    @property
    def active(self):
        """Obtiene el estado de actividad del profesor."""
        return self._active