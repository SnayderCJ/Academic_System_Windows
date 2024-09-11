from estudiante import Estudiante

class DetalleTesis: 
    def __init__(self, id, estudiante, nota): 
        self.id = id # Identificador único para el detalle de la tesis. 
        self.estudiante = estudiante # registro del estudiante de la tesis. 
        self.nota = nota # nota de la tesis 
        self.observacion # observación de aprobado >= 70 sino reprobado

    @property
    def id(self):
        """Obtiene el identificador único del detalle de la nota."""
        return self.id

    @property
    def estudiante(self):
        """Obtiene el estudiante al que se le asigna la nota."""
        return self.estudiante
    
    @property
    def nota(self):
        """Obtiene la primera nota del estudiante."""
        return self.nota
    
    @property
    def observacion(self):
        return self.observacion  #Logica para observacion 
    
    # def calcular_promedio(self):
    #     """Calcula el promedio de las notas, considerando la recuperación si existe."""
    #     if self.recuperacion is not None and self.recuperacion != 0:  
    #         try:
    #             recuperacion_float = float(self.recuperacion)
    #             nota = self.nota1 + self.nota2
    #             return (nota + recuperacion_float)/2
    #         except ValueError:
    #             print(f"Error: La nota de recuperación '{self.recuperacion}' no es un número válido.")
    #             return None
    #     else:
    #         return self.nota1 + self.nota2