from profesor import Profesor
from temaTesis import TemaTesis

class Tesis:
    def __init__(self, id, tema, tutor, fecha_sustentacion, active): 
        self.id = id # Identificador único para la tesis. 
        self.tema = tema #tema de la tesis. 
        self.profesor = tutor # profesor tutor de la tesis 
        self.fecha_sustentacion = fecha_sustentacion # Fecha de sustentación de la tesis. self.detalleTesis = [] # Lista para almacenar los detalles de las asignaturas del estudiante. self.fecha_creacion = date.today() # Fecha de creación del registro de la nota, se asigna la fecha actual. self.active = active # Estado de actividad de la nota (True o False). 
        
        def addDetalleTesis(self, detalle_tesis: DetalleTesis):
            estudiante_id = detalle_tesis.estudiante._cedula
            if any(dn.estudiante._cedula == estudiante_id for dn in self._detalleTesis):
                raise ValueError("El estudiante ya tiene una Tesis Registrada para esta Tema y profesor")
            self.detalleTesis.append(detalle_tesis)

            # Método placeholder para añadir detalles de los estudiantes de la tesis.

        # def add_detalle_nota(self, detalle_nota: DetalleNota):
        # estudiante_id = detalle_nota.estudiante._cedula
        # if any(dn.estudiante._cedula == estudiante_id for dn in self._detalleNota):
        #     raise ValueError("El estudiante ya tiene una nota registrada para esta asignatura y periodo.")
        # self._detalleNota.append(detalle_nota)