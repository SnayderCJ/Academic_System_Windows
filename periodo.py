from datetime import date

class Periodo:
    """Representa un período académico en el sistema."""

    def __init__(self, id, periodo, active):
        if not periodo:
            raise ValueError("El nombre del período no puede estar vacío.")
        if not isinstance(active, bool):
            raise ValueError("El estado 'active' debe ser True o False.")

        self._id = id
        self._periodo = periodo
        self._fecha_creacion = date.today().strftime('%Y-%m-%d')
        self._active = active

    @property
    def id(self):
        """Obtiene el identificador único del período."""
        return self._id

    @property
    def periodo(self):
        """Obtiene el nombre o descripción del período."""
        return self._periodo

    @property
    def fecha_creacion(self):
        """Obtiene la fecha de creación del período."""
        return self._fecha_creacion
    
    @property
    def active(self):
        """Obtiene el estado de actividad del período."""
        return self._active

    def activar(self):
        """Activa el período."""
        self._active = True

    def desactivar(self):
        """Desactiva el período."""
        self._active = False