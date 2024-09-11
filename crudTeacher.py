from Icrud import Icrud
from clsJson import JsonFile
from components import Valida
from paths import path
from profesor import Profesor
from utilities import borrarPantalla, gotoxy, purple_color, red_color, blue_color, reset_color, linea, green_color, yellow_color, cyan_color
import time

class CrudTeacher(Icrud):
    def __init__(self):
        self.json_file = JsonFile(f"{path}/data/teachers.json")
        self.valida = Valida()

    def create(self):
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Crear Profesor '.center(80)}{reset_color}")
        linea(80, green_color)
        """Crea un nuevo profesor y lo guarda en el archivo JSON."""
        data = self.json_file.read()
        if not data:  # Si el archivo está vacío, inicializar data con una lista vacía
            data = []
        # Convertir los datos del JSON a objetos Profesor
        profesores = [Profesor(t['_cedula'], t['_nombre'], t.get('_active', True)) for t in data]

        while True:  # Bucle para asegurar que la cédula sea única y válida
            cedula = self.valida.cedula(f"{purple_color}Ingrese la cédula del profesor: {reset_color}", 0, 5)
            if cedula is None:  # Manejar el caso de error en la validación
                continue
            if not any(p.cedula == cedula for p in profesores):
                break
            else:
                print(f"{red_color}Cédula ya registrada. Intente de nuevo.{reset_color}")

        nombre = self.valida.solo_letras(f"{purple_color}Ingrese el nombre del profesor: {reset_color}", f"{red_color}Nombre inválido. Solo se permiten letras.{reset_color}")

        nuevo_profesor = Profesor(cedula, nombre, True) 
        profesores.append(nuevo_profesor)

        # Convertir los objetos Profesor de vuelta a diccionarios para guardarlos en el JSON
        data = [profesor.__dict__ for profesor in profesores]
        self.json_file.save(data)
        print(f"{green_color}{' Profesor Creado Exitosamente... '.center(80)}{reset_color}")
        time.sleep(2)

    def update(self):
        """Actualiza un profesor existente en el archivo JSON."""
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Actualizar Profesor '.center(80)}{reset_color}")
        linea(80, green_color)

        data = self.json_file.read()
        profesores = [Profesor(t['_cedula'], t['_nombre'], t.get('_active', True)) for t in data]

        while True:
            cedula = self.valida.cedula(f"{purple_color}Ingrese la cédula del profesor a actualizar: {reset_color}", 0, 5)
            if cedula is not None:
                break

        profesor = next((p for p in profesores if p.cedula == cedula), None)

        if profesor:
            profesor.nombre = self.valida.solo_letras(f"{purple_color}Ingrese el nuevo nombre del profesor: {reset_color}", f"{red_color}Nombre inválido. Solo se permiten letras. {reset_color}")
            # Actualiza otros atributos del profesor según sea necesario, utilizando profesor.atributo = nuevo_valor

            # Convertir los objetos Profesor de vuelta a diccionarios para guardarlos en el JSON
            data = [profesor.__dict__ for profesor in profesores]
            self.json_file.save(data)
            print(f"{green_color}{' Profesor actualizado exitosamente.'.center(80)}{reset_color}")
            time.sleep(2)
        else:
            print(f"{yellow_color}{' Profesor no encontrado.'.center(80)}{reset_color}")
            time.sleep(2)

    def delete(self):
        """Elimina un profesor del archivo JSON."""
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Eliminar Profesor '.center(80)}{reset_color}")
        linea(80, green_color)

        data = self.json_file.read()
        profesores = [Profesor(t['_cedula'], t['_nombre'], t.get('_active', True)) for t in data]

        while True:
            cedula = self.valida.cedula(f"{purple_color}Ingrese la cédula del profesor a eliminar: {reset_color}", 0, 5)
            if cedula is not None:
                break

        # Buscar el profesor por cédula en la lista de objetos Profesor
        profesor_a_eliminar = next((p for p in profesores if p.cedula == cedula), None)

        if profesor_a_eliminar:
            # Mostrar los datos del profesor antes de eliminarlo
            print("\nDatos del profesor a eliminar:")
            print(f"Cédula: {profesor_a_eliminar.cedula}")
            print(f"Nombre: {profesor_a_eliminar.nombre}")
            print(f"Estado: {'Activo' if profesor_a_eliminar.active else 'Inactivo'}")

            # Solicitar confirmación al usuario
            confirmacion = input(f"{purple_color}\n¿Realmente desea eliminar este profesor? (s/n): {reset_color}")
            if confirmacion.lower() == 's':
                profesores.remove(profesor_a_eliminar)

                # Convertir los objetos Profesor de vuelta a diccionarios para guardarlos en el JSON
                data = [profesor.__dict__ for profesor in profesores]
                self.json_file.save(data)
                print(f"{green_color}{' Profesor eliminado exitosamente.'.center(80)}{reset_color}")
            else:
                print(f"{yellow_color}{' Eliminación cancelada. '.center(80)}{reset_color}")
        else:
            print(f"{red_color}{' Profesor no encontrado. '.center(80)}{reset_color}")

        time.sleep(2)

    def consult(self):
        """Muestra la lista de profesores o busca uno específico."""
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Consultar Profesores '.center(80)}{reset_color}")
        linea(80, green_color)

        data = self.json_file.read()
        profesores = [Profesor(t['_cedula'], t['_nombre'], t.get('_active', True)) for t in data]

        if not profesores:
            print("No hay profesores registrados.")
            return

        while True:
            cyan_color
            print(f"{cyan_color}1. Listar todos los profesores")
            print("2. Buscar profesor por cédula") 
            print(f"3. Volver {reset_color}") 
            

            opcion = input(f"\n{red_color}Seleccione una opción: {reset_color}")

            if opcion == '1':
                borrarPantalla()
                for profesor in profesores:
                    print(f"Cédula: {profesor.cedula}, Nombre: {profesor.nombre}")  # Muestra otros atributos según sea necesario
            elif opcion == '2':
                while True:
                    borrarPantalla()
                    cedula = self.valida.cedula(f"{purple_color}Ingrese la cédula del profesor a buscar: {reset_color}", 0, 5)
                    if cedula is not None:
                        break

                profesor = next((p for p in profesores if p.cedula == cedula), None)
                if profesor:
                    print(f"Cédula: {profesor.cedula}, Nombre: {profesor.nombre}")  # Muestra otros atributos según sea necesario
                else:
                    print(f"{yellow_color}{' Profesor no encontrado.'.center(80)}{reset_color}")
                    time.sleep(2)
            elif opcion == '3':
                break
            else:
                print(f"{red_color}{' Opción inválida. Intente de nuevo.'.center(80)}{reset_color}")
                time.sleep(2)