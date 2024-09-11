from Icrud import Icrud
from clsJson import JsonFile
from components import Valida
from paths import path
from nivel import Nivel
from utilities import borrarPantalla, gotoxy, purple_color, red_color, blue_color, reset_color, linea, green_color, yellow_color, cyan_color
import time

class CrudLevel(Icrud):
    def __init__(self):
        self.json_file = JsonFile(f'{path}/data/levels.json')
        self.valida = Valida()

        self.niveles_predefinidos = [
            "Primer Semestre",
            "Segundo Semestre",
            "Tercero Semestre",
            "Cuarto Semestre",
            "Quinto Semestre",
            "Sexto Semestre",
            "Séptimo Semestre",
            "Octavo Semestre",
        ]

    def create(self):
        """Crea un nuevo nivel educativo y lo guarda en el archivo JSON."""
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Crear Nivel Educativo '.center(80)}{reset_color}")
        linea(80, green_color)

        data = self.json_file.read()
        niveles = [Nivel(n['_id'], n['_nivel']) for n in data]

        if niveles:
            id = max([nivel._id for nivel in niveles]) + 1
        else:
            id = 1

        # Preguntar al usuario si desea crear un nuevo nivel predefinido
        while True:
            crear_nuevo = input(f"{purple_color}¿Desea crear un nuevo nivel predefinido? (s/n): {reset_color}")
            if crear_nuevo.lower() in ['s', 'n']:
                break
            else:
                print(f"{red_color}Opción inválida. Ingrese 's' o 'n'.{reset_color}")

        if crear_nuevo.lower() == 's':
            # Crear un nuevo nivel predefinido
            nombre_nivel = self.valida.solo_letras(f"{purple_color}Ingrese el nombre del nuevo nivel educativo: {reset_color}", f"{red_color}Nombre inválido. Solo se permiten letras.{reset_color}")
            self.niveles_predefinidos.append(nombre_nivel)

        # Mostrar niveles predefinidos (incluyendo el nuevo si se creó)
        print(f"{purple_color}\nNiveles educativos predefinidos:{reset_color}")
        for i, nivel_predefinido in enumerate(self.niveles_predefinidos):
            print(f"{cyan_color}{i+1}. {nivel_predefinido}{reset_color}")

        # Solicitar al usuario que elija un nivel predefinido
        while True:
            opcion = self.valida.solo_numeros(f"{purple_color}Seleccione el número del nivel educativo: {reset_color}",
                                              f"{red_color}Opción inválida. Ingrese un número entero positivo. {reset_color}", 0, 5)
            if 1 <= int(opcion) <= len(self.niveles_predefinidos):
                nombre_nivel = self.niveles_predefinidos[int(opcion) - 1]
                break
            else:
                print(f"{red_color}Opción fuera de rango. Intente de nuevo.{reset_color}")

        nuevo_nivel = Nivel(id, nombre_nivel)
        niveles.append(nuevo_nivel)

        # Convertir los objetos Nivel de vuelta a diccionarios para guardarlos en el JSON
        data = [nivel.__dict__ for nivel in niveles]
        self.json_file.save(data)
        print(f"{green_color}{' Nivel educativo creado exitosamente. '.center(80)}{reset_color}")
        time.sleep(2)


    def update(self):
        """Actualiza un nivel educativo existente en el archivo JSON."""
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Actualizar Nivel Educativo '.center(80)}{reset_color}")
        linea(80, green_color)

        data = self.json_file.read()
        niveles = [Nivel(n['_id'], n['_nivel']) for n in data] 

        id = self.valida.solo_numeros("Ingrese el ID del nivel educativo a actualizar: ", "ID inválido. Ingrese un número entero positivo.", 0, 5)
        nivel = next((n for n in niveles if n.id == int(id)), None)

        if nivel:
            nivel._nivel = self.valida.solo_letras("Ingrese el nuevo nombre del nivel educativo: ", "Nombre inválido. Solo se permiten letras.")

            while True:
                nuevo_estado = input(f"{purple_color}Ingrese el nuevo estado del nivel (activo/inactivo) (actual: {'activo' if nivel.active else 'inactivo'}): {reset_color}")
                if nuevo_estado.lower() in ['activo', 'inactivo']:
                    if nuevo_estado.lower() == 'activo':
                        nivel.activar() 
                    else:
                        nivel.desactivar() 
                    break
                else:
                    mensaje = f"{purple_color} Estado inválido. Ingrese 'activo' o 'inactivo'. {reset_color}"
                    print(mensaje.center(80)) 
                    

            data = [nivel.__dict__ for nivel in niveles]
            self.json_file.save(data)
            print("Nivel educativo actualizado exitosamente.")
            time.sleep(2)
        else:
            print("Nivel educativo no encontrado.")
            time.sleep(2)
        

    def delete(self):
        """Elimina un nivel educativo del archivo JSON."""
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Eliminar Nivel Educativo '.center(80)}{reset_color}")
        linea(80, green_color)

        data = self.json_file.read()
        niveles = [Nivel(n['_id'], n['_nivel']) for n in data]

        id = self.valida.solo_numeros(f"{purple_color}Ingrese el ID del nivel educativo a eliminar: {reset_color}", f"{red_color}ID inválido. Ingrese un número entero positivo.{reset_color}", 0, 5)
        nivel_a_eliminar = next((n for n in niveles if n.id == int(id)), None)

        if nivel_a_eliminar:
            # Mostrar los detalles del nivel antes de eliminarlo
            print("\nDetalles del nivel a eliminar:")
            print(f"ID: {nivel_a_eliminar.id}")
            print(f"Nombre: {nivel_a_eliminar.nivel}")
            print(f"Estado: {'Activo' if nivel_a_eliminar.active else 'Inactivo'}")

            # Solicitar confirmación al usuario
            confirmacion = input(f"{purple_color}\n¿Realmente desea eliminar este nivel educativo? (s/n): {reset_color}")
            if confirmacion.lower() == 's':
                niveles = [n for n in niveles if n.id != int(id)]
                data = [nivel.__dict__ for nivel in niveles]
                self.json_file.save(data)
                print(f"{green_color}{' Nivel educativo eliminado exitosamente. '.center(80)}{reset_color}")
            else:
                print(f"{yellow_color}{' Eliminación cancelada. '.center(80)}{reset_color}")
        else:
            print(f"{red_color}{' Nivel educativo no encontrado. '.center(80)}{reset_color}")

        time.sleep(2)

    def consult(self):
        """Muestra la lista de niveles educativos o busca uno específico."""
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Consultar Nivel Educativo '.center(80)}{reset_color}")
        linea(80, green_color)

        data = self.json_file.read()
        niveles = [Nivel(n['_id'], n['_nivel']) for n in data]

        if not niveles:
            print(f"{red_color}No hay niveles educativos registrados.{reset_color}")
            return

        while True:
            print(f"{cyan_color}1. Listar todos los niveles educativos")
            print("2. Buscar nivel educativo por ID")
            print(f"3. Volver{reset_color}")

            opcion = input(f"{red_color}Seleccione una opción: {reset_color}")

            if opcion == '1':
                borrarPantalla()
                for nivel in niveles:
                    print(f"ID: {nivel._id}, Nombre: {nivel._nivel}, Estado: {'Activo' if nivel._active else 'Inactivo'}")
                    time.sleep(3)
            elif opcion == '2':
                borrarPantalla()
                id = self.valida.solo_numeros(f"{purple_color}Ingrese el ID del nivel educativo a buscar: {reset_color}", f"{red_color}ID inválido. Ingrese un número entero positivo. {reset_color}", 0, 5)
                nivel = next((n for n in niveles if n._id == int(id)), None)
                if nivel:
                    borrarPantalla()
                    print(f"ID: {nivel._id}, Nombre: {nivel._nivel}, Estado: {'Activo' if nivel._active else 'Inactivo'}")
                    time.sleep(3)
                else:
                    print("Nivel educativo no encontrado.")
            elif opcion == '3':
                break
            else:
                print("Opción inválida. Intente de nuevo.")