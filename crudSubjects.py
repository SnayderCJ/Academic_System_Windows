from Icrud import Icrud
from clsJson import JsonFile
from components import Valida
from paths import path
from utilities import borrarPantalla, gotoxy, purple_color, red_color, blue_color, reset_color, linea, green_color, yellow_color, cyan_color
from asignatura import Asignatura
from nivel import Nivel
import time

class CrudSubjects(Icrud):
    def __init__(self):
        self.json_file = JsonFile(f'{path}/data/subjects.json')
        self.niveles_json_file = JsonFile(f'{path}/data/levels.json')
        self.valida = Valida()

    def create(self):
        """Crea una nueva asignatura y la guarda en el archivo JSON."""
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Crear Asignatura '.center(80)}{reset_color}")
        linea(80, green_color)

        data = self.json_file.read()
        asignaturas = [Asignatura(s['_id'], s['_descripcion'], s['_nivel'], s['_active']) for s in data]

        if asignaturas:
            id = max([asignatura.id for asignatura in asignaturas]) + 1
        else:
            id = 1

        descripcion = self.valida.solo_letras(f"{purple_color}Ingrese la descripción de la asignatura: {reset_color}", f"{red_color}Descripción inválida. Solo se permiten letras.{reset_color}")

        # Obtener niveles disponibles (solo los activos)
        niveles_data = self.niveles_json_file.read()
        niveles = [Nivel(n['_id'], n['_nivel']) for n in niveles_data]
        niveles_activos = [nivel for nivel in niveles if nivel._active]

        if not niveles_activos:
            print(f"{yellow_color}No hay niveles activos registrados. Debe crear un nivel antes de crear una asignatura.{reset_color}")
            time.sleep(2)
            return

        print("\nNiveles disponibles:")
        for nivel in niveles_activos:
            print(f"ID: {nivel._id}, Nivel: {nivel._nivel}")

        while True:
            nivel_id = self.valida.solo_numeros(f"{purple_color}Ingrese el ID del nivel: {reset_color}", f"{red_color}ID de nivel inválido. Ingrese un número entero positivo. {reset_color}", 0, 5)
            nivel_seleccionado = next((n for n in niveles_activos if n._id == int(nivel_id)), None)
            if nivel_seleccionado:
                break
            else:
                print(f"{red_color}{' Nivel no encontrado o inactivo. Intente de nuevo. '.center(80)}{reset_color}")

        nueva_asignatura = Asignatura(id, descripcion, nivel_seleccionado.id, True)  # Almacenar solo el ID del nivel
        asignaturas.append(nueva_asignatura)

        # Convertir los objetos Asignatura a diccionarios, asegurándonos de que 'nivel' sea un ID
        data = [{**asignatura.__dict__, 'nivel': asignatura.nivel} for asignatura in asignaturas] 
        self.json_file.save(data)
        print(f"{green_color}{' Asignatura creada exitosamente... '.center(80)}{reset_color}")
        time.sleep(2)

    def update(self):
        """Actualiza una asignatura existente en el archivo JSON."""
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Actualizar Asignatura '.center(80)}{reset_color}")
        linea(80, green_color)

        data = self.json_file.read()
        asignaturas = [Asignatura(s['_id'], s['_descripcion'], s['_nivel'], s['_active']) for s in data]

        id = self.valida.solo_numeros(f"{purple_color}Ingrese el ID de la asignatura a actualizar: {reset_color}", f"{red_color}ID inválido. Ingrese un número entero positivo.{reset_color}", 0, 5)
        asignatura = next((a for a in asignaturas if a._id == int(id)), None)

        if asignatura:
            # Solicitar nueva descripción, manteniendo la original si se presiona Enter
            nueva_descripcion = input(f"{purple_color}Ingrese la nueva descripción de la asignatura (Enter para mantener '{asignatura._descripcion}'): {reset_color}")
            if nueva_descripcion:  # Actualizar solo si se ingresa un nuevo valor
                asignatura._descripcion = self.valida.solo_letras(nueva_descripcion, f"{red_color}Descripción inválida. Solo se permiten letras.{reset_color}")

            # Obtener niveles disponibles (solo los activos)
            niveles_data = self.niveles_json_file.read()
            niveles = [Nivel(n['_id'], n['_nivel']) for n in niveles_data]
            niveles_activos = [nivel for nivel in niveles if nivel._active]

            if not niveles_activos:
                print(f"{yellow_color}No hay niveles activos registrados. No se puede actualizar el nivel de la asignatura.{reset_color}")
                time.sleep(2)
            else:
                print("\nNiveles disponibles:")
                for nivel in niveles_activos:
                    print(f"ID: {nivel._id}, Nivel: {nivel._nivel}")

                # Solicitar al usuario que elija un nivel válido o mantenga el actual
                while True:
                    nivel_id_input = input(f"{purple_color}Ingrese el ID del nuevo nivel (Enter para mantener '{asignatura._nivel}'): {reset_color}")
                    if nivel_id_input == "":
                        break  # Mantener el nivel actual
                    try:
                        nivel_id = int(nivel_id_input)
                        nivel_seleccionado = next((n for n in niveles_activos if n._id == nivel_id), None)
                        if nivel_seleccionado:
                            asignatura._nivel = nivel_seleccionado.id
                            break
                        else:
                            print(f"{yellow_color}{' Nivel no encontrado o inactivo. Intente de nuevo. '.center(80)}{reset_color}")
                    except ValueError:
                        print(f"{red_color}{' ID de nivel inválido. Ingrese un número entero positivo o Enter para mantener el nivel actual.'.center(80)}{reset_color}")

            # Solicitar nuevo estado, manteniendo el original si se presiona Enter
            while True:
                nuevo_estado = input(f"{purple_color}Ingrese el nuevo estado de la asignatura (activo/inactivo) (actual: {'activo' if asignatura.active else 'inactivo'}): {reset_color}")
                if nuevo_estado.lower() in ['activo', 'inactivo']:
                    if nuevo_estado.lower() == 'activo':
                        asignatura.activar()
                    else:
                        asignatura.desactivar()
                    break
                elif nuevo_estado == "":  # Mantener el estado original si se presiona Enter
                    break
                else:
                    mensaje = f"{red_color}Estado inválido. Ingrese 'activo' o 'inactivo' o presione Enter para mantener el estado actual.{reset_color}"
                    print(mensaje.center(80))

            data = [asignatura.__dict__ for asignatura in asignaturas]
            self.json_file.save(data)
            print(f"{green_color}{' Asignatura actualizada exitosamente... '.center(80)}{reset_color}")
            time.sleep(2)
        else:
            print(f"{red_color}{' Asignatura no encontrada. '.center(80)}{reset_color}")
            time.sleep(2)

    def delete(self):
        """Elimina una asignatura del archivo JSON."""
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Eliminar Asignatura '.center(80)}{reset_color}")
        linea(80, green_color)

        data = self.json_file.read()
        asignaturas = [Asignatura(s['_id'], s['_descripcion'], s['_nivel'], s['_active']) for s in data]

        id = self.valida.solo_numeros("Ingrese el ID de la asignatura a eliminar: ", "ID inválido. Ingrese un número entero positivo.", 0, 5)
        asignatura_a_eliminar = next((a for a in asignaturas if a._id == int(id)), None)

        if asignatura_a_eliminar:
            # Mostrar los detalles de la asignatura antes de eliminarla
            print("\nDetalles de la asignatura a eliminar:")
            print(f"ID: {asignatura_a_eliminar._id}")
            print(f"Descripción: {asignatura_a_eliminar._descripcion}")
            print(f"Nivel: {asignatura_a_eliminar._nivel}")
            print(f"Estado: {'Activo' if asignatura_a_eliminar._active else 'Inactivo'}")

            # Solicitar confirmación al usuario
            confirmacion = input(f"{purple_color}\n¿Realmente desea eliminar esta asignatura? (s/n): {reset_color}")
            if confirmacion.lower() == 's':
                asignaturas = [a for a in asignaturas if a._id != int(id)]
                data = [asignatura.__dict__ for asignatura in asignaturas]
                self.json_file.save(data)
                print(f"{green_color}{' Asignatura eliminada exitosamente. '.center(80)}{reset_color}")
            else:
                print(f"{yellow_color}{' Eliminación cancelada. '.center(80)}{reset_color}")
        else:
            print(f"{red_color}{' Asignatura no encontrada. '.center(80)}{reset_color}")

        time.sleep(2)

    def consult(self):
        """Muestra la lista de asignaturas o busca una específica."""
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Consultar Asignatura '.center(80)}{reset_color}")
        linea(80, green_color)

        data = self.json_file.read()
        asignaturas = [Asignatura(s['_id'], s['_descripcion'], s['_nivel'], s['_active']) for s in data]

        # Obtener todos los niveles desde el archivo niveles.json
        niveles_data = self.niveles_json_file.read()
        niveles = [Nivel(n['_id'], n['_nivel']) for n in niveles_data] 

        if not asignaturas:
            print("No hay asignaturas registradas.")
            return

        while True:
            print(f"{cyan_color}1. Listar todas las asignaturas")
            print("2. Buscar asignatura por ID")
            print(f"3. Volver{reset_color}")

            opcion = input(f"{red_color}Seleccione una opción: {reset_color}")

            if opcion == '1':
                borrarPantalla()
                for asignatura in asignaturas:
                    # Buscar el nivel correspondiente por su ID
                    nivel = next((n for n in niveles if n._id == asignatura._nivel), None)
                    nombre_nivel = nivel._nivel if nivel else "Nivel no encontrado"
                    print(f"ID: {asignatura._id}, Descripción: {asignatura._descripcion}, Nivel: {nombre_nivel}, Estado: {'Activo' if asignatura._active else 'Inactivo'}")
            elif opcion == '2':
                borrarPantalla()
                id = self.valida.solo_numeros(f"{purple_color}Ingrese el ID de la asignatura a buscar: {reset_color}", f"{red_color}ID inválido. Ingrese un número entero positivo.{reset_color}", 0, 5)
                asignatura = next((a for a in asignaturas if a._id == int(id)), None)
                if asignatura:
                    # Buscar el nivel correspondiente por su ID
                    nivel = next((n for n in niveles if n._id == asignatura._nivel), None)
                    nombre_nivel = nivel._nivel if nivel else "Nivel no encontrado"
                    print(f"ID: {asignatura._id}, Descripción: {asignatura._descripcion}, Nivel: {nombre_nivel}, Estado: {'Activo' if asignatura._active else 'Inactivo'}")
                else:
                    print(f"{yellow_color}{' Asignatura no encontrada. '.center(80)}{reset_color}")
                    time.sleep(2)
            elif opcion == '3':
                break
            else:
                print(f"{red_color}{' Opción inválida. Intente de nuevo.'.center(80)}{reset_color}")
                time.sleep(2)