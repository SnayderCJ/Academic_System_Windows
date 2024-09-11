from Icrud import Icrud
from clsJson import JsonFile
from components import Valida
from paths import path
from utilities import borrarPantalla, gotoxy, purple_color, red_color, blue_color, reset_color, linea, green_color, yellow_color, cyan_color
from temaTesis import TemaTesis
from periodo import Periodo
import time

class CrudTemaDeTesis(Icrud):
    def __init__(self):
        self.json_file = JsonFile(f'{path}\data\ temaTesis.json')
        self.periodo_json_file = JsonFile(f'{path}\data\periods.json')
        self.valida = Valida()

    def create(self):
        """Crea un nuevo tema de Tesis y lo guarda en el archivo JSON."""
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Crear Tema de Tesis '.center(80)}{reset_color}")
        linea(80, green_color)

        data = self.json_file.read()
        temas_tesis = [TemaTesis(s['_id'], s['_descripcion'], s['_periodo'], s['_active']) for s in data]

        if temas_tesis:
            id = max([n.id for n in temas_tesis]) + 1
        else:
            id = 1

        descripcion = self.valida.solo_letras(f"{purple_color}Ingrese la descripción del tema de tesis: {reset_color}", f"{red_color}Descripción inválida. Solo se permiten letras.{reset_color}")

        # Obtener periodos disponibles (solo los activos)
        periodo_data = self.periodo_json_file.read()
        periodos = [Periodo(n['_id'], n['_periodo'], n["_active"]) for n in periodo_data]
        periodos_activos = [p for p in periodos if p._active]

        if not periodos_activos:
            print(f"{yellow_color}No hay periodos activos registrados. Debe crear un periodo antes de crear un tema de Tesis.{reset_color}")
            time.sleep(2)
            return

        print("\nPeriodos disponibles:")
        for periodo in periodos_activos:
            print(f"ID: {periodo._id}, Periodo: {periodo._periodo}")

        while True:
            periodo_id = self.valida.solo_numeros(f"{purple_color}Ingrese el ID del nivel: {reset_color}", f"{red_color}ID de nivel inválido. Ingrese un número entero positivo. {reset_color}", 0, 5)
            periodo_seleccionado = next((n for n in periodos_activos if n._id == int(periodo_id)), None)
            if periodo_seleccionado:
                break
            else:
                print(f"{red_color}{' Nivel no encontrado o inactivo. Intente de nuevo. '.center(80)}{reset_color}")

        nuevo_tema_tesis = TemaTesis(id, descripcion, periodo_seleccionado.id, True)  # Almacenar solo el ID del periodo
        temas_tesis.append(nuevo_tema_tesis)

        # Convertir los objetos TemaTesis a diccionarios
        data = [tema_tesis.__dict__ for tema_tesis in temas_tesis]
        self.json_file.save(data)
        print(f"{green_color}{' Tema de Tesis creada exitosamente... '.center(80)}{reset_color}")
        time.sleep(2)

    def update(self):
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Actualizar Tema De Tesis '.center(80)}{reset_color}")
        linea(80, green_color)

        data = self.json_file.read()
        temas_tesis = [TemaTesis(s['_id'], s['_descripcion'], s['_periodo'], s['_active']) for s in data]

        id = self.valida.solo_numeros(f"{purple_color}Ingrese el ID del tema de Tesis a actualizar: {reset_color}", f"{red_color}ID inválido. Ingrese un número entero positivo.{reset_color}", 0, 5)
        tema_tesis = next((a for a in temas_tesis if a.id == int(id)), None)

        if tema_tesis:
            # Solicitar nueva descripción, manteniendo la original si se presiona Enter
            nueva_descripcion = input(f"{purple_color}Ingrese la nueva descripción del tema de Tesis (Enter para mantener '{tema_tesis.descripcion}'): {reset_color}")
            if nueva_descripcion:  # Actualizar solo si se ingresa un nuevo valor
                tema_tesis.descripcion = self.valida.solo_letras(nueva_descripcion, f"{red_color}Descripción inválida. Solo se permiten letras.{reset_color}")

            # Obtener periodos disponibles (solo los activos)
            periodo_data = self.periodo_json_file.read()
            periodos = [Periodo(n['_id'], n['_periodo'], n['_active']) for n in periodo_data]
            periodos_activos = [p for p in periodos if p._active]

            if not periodos_activos:
                print(f"{yellow_color}No hay periodos activos registrados. No se puede actualizar el periodo del tema de Tesis.{reset_color}")
                time.sleep(2)
            else:
                print("\nPeriodos disponibles:")
                for periodo in periodos_activos:
                    print(f"ID: {periodo._id}, Periodo: {periodo._periodo}")

                # Solicitar al usuario que elija un periodo válido o mantenga el actual
                while True:
                    periodo_id_input = input(f"{purple_color}Ingrese el ID del nuevo periodo (Enter para mantener '{tema_tesis.periodo}'): {reset_color}")
                    if periodo_id_input == "":
                        break  # Mantener el periodo actual
                    try:
                        periodo_id = int(periodo_id_input)
                        periodo_seleccionado = next((n for n in periodos_activos if n._id == periodo_id), None)
                        if periodo_seleccionado:
                            tema_tesis._periodo = periodo_seleccionado._id
                            break
                        else:
                            print(f"{yellow_color}{' Periodo no encontrado o inactivo. Intente de nuevo. '.center(80)}{reset_color}")
                    except ValueError:
                        print(f"{red_color}{' ID de periodo inválido. Ingrese un número entero positivo o Enter para mantener el periodo actual.'.center(80)}{reset_color}")

            # Solicitar nuevo estado, manteniendo el original si se presiona Enter
            while True:
                nuevo_estado = input(f"{purple_color}Ingrese el nuevo estado del tema de Tesis (activo/inactivo) (actual: {'activo' if tema_tesis.active else 'inactivo'}): {reset_color}")
                if nuevo_estado.lower() in ['activo', 'inactivo']:
                    if nuevo_estado.lower() == 'activo':
                        tema_tesis.activar()
                    else:
                        tema_tesis.desactivar()
                    break
                elif nuevo_estado == "":  # Mantener el estado original si se presiona Enter
                    break
                else:
                    mensaje = f"{red_color}Estado inválido. Ingrese 'activo' o 'inactivo' o presione Enter para mantener el estado actual.{reset_color}"
                    print(mensaje.center(80))

            data = [tema_tesis.__dict__ for tema_tesis in temas_tesis]
            self.json_file.save(data)
            print(f"{green_color}{' Tema de Tesis actualizada exitosamente... '.center(80)}{reset_color}")
            time.sleep(2)
        else:
            print(f"{red_color}{' Tema de Tesis no encontrada. '.center(80)}{reset_color}")
            time.sleep(2)

    def delete(self):
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Eliminar Tema de Tesis '.center(80)}{reset_color}")
        linea(80, green_color)

        data = self.json_file.read()
        temaTesis = [TemaTesis(s['_id'], s['_descripcion'], s['_periodo'], s['_active']) for s in data]

        id = self.valida.solo_numeros("Ingrese el ID de la asignatura a eliminar: ", "ID inválido. Ingrese un número entero positivo.", 0, 5)
        temaTesis_a_eliminar = next((a for a in temaTesis if a.id == int(id)), None)

        if temaTesis_a_eliminar:
            # Mostrar los detalles de la asignatura antes de eliminarla
            print("\nDetalles de la asignatura a eliminar:")
            print(f"ID: {temaTesis_a_eliminar._id}")
            print(f"Descripción: {temaTesis_a_eliminar._descripcion}")
            print(f"Nivel: {temaTesis_a_eliminar._periodo}")
            print(f"Estado: {'Activo' if temaTesis_a_eliminar._active else 'Inactivo'}")

            # Solicitar confirmación al usuario
            confirmacion = input(f"{purple_color}\n¿Realmente desea eliminar esta asignatura? (s/n): {reset_color}")
            if confirmacion.lower() == 's':
                temaTesis = [a for a in temaTesis if a._id != int(id)]
                data = [n.__dict__ for n in temaTesis]
                self.json_file.save(data)
                print(f"{green_color}{' Tema de Tesis eliminada exitosamente. '.center(80)}{reset_color}")
            else:
                print(f"{yellow_color}{' Eliminación cancelada. '.center(80)}{reset_color}")
        else:
            print(f"{red_color}{' Tema de Tesis no encontrada. '.center(80)}{reset_color}")

        time.sleep(2)

    def consult(self):
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Consultar Tema de Tesis '.center(80)}{reset_color}")
        linea(80, green_color)

        data = self.json_file.read()
        temaTesis = [TemaTesis(s['_id'], s['_descripcion'], s['_periodo'], s['_active']) for s in data]

        # Obtener todos los niveles desde el archivo niveles.json
        periodo_data = self.periodo_json_file.read()
        periodos = [Periodo(n['_id'], n['_periodo']) for n in periodo_data] 

        if not temaTesis:
            print("No hay asignaturas registradas.")
            return

        while True:
            print(f"{cyan_color}1. Listar todas los Temas de Tesis")
            print("2. Buscar asignatura por ID")
            print(f"3. Volver{reset_color}")

            opcion = input(f"{red_color}Seleccione una opción: {reset_color}")

            if opcion == '1':
                borrarPantalla()
                for tematesi in temaTesis:
                    # Buscar el nivel correspondiente por su ID
                    nivel = next((n for n in periodos if n._id == tematesi._nivel), None)
                    nombre_nivel = nivel._nivel if nivel else "Nivel no encontrado"
                    print(f"ID: {tematesi._id}, Descripción: {tematesi._descripcion}, Nivel: {nombre_nivel}, Estado: {'Activo' if tematesi._active else 'Inactivo'}")
            elif opcion == '2':
                borrarPantalla()
                id = self.valida.solo_numeros(f"{purple_color}Ingrese el ID de la asignatura a buscar: {reset_color}", f"{red_color}ID inválido. Ingrese un número entero positivo.{reset_color}", 0, 5)
                asignatura = next((a for a in temaTesis if a._id == int(id)), None)
                if tematesi:
                    # Buscar el nivel correspondiente por su ID
                    nivel = next((n for n in periodos if n._id == tematesi._nivel), None)
                    nombre_nivel = nivel._nivel if nivel else "Nivel no encontrado"
                    print(f"ID: {tematesi._id}, Descripción: {tematesi._descripcion}, Nivel: {nombre_nivel}, Estado: {'Activo' if tematesi._active else 'Inactivo'}")
                else:
                    print(f"{yellow_color}{' Asignatura no encontrada. '.center(80)}{reset_color}")
                    time.sleep(2)
            elif opcion == '3':
                break
            else:
                print(f"{red_color}{' Opción inválida. Intente de nuevo.'.center(80)}{reset_color}")
                time.sleep(2)