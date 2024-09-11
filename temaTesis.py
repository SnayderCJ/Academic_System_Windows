from datetime import date

class TemaTesis: 
    def __init__(self, id, nombre, periodo,active):
        self._id = id # Identificador único para el tema.
        self._descripcion = nombre # tema de la tesis.
        self._periodo = periodo # Periodo de la tesis. 
        self._fecha_creacion = date.today() # Fecha de creación del registro , se asigna la fecha actual. 
        self._active = active # Estado de actividad del curso (True o False).

    @property
    def id(self):
        return self._id
    
    @property
    def descripcion(self):
        return self._descripcion
    
    @property
    def periodo(self):
        return self._periodo
    
    @property
    def fecha_creacion(self):
        return self._fecha_creacion
    
    @property
    def active(self):
        return self._active
