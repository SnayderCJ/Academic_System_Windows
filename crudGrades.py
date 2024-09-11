from Icrud import Icrud
from clsJson import JsonFile
from components import Valida
from paths import path
from nota import Nota
from detalleNota import DetalleNota
from estudiante import Estudiante
from periodo import Periodo
from profesor import Profesor
from asignatura import Asignatura
from utilities import borrarPantalla, gotoxy, purple_color, red_color, blue_color, reset_color, linea, green_color, yellow_color, cyan_color
import time

class CrudGrades(Icrud):
    def __init__(self):
        self.json_file = JsonFile(f'{path}/data/grades.json')
        self.valida = Valida()

    def create(self):
        """Crea un nuevo registro de notas y lo guarda en el archivo JSON."""
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Crear Registro de Notas '.center(80)}{reset_color}")
        linea(80, green_color)

        grades_data = self.json_file.read()
        if grades_data:
            id = max([grade['_id'] for grade in grades_data]) + 1
        else:
            id = 1

        # Obtener periodo, profesor y asignatura, asegúrate de validar que existan
        periodos_data = JsonFile(f'{path}/data/periods.json').read()
        profesores_data = JsonFile(f'{path}/data/teachers.json').read()
        asignaturas_data = JsonFile(f'{path}/data/subjects.json').read()

        # Mostrar periodos disponibles (solo los activos)
        borrarPantalla()
        print(f"{cyan_color}\nPeriodos disponibles:{reset_color}")
        for periodo in periodos_data:
            if periodo.get('_active'):
                print(f"ID: {periodo['_id']}, Periodo: {periodo['_periodo']}")

        while True:
            periodo_id = self.valida.solo_numeros(f"{purple_color}Ingrese el ID del periodo: {reset_color}", f"{red_color}ID de periodo inválido. Ingrese un número entero positivo.{reset_color}", 0, 5)
            periodo_seleccionado = next((p for p in periodos_data if p['_id'] == int(periodo_id) and p.get('_active')), None)
            if periodo_seleccionado:
                break
            else:
                print(f"{yellow_color}{' Periodo no encontrado o inactivo. Intente de nuevo. '.center(80)}{reset_color}")

        # Mostrar profesores disponibles (solo los activos)
        borrarPantalla()
        print(f"{cyan_color}\nProfesores disponibles:{reset_color}")
        for profesor in profesores_data:
            if profesor.get('_active'):
                print(f"ID: {profesor['_cedula']}, Nombre: {profesor['_nombre']}")

        while True:
            profesor_cedula = self.valida.cedula(f"{purple_color}Ingrese la cédula del profesor: {reset_color}", 0, 5)
            profesor_seleccionado = next((p for p in profesores_data if p['_cedula'] == profesor_cedula and p.get('_active')), None)
            if profesor_seleccionado:
                break
            else:
                print(f"{yellow_color}{' Profesor no encontrado o inactivo. Intente de nuevo. '.center(80)}{reset_color}")

        # Mostrar asignaturas disponibles (solo las activas)
        borrarPantalla()
        print(f"{cyan_color}\nAsignaturas disponibles:{reset_color}")
        for asignatura in asignaturas_data:
            if asignatura.get('_active'):
                print(f"ID: {asignatura['_id']}, Nombre: {asignatura['_descripcion']}")

        while True:
            asignatura_id = self.valida.solo_numeros("Ingrese el ID de la asignatura: ", "ID de asignatura inválido. Ingrese un número entero positivo.", 0, 5)
            asignatura_seleccionada = next((a for a in asignaturas_data if a['_id'] == int(asignatura_id) and a.get('_active')), None)
            if asignatura_seleccionada:
                break
            else:
                print(f"{yellow_color}{' Asignatura no encontrado o inactivo. Intente de nuevo. '.center(80)}{reset_color}")

        # Obtener todos los estudiantes desde el archivo students.json
        estudiantes_data = JsonFile(f'{path}/data/students.json').read()

        
        # Crear la instancia de Nota, almacenando solo los IDs
        nueva_nota = Nota(id, 
                        periodo_seleccionado['_periodo'], 
                        profesor_seleccionado['_nombre'],
                        asignatura_seleccionada['_descripcion']
                        )

        for estudiante_data in estudiantes_data:
            if estudiante_data.get('_active'): 
                estudiante = Estudiante(estudiante_data['_cedula'], estudiante_data['_nombre'], estudiante_data['_apellido'], estudiante_data['_fecha_nacimiento'], estudiante_data['_active'])
                while True:
                    try:
                        nota1 = self.valida.valida_nota(f"Ingrese la primera nota para {estudiante._nombre}: ", "Nota inválida. Ingrese un número decimal positivo.")
                        nota2 = self.valida.valida_nota(f"Ingrese la segunda nota para {estudiante._nombre}: ", "Nota inválida. Ingrese un número decimal positivo.")
                        recuperacion = input(f"Ingrese la nota de recuperación para {estudiante._nombre} (dejar en blanco si no aplica): ") or 0
                        observacion = input(f"Ingrese una observación para {estudiante._nombre} (opcional): ")

                        detalle = DetalleNota(None, estudiante, float(nota1), float(nota2),
                                            float(recuperacion) if recuperacion else None, observacion)
                        nueva_nota.add_detalle_nota(detalle) 
                        break
                    
                    except ValueError as e:
                        print(f"Error: {e}")


        grade_dict = {
            '_id': id,
            '_periodo_id': nueva_nota._periodo,
            '_profesor_id': nueva_nota._profesor,  # Asumiendo que el identificador del profesor es la cédula
            '_asignatura_id': nueva_nota._asignatura,
            '_fecha_creacion': nueva_nota._fecha_creacion.strftime('%Y-%m-%d'),  # Convertir la fecha a cadena
            '_active': nueva_nota._active,
            '_detalleNota': [detalle.__dict__ for detalle in nueva_nota._detalleNota]
}

        # Convertir los objetos DetalleNota dentro de _detalleNota a diccionarios
        grade_dict['_detalleNota'] = [detalle.__dict__ for detalle in nueva_nota._detalleNota] 

        grades_data.append(grade_dict)
        self.json_file.save(grades_data)
        print(f"{green_color}{' Registro de calificaciones creado exitosamente. '.center(80)}{reset_color}")
        time.sleep(2)

    def update(self):
        """Actualiza un registro de calificaciones existente en el archivo JSON."""
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Actualizar Registro de Notas '.center(80)}{reset_color}")
        linea(80, green_color)

        grades_data = self.json_file.read()
        id = self.valida.solo_numeros("Ingrese el ID del registro de calificaciones a actualizar: ", "ID inválido. Ingrese un número entero positivo.", 0, 5)
        grade_dict = next((g for g in grades_data if g['_id'] == int(id)), None)

        if grade_dict:
            # Obtener periodo, profesor y asignatura, asegúrate de validar que existan
            periodos_data = JsonFile(f'{path}/data/periods.json').read()
            profesores_data = JsonFile(f'{path}/data/teachers.json').read()
            asignaturas_data = JsonFile(f'{path}/data/subjects.json').read()


            # Mostrar periodos disponibles (solo los activos)
            borrarPantalla()
            print(f"{cyan_color}\nPeriodos disponibles:{reset_color}")
            for periodo in periodos_data:
                if periodo.get('_active'):
                    print(f"ID: {periodo['_id']}, Periodo: {periodo['_periodo']}")

            while True:
                periodo_id = self.valida.solo_numeros(f"{purple_color}Ingrese el ID del periodo: {reset_color}", f"{red_color}ID de periodo inválido. Ingrese un número entero positivo.{reset_color}", 0, 5)
                periodo_seleccionado = next((p for p in periodos_data if p['_id'] == int(periodo_id) and p.get('_active')), None)
                if periodo_seleccionado:
                    break
                else:
                    print(f"{yellow_color}{' Periodo no encontrado o inactivo. Intente de nuevo. '.center(80)}{reset_color}")

            # Mostrar profesores disponibles (solo los activos)
            borrarPantalla()
            print(f"{cyan_color}\nProfesores disponibles:{reset_color}")
            for profesor in profesores_data:
                if profesor.get('_active'):
                    print(f"ID: {profesor['_cedula']}, Nombre: {profesor['_nombre']}")

            while True:
                profesor_cedula = self.valida.cedula(f"{purple_color}Ingrese la cédula del profesor: {reset_color}", 0, 5)
                profesor_seleccionado = next((p for p in profesores_data if p['_cedula'] == profesor_cedula and p.get('_active')), None)
                if profesor_seleccionado:
                    break
                else:
                    print(f"{yellow_color}{' Profesor no encontrado o inactivo. Intente de nuevo. '.center(80)}{reset_color}")

            # Mostrar asignaturas disponibles (solo las activas)
            borrarPantalla()
            print(f"{cyan_color}\nAsignaturas disponibles:{reset_color}")
            for asignatura in asignaturas_data:
                if asignatura.get('_active'):
                    print(f"ID: {asignatura['_id']}, Nombre: {asignatura['_descripcion']}")

            while True:
                asignatura_id = self.valida.solo_numeros("Ingrese el ID de la asignatura: ", "ID de asignatura inválido. Ingrese un número entero positivo.", 0, 5)
                asignatura_seleccionada = next((a for a in asignaturas_data if a['_id'] == int(asignatura_id) and a.get('_active')), None)
                if asignatura_seleccionada:
                    break
                else:
                    print(f"{yellow_color}{' Asignatura no encontrado o inactivo. Intente de nuevo. '.center(80)}{reset_color}")

            # Obtener todos los estudiantes desde el archivo students.json
            estudiantes_data = JsonFile(f'{path}/data/students.json').read()

            # Actualizar la instancia de Nota, almacenando solo los IDs
            nota_actualizada = Nota(grade_dict['_id'], 
                            periodo_seleccionado['_periodo'], 
                            profesor_seleccionado['_nombre'],
                            asignatura_seleccionada['_descripcion']
                            )

            # Limpiar los detalles de la nota anterior
            nota_actualizada._detalleNota = []

            for estudiante_data in estudiantes_data:
                if estudiante_data.get('_active'): 
                    estudiante = Estudiante(estudiante_data['_cedula'], estudiante_data['_nombre'], estudiante_data['_apellido'], estudiante_data['_fecha_nacimiento'], estudiante_data['_active'])
                    while True:
                        try:
                            nota1 = self.valida.valida_nota(f"Ingrese la primera nota para {estudiante._nombre}: ", "Nota inválida. Ingrese un número decimal positivo.")
                            nota2 = self.valida.valida_nota(f"Ingrese la segunda nota para {estudiante._nombre}: ", "Nota inválida. Ingrese un número decimal positivo.")
                            recuperacion = input(f"Ingrese la nota de recuperación para {estudiante._nombre} (dejar en blanco si no aplica): ")
                            observacion = input(f"Ingrese una observación para {estudiante._nombre} (opcional): ")

                            detalle = DetalleNota(None, estudiante, float(nota1), float(nota2),
                                                  float(recuperacion) if recuperacion else None, observacion)
                            nota_actualizada.add_detalle_nota(detalle) 
                            break
                        except ValueError as e:
                            print(f"Error: {e}")

            # Actualizar el registro en grades_data
            for i, g in enumerate(grades_data):
                if g['_id'] == nota_actualizada._id:
                    # Convertir el objeto Nota a un diccionario, incluyendo los IDs de las entidades relacionadas
                    grade_dict = nota_actualizada.__dict__
                    grade_dict['_periodo_id'] = nota_actualizada._periodo  # Asignar el ID del periodo directamente
                    grade_dict['_profesor_id'] = nota_actualizada._profesor  # Asignar la cédula del profesor directamente
                    grade_dict['_asignatura_id'] = nota_actualizada._asignatura  # Asignar el ID de la asignatura directamente

                    # Convertir los objetos DetalleNota dentro de _detalleNota a diccionarios
                    grade_dict['_detalleNota'] = [detalle.__dict__ for detalle in nota_actualizada._detalleNota] 

                    grades_data[i] = grade_dict
                    break

            self.json_file.save(grades_data)
            print(f"{green_color}{' Registro de calificaciones actualizado exitosamente. '.center(80)}{reset_color}")
            time.sleep(2)
        else:
            print("Registro de calificaciones no encontrado.")
            time.sleep(2)

    def delete(self):
        """Elimina un registro de calificaciones del archivo JSON."""
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Eliminar Registro de Notas '.center(80)}{reset_color}")
        linea(80, green_color)

        data = self.json_file.read()

        id = self.valida.solo_numeros("Ingrese el ID del registro de calificaciones a eliminar: ", "ID inválido. Ingrese un número entero positivo.", 0, 5)

        # Buscar y eliminar el registro por ID
        data = [g for g in data if g['_id'] != int(id)]

        self.json_file.save(data)
        print(f"{green_color}{' Registro de notas eliminado exitosamente. '.center(80)}{reset_color}")
        time.sleep(2)


    def consult(self):
        """Muestra la lista de registros de calificaciones o busca uno específico."""
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Consultar Registro de Notas '.center(80)}{reset_color}")
        linea(80, green_color)

        data = self.json_file.read()
        if not data:
            print("No hay registros de calificaciones.")
            return

        # Obtener datos de periodos, profesores y asignaturas para mostrar nombres en lugar de IDs
        periodos_data = JsonFile(f'{path}/data/periods.json').read()
        profesores_data = JsonFile(f'{path}/data/teachers.json').read()
        asignaturas_data = JsonFile(f'{path}/data/subjects.json').read()

        while True:
            print(f"{cyan_color}\n1. Listar todos los registros de calificaciones")
            print("2. Buscar registro por ID")
            print(f"3. Volver{reset_color}")

            opcion = input(f"{red_color}Seleccione una opción: {reset_color}")

            if opcion == '1':
                borrarPantalla()
                for grade_dict in data:
                    print(f'{cyan_color} Periodo:  {grade_dict['_periodo_id']}  Profesor: {grade_dict['_profesor_id']}  Asignatura: {grade_dict['_asignatura_id']} {reset_color}')

                    for detalle in grade_dict['_detalleNota']:
                        estudiantes_data = JsonFile(f'{path}/data/students.json').read()
                        estudiante_data = next((s for s in estudiantes_data if s['_cedula'] == detalle['_estudiante']['_cedula']), None)  # Corrección aquí
                        if estudiante_data:
                            nombre_estudiante = estudiante_data['_nombre'] + " " + estudiante_data['_apellido']
                        else:
                            nombre_estudiante = "Estudiante no encontrado"

                        # Calcular el promedio utilizando el método de DetalleNota
                        detalle_nota_obj = DetalleNota(None, detalle['_estudiante']['_cedula'], detalle['_nota1'], detalle['_nota2'], detalle.get('_recuperacion'), detalle.get('_observacion'))
                        promedio = detalle_nota_obj.calcular_promedio()
                        if promedio is None:  # Verificar si hubo un error en el cálculo del promedio
                            estado = "Error en el cálculo"
                        else:
                            estado = "Aprobado" if promedio >= 70 else "Reprobado"

                        print(f"  - Estudiante: {nombre_estudiante}, Nota 1: {detalle['_nota1']}, Nota 2: {detalle['_nota2']}, Recuperación: {detalle.get('_recuperacion')}, Observación: {detalle.get('_observacion')}, Promedio: {promedio}, Estado: {estado}")

            elif opcion == '2':
                borrarPantalla()
                id = self.valida.solo_numeros("Ingrese el ID del registro a buscar: ", "ID inválido. Ingrese un número entero positivo.", 0, 5)
                grade_dict = next((g for g in data if g['_id'] == int(id)), None)
                if grade_dict:
                    print(f"\nID: {grade_dict['_id']}, Periodo: {grade_dict['_periodo_id']}, Profesor: {grade_dict['_profesor_id']}, Asignatura: {grade_dict['_asignatura_id']}")
                    for detalle in grade_dict['_detalleNota']:
                        estudiantes_data = JsonFile(f'{path}/data/students.json').read()
                        estudiante_data = next((s for s in estudiantes_data if s['_cedula'] == detalle['_estudiante']['_cedula']), None)  
                        if estudiante_data:
                            nombre_estudiante = estudiante_data['_nombre'] + " " + estudiante_data['_apellido']
                        else:
                             nombre_estudiante = "Estudiante no encontrado"
                        
                        # Calcular el promedio utilizando el método de DetalleNota
                        detalle_nota_obj = DetalleNota(None, detalle['_estudiante']['_cedula'], detalle['_nota1'], detalle['_nota2'], detalle.get('_recuperacion'), detalle.get('_observacion'))
                        promedio = detalle_nota_obj.calcular_promedio()
                        if promedio is None:  # Verificar si hubo un error en el cálculo del promedio
                            estado = "Error en el cálculo"
                        else:
                            estado = "Aprobado" if promedio >= 70 else "Reprobado"

                        print(f"  - Estudiante: {nombre_estudiante}, Nota 1: {detalle['_nota1']}, Nota 2: {detalle['_nota2']}, Recuperación: {detalle.get('_recuperacion')}, Observación: {detalle.get('_observacion')}, Promedio: {promedio}, Estado: {estado}")

                else:
                    print(f"{red_color}{' Registro de notas no encontrado. '.center(80)}{reset_color}")
                    time.sleep(2)

            elif opcion == '3':
                break
            else:
                print(f"{red_color}{' Opción inválida. Intente de nuevo. '.center(80)}{reset_color}")
                time.sleep(2)



