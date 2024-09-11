from Icrud import Icrud
from clsJson import JsonFile
from components import Valida
from utilities import borrarPantalla, gotoxy, purple_color, red_color, blue_color, reset_color, linea, green_color, yellow_color, cyan_color
from paths import path
from estudiante import Estudiante # Importa la clase Estudiante
import time
from datetime import datetime

class CrudStudents(Icrud):
    def __init__(self):
        self.json_file = JsonFile(f"{path}/data/students.json") # Modifica la ruta del archivo JSON
        self.valida = Valida()

    def create(self):
        """Crea un nuevo estudiante y lo guarda en el archivo JSON."""
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Crear Estudiante '.center(80)}{reset_color}")
        linea(80, green_color)

        data = self.json_file.read()
        estudiantes = [Estudiante(s['_cedula'], s['_nombre'], s['_apellido'], s['_fecha_nacimiento'], s['_active']) for s in data] # Convertir a objetos Estudiante

        while True:
            cedula = self.valida.cedula(f"{purple_color}Ingrese la cédula del estudiante: {reset_color}", 0, 5)
            if not any(s._cedula == cedula for s in estudiantes):  # Verificar si la cédula ya existe
                break
            else:
                print(f"{red_color}Cédula ya registrada. Intente de nuevo.{reset_color}")

        nombre = self.valida.solo_letras(f"{purple_color}Ingrese el nombre del estudiante: {reset_color}", f"{red_color} Nombre inválido. Solo se permiten letras.{reset_color}")
        apellido = self.valida.solo_letras(f"{purple_color}Ingrese el apellido del estudiante: {reset_color}", f"{red_color} Apellido inválido. Solo se permiten letras.{reset_color}")
        
        fecha_nacimiento_str = input(f"          ------>   | {purple_color}Ingrese la fecha de nacimiento (YYYY-MM-DD): {reset_color}")
        fecha_nacimiento = fecha_nacimiento_str

        nuevo_estudiante = Estudiante(cedula, nombre, apellido, fecha_nacimiento) 
        estudiantes.append(nuevo_estudiante)

        # Convertir los objetos Estudiante de vuelta a diccionarios para guardarlos en el JSON
        data = [estudiante.__dict__ for estudiante in estudiantes]
        self.json_file.save(data)
        print(f"{green_color}{' Estudiante Creado Exitosamente... '.center(80)}{reset_color}")
        time.sleep(2)

    def update(self):
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Actualizar Estudiante '.center(80)}{reset_color}")
        linea(80, green_color)

        data = self.json_file.read()
        estudiantes = [Estudiante(s['_cedula'], s['_nombre'], s['_apellido'],
                                  ['_fecha_nacimiento'], s['_active']) for s in data]

        while True:  # Bucle para asegurar que se ingrese una cédula válida
            cedula = self.valida.cedula(f"{purple_color}Ingrese la cédula del estudiante a actualizar: {reset_color}", 0, 5)
            if cedula is not None:
                break

        estudiante = next((s for s in estudiantes if s._cedula == cedula), None)
        if estudiante:
            # Solicitar nuevo nombre, manteniendo el original si se presiona Enter
            nuevo_nombre = input(f"          ------>   | {purple_color}Ingrese el nuevo nombre del estudiante (Enter para mantener {estudiante.nombre}): {reset_color}")
            estudiante._nombre = nuevo_nombre if nuevo_nombre else estudiante.nombre

            # Solicitar nuevo apellido, manteniendo el original si se presiona Enter
            nuevo_apellido = input(f"          ------>   | {purple_color}Ingrese el nuevo apellido del estudiante (Enter para mantener {estudiante.apellido}): {reset_color}")
            estudiante._apellido = nuevo_apellido if nuevo_apellido else estudiante.apellido

            # Convertir los objetos Estudiante de vuelta a diccionarios para guardarlos en el JSON
            data = [estudiante.__dict__ for estudiante in estudiantes]
            self.json_file.save(data)
            print()
            print(f"{green_color}{' Estudiante actualizado exitosamente... '.center(80)}{reset_color}")
            time.sleep(2)
        else:
            print(f"{red_color}{' Estudiante no encontrado. '.center(80)}{reset_color}")
            time.sleep(2)

    def delete(self):
        """Elimina un estudiante del archivo JSON."""
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Eliminar Estudiante '.center(80)}{reset_color}")
        linea(80, green_color)

        data = self.json_file.read()
        estudiantes = [Estudiante(s['_cedula'], s['_nombre'], s['_apellido'], 
                                  s['_fecha_nacimiento'], 
                                  s['_active']) for s in data]

        while True:
            cedula = self.valida.cedula(f"{purple_color}Ingrese la cédula del estudiante a eliminar: {reset_color}", 0, 5) 
            if cedula is not None:
                break

        estudiante_a_eliminar = next((s for s in estudiantes if s._cedula == cedula), None)

        if estudiante_a_eliminar:
            # Mostrar los datos del estudiante antes de eliminarlo
            print("\nDatos del estudiante a eliminar:")
            print(f"Cédula: {estudiante_a_eliminar._cedula}")
            print(f"Nombre: {estudiante_a_eliminar._nombre}")
            print(f"Apellido: {estudiante_a_eliminar._apellido}")

            # Solicitar confirmación al usuario
            confirmacion = input(f"{purple_color}\n¿Realmente desea eliminar este estudiante? (s/n): {reset_color}")
            if confirmacion.lower() == 's':
                estudiantes.remove(estudiante_a_eliminar)
                data = [estudiante.__dict__ for estudiante in estudiantes]
                self.json_file.save(data)
                print(f"{green_color}{' Estudiante eliminado exitosamente.... '.center(80)}{reset_color}")
            else:
                print(f"{yellow_color}{' Eliminación cancelada. '.center(80)}{reset_color}")
        else:
            print(f"{red_color}{' Estudiante no encontrado. '.center(80)}{reset_color}")

        time.sleep(2)

    def consult(self):
        """Muestra la lista de estudiantes o busca uno específico."""
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Consultar Estudiante(s) '.center(80)}{reset_color}")
        linea(80, green_color)

        data = self.json_file.read()
        if not data:
            print(f"{yellow_color}{' No hay estudiantes registrados. '.center(80)}{reset_color}")
            time.sleep(2)
            return

        while True:
            print(f"{cyan_color}1. Listar todos los estudiantes")
            print("2. Buscar estudiante por cédula") 
            print(f"3. Volver{reset_color}")

            opcion = input(f"{red_color}Seleccione una opción: {reset_color}")

            if opcion == '1':
                borrarPantalla()
                for student_data in data:
                    # Crear un objeto Estudiante a partir de los datos del diccionario
                    estudiante = Estudiante(student_data['_cedula'], student_data['_nombre'], student_data['_apellido'], 
                                          student_data['_fecha_nacimiento'], 
                                          student_data['_active'])
                    
                    # Usar las propiedades del objeto Estudiante para mostrar la información
                    print(f"Cédula: {estudiante._cedula}, Nombre: {estudiante._nombre}, Apellido: {estudiante._apellido}, ")
            elif opcion == '2':
                borrarPantalla()
                while True:
                    cedula = self.valida.cedula(f"{purple_color}Ingrese la cédula del estudiante a buscar: {reset_color}", 0, 5)
                    if cedula is not None:
                        break

                student_data = next((s for s in data if s['_cedula'] == cedula), None)
                if student_data:
                    # Crear un objeto Estudiante a partir de los datos del diccionario
                    estudiante = Estudiante(student_data['_cedula'], student_data['_nombre'], student_data['_apellido'], 
                                          student_data['_fecha_nacimiento'], 
                                          student_data['_active'])

                    # Usar las propiedades del objeto Estudiante para mostrar la información
                    print(f"Cédula: {estudiante._cedula}, Nombre: {estudiante.nombre}, Apellido: {estudiante._apellido}, ")
                else:
                    print(f"{yellow_color}{' Estudiante no encontrado. '.center(80)}{reset_color}")
                    time.sleep(2)
            elif opcion == '3':
                break
            else:
                print(f"{red_color}{' Opción inválida. Intente de nuevo. '.center(80)}{reset_color}")
                time.sleep(2)