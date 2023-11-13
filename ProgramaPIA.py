from datetime import date, datetime
import sys
import sqlite3
from sqlite3 import Error
import datetime
import openpyxl
import csv
import re

try:
    with sqlite3.connect ('Evidencia3_Prueba.db') as conn:
        mi_cursor=conn.cursor()
        mi_cursor.execute("CREATE TABLE IF NOT EXISTS clientes \
        (clave_cliente INTEGER PRIMARY KEY, nombre_cliente TEXT NOT NULL, RFC TEXT NOT NULL, correo_cliente TEXT NOT NULL, estatus TEXT NOT NULL);")

        mi_cursor.execute("CREATE TABLE IF NOT EXISTS servicios \
        (clave_servicio INTEGER PRIMARY KEY, nombre_servicio TEXT NOT NULL, costo_servicio NUMBER, estatus INTEGER NOT NULL);")

        mi_cursor.execute("CREATE TABLE IF NOT EXISTS notas (folio_nota INTEGER PRIMARY KEY, fecha_nota timestamp, clave_cliente INTEGER NOT NULL, total_nota NUMBER, estatus TEXT NOT NULL, FOREIGN KEY (clave_cliente) REFERENCES clientes (clave_cliente));")

        mi_cursor.execute("CREATE TABLE IF NOT EXISTS detalle_notas (id_detalle INTEGER PRIMARY KEY, folio_nota INTEGER NOT NULL, clave_servicio INTEGER NOT NULL, FOREIGN KEY (folio_nota) REFERENCES NOTAS (folio_nota), FOREIGN KEY (clave_servicio) REFERENCES servicios (clave_servicio));")

        print ('Tablas creadas exitosamente')

#############################CLIENTES
        def agregar_cliente():
            while True:
                try:
                    nombre_cliente=input("Ingrese el nombre del cliente: ").strip()
                    nombre_cliente=nombre_cliente.capitalize()
                    if not nombre_cliente.strip():
                        print('NO SE PUEDE QUEDAR EL NOMBRE DEL CLIENTE EN BLANCO, INTENTE DE NUEVO')
                        continue
                    if nombre_cliente.isdigit():
                        print('EL NOMBRE DEL CLIENTE NO PUEDE SER UN NÚMERO, INTENTE DE NUEVO')
                        continue
                    else:
                        break
                except ValueError:
                    print('Ingrese un nombre válido. Intentélo de nuevo.')
                    continue

            while True:
                try:
                    RFC=input("Ingrese el RFC del cliente (formato: ABCD123456XXX): ").strip().upper()
                    if RFC.strip() == '':
                        print("NO ES POSIBLE DEJAR EL RFC EN BLANCO, INTENTE DE NUEVO")
                        continue
                    if not re.match(r'^[A-Z&Ñ]{4}(0[0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-3])(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])[0-9A-Z]{3}$', RFC):
                        print(f"\nEL FORMATO DEL RFC ES INCORRECTO, INTENTE DE NUEVO (formato: ABCD123456XXX)")
                        continue
                    else:
                        break
                except ValueError:
                    print('Ingrese un nombre válido. Intentélo de nuevo.')
                    continue

            while True:
                try:
                    correo_cliente=input("Ingrese el correo electrónico del cliente (formato: tunombre@ejemplo.com): ")
                    validacion="(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"

                    if correo_cliente.strip() == '':
                        print("NO ES POSIBLE DEJAR EL CORREO EN BLANCO, INTENTE DE NUEVO")
                        continue

                    if not re.match(validacion, correo_cliente):
                        print("EL FORMATO DEL CORREO ES INCORRECTO, INTENTE DE NUEVO")
                        continue

                    else:
                        estatus= '1'
                        with sqlite3.connect ('Evidencia3_Prueba.db') as conn:
                            mi_cursor= conn.cursor()
                            valores=(nombre_cliente, RFC, correo_cliente, estatus)
                            mi_cursor.execute("INSERT INTO clientes (nombre_cliente, RFC, correo_cliente, estatus) VALUES (?,?,?,?)", valores)
                            conn.commit()

                            clave_cliente=mi_cursor.lastrowid
                            print(f'Se registró el cliente con la clave: {clave_cliente}')
                            break

                except ValueError:
                    print('Ingrese un correo válido. Intentélo de nuevo.')
                    continue
        def suspender_cliente():
          try:
            with sqlite3.connect('Evidencia3_Prueba.db') as conn:
              mi_cursor = conn.cursor()

              mi_cursor.execute("SELECT clave_cliente, nombre_cliente FROM clientes WHERE estatus='1'")
              clientes_activos = mi_cursor.fetchall()

              if not clientes_activos:
                print("No hay clientes activos para suspender.")
                return

              print("\nReporte de Clientes Activos:")
              print("Clave cliente\t\tNombre cliente")
              for cliente in clientes_activos:
                print(f"\t{cliente[0]}\t\t{cliente[1]}")

              clave_suspender = input("\nIngrese la clave del cliente que desea suspender (0 para volver al menú anterior): ").strip()
              if clave_suspender == '0':
                print("Volviendo al menú anterior.")
                return

              mi_cursor.execute("SELECT * FROM clientes WHERE clave_cliente=? AND estatus='1'", (clave_suspender,))
              cliente_suspender = mi_cursor.fetchone()

              if not cliente_suspender:
                print("Clave de cliente no válida.")
                return

              # Mostrar los datos del cliente y solicitar confirmación
              print("\nDatos del cliente a suspender:")
              print(f"Clave cliente: {cliente_suspender[0]}")
              print(f"Nombre cliente: {cliente_suspender[1]}")
              print(f"RFC: {cliente_suspender[2]}")
              print(f"Correo cliente: {cliente_suspender[3]}")

              confirmacion = input("\n¿Desea suspender a este cliente? (Sí/No): ").strip().lower()
              if confirmacion == 'si':
                # Actualizar el estatus del cliente a suspendido
                mi_cursor.execute("UPDATE clientes SET estatus='0' WHERE clave_cliente=?", (clave_suspender,))
                conn.commit()
                print(f"El cliente con clave {cliente_suspender[0]} ha sido suspendido.")
              else:
                print("Operación cancelada. Volviendo al menú anterior.")

          except Exception as e:
            print(f"Ocurrió un error: {str(e)}")


        def recuperar_cliente():
          try:
           with sqlite3.connect('Evidencia3_Prueba.db') as conn:
            mi_cursor = conn.cursor()

            mi_cursor.execute("SELECT clave_cliente, nombre_cliente FROM clientes WHERE estatus = '0'")
            clientes_suspendidos = mi_cursor.fetchall()

            if not clientes_suspendidos:
              print("No hay clientes suspendidos para recuperar")
              return

            print("\nReporte de Clientes Suspendidos:")
            print("Clave cliente\t\tNombre cliente")
            for cliente in clientes_suspendidos:
             print(f"\t{cliente[0]}\t\t{cliente[1]}")

        # Solicitar al usuario que elija una clave de cliente para recuperar
            clave_recuperar = input("\nIngrese la clave del cliente que desea recuperar (0 para volver al menú anterior): ").strip()

            if clave_recuperar == '0':
             print("Volviendo al menú anterior.")
             return
            mi_cursor.execute("SELECT * FROM clientes WHERE clave_cliente=? AND estatus='0'", (clave_recuperar,))
            cliente_recuperar = mi_cursor.fetchone()

            if not cliente_recuperar:
             print("Clave de cliente no válida.")
             return
        # Mostrar los datos del cliente y solicitar confirmación
            print("\nDatos del cliente a recuperar:")
            print(f"Clave cliente: {cliente_recuperar[0]}")
            print(f"Nombre cliente: {cliente_recuperar[1]}")
            print(f"RFC: {cliente_recuperar[2]}")
            print(f"Correo cliente: {cliente_recuperar[3]}")
            confirmacion = input("\n¿Desea recuperar a este cliente? (Sí/No): ").strip().lower()

            if confirmacion == 'si' or confirmacion == 'SI':
            # Actualizar el estatus del cliente a activo
             mi_cursor.execute("UPDATE clientes SET estatus='1' WHERE clave_cliente=?", (clave_recuperar,))
             conn.commit()
             print(f"El cliente con clave {cliente_recuperar[0]} ha sido recuperado.")
            else:
              print("Operación cancelada. Volviendo al menú anterior.")
          except Exception as e:
           print(f"Ocurrió un error: {str(e)}")
        #consultas y reportes de clientes
        #LISTADO DE clientes
        def ordenar_cliente_por_clave():
            while True:
                try:
                    with sqlite3.connect ('Evidencia3_Prueba.db') as conn:
                        mi_cursor= conn.cursor()
                        print(f"\nClientes ordenados por clave: ")
                        mi_cursor.execute(f"SELECT * FROM clientes WHERE estatus='1' ORDER BY clave_cliente")
                        clientes_orden_clave=mi_cursor.fetchall()
                        print(f"\nClave cliente\t\tNombre cliente\t\tRFC\t\t\tCorreo cliente")
                        for cliente in clientes_orden_clave:
                            print(f"\t{cliente[0]}\t\t{cliente[1]}\t\t{cliente[2]}\t\t{cliente[3]}")

                        print(f"\nOpciones de exportación:")
                        print(f"1. Excel")
                        print(f"2. CSV")
                        print(f"3. Volver a menú de reportes")

                        opcion_exportar=int(input(f'\nOpción a elegir: '))
                        match opcion_exportar:
                            case 1:
                                workbook = openpyxl.Workbook()
                                sheet = workbook.active
                                sheet.title = "Clientes_Ordenados_Clave"

                                sheet['A1'] = "Clave cliente"
                                sheet['B1'] = "Nombre cliente"
                                sheet['C1'] = "RFC"
                                sheet['D1'] = "Correo cliente"

                                row = 2
                                for cliente in clientes_orden_clave:
                                    sheet[f'A{row}'] = cliente[0]
                                    sheet[f'B{row}'] = cliente[1]
                                    sheet[f'C{row}'] = cliente[2]
                                    sheet[f'd{row}'] = cliente[3]
                                    row+=1

                                fecha_actual=datetime.date.today()
                                fecha_reporte = fecha_actual.strftime("%m-%d-%Y")

                                nombre_archivo_excel = f"ReporteClientesActivosPorClave_{fecha_reporte}.xlsx"
                                workbook.save(nombre_archivo_excel)
                                print(f"Se ha exportado la información a '{nombre_archivo_excel}'.")
                                break

                            case 2:
                                fecha_actual=datetime.date.today()
                                fecha_reporte = fecha_actual.strftime("%m-%d-%Y")

                                nombre_archivo_csv=f"ReporteClientesActivosPorClave_{fecha_reporte}.csv"
                                with open(nombre_archivo_csv, 'w', newline='') as file:
                                    writer = csv.writer(file)
                                    writer.writerow(["Clave cliente", "Nombre cliente", "RFC", "Correo cliente"])
                                    for cliente in clientes_orden_clave:
                                        writer.writerow([cliente[0], cliente[1], cliente[2], cliente[3]])

                                    print(f"Se ha exportado la información a '{nombre_archivo_csv}'.")
                                    break

                            case 3:
                                print('VOLVIENDO AL MENÚ DE REPORTES.')
                                break
                            case _:
                                print("OPCIÓN NO VÁLIDA. INGRESE UN NÚMERO DEL 1 AL 3.")

                except ValueError:
                    print('INGRESE UNA OPCIÓN VÁLIDA')

                except Exception as e:
                    print(f"Ocurrió un error: {str(e)}")


        def ordenar_cliente_por_nombre():
            while True:
                try:
                    with sqlite3.connect ('Evidencia3_Prueba.db') as conn:
                        mi_cursor= conn.cursor()
                        print(f"\nClientes ordenados por nombre: ")
                        mi_cursor.execute(f"SELECT * FROM clientes WHERE estatus='1' ORDER BY nombre_cliente")
                        clientes_orden_clave=mi_cursor.fetchall()
                        print(f"\nClave cliente\t\tNombre cliente\t\tRFC\t\t\tCorreo cliente")
                        for cliente in clientes_orden_clave:
                            print(f"\t{cliente[0]}\t\t{cliente[1]}\t\t{cliente[2]}\t\t{cliente[3]}")

                        print(f"\nOpciones de exportación:")
                        print(f"1. Excel")
                        print(f"2. CSV")
                        print(f"3. Volver a menú de reportes")

                        opcion_exportar=int(input(f'\nOpción a elegir: '))
                        match opcion_exportar:
                            case 1:
                                workbook = openpyxl.Workbook()
                                sheet = workbook.active
                                sheet.title = "Clientes_Ordenados_Clave"

                                sheet['A1'] = "Clave cliente"
                                sheet['B1'] = "Nombre cliente"
                                sheet['C1'] = "RFC"
                                sheet['D1'] = "Correo cliente"

                                row = 2
                                for cliente in clientes_orden_clave:
                                    sheet[f'A{row}'] = cliente[0]
                                    sheet[f'B{row}'] = cliente[1]
                                    sheet[f'C{row}'] = cliente[2]
                                    sheet[f'd{row}'] = cliente[3]
                                    row+=1

                                fecha_actual=datetime.date.today()
                                fecha_reporte = fecha_actual.strftime("%m-%d-%Y")

                                nombre_archivo_excel = f"ReporteClientesActivosPorNombre_{fecha_reporte}.xlsx"
                                workbook.save(nombre_archivo_excel)
                                print(f"Se ha exportado la información a '{nombre_archivo_excel}'.")
                                break

                            case 2:
                                fecha_actual=datetime.date.today()
                                fecha_reporte = fecha_actual.strftime("%m-%d-%Y")

                                nombre_archivo_csv=f"ReporteClientesActivosPorNombre_{fecha_reporte}.csv"
                                with open(nombre_archivo_csv, 'w', newline='') as file:
                                    writer = csv.writer(file)
                                    writer.writerow(["Clave cliente", "Nombre cliente", "RFC", "Correo cliente"])
                                    for cliente in clientes_orden_clave:
                                        writer.writerow([cliente[0], cliente[1], cliente[2], cliente[3]])

                                    print(f"Se ha exportado la información a '{nombre_archivo_csv}'.")
                                    break

                            case 3:
                                print('VOLVIENDO AL MENÚ DE REPORTES.')
                                break
                            case _:
                                print("OPCIÓN NO VÁLIDA. INGRESE UN NÚMERO DEL 1 AL 3.")

                except ValueError:
                    print('INGRESE UNA OPCIÓN VÁLIDA')

                except Exception as e:
                    print(f"Ocurrió un error: {str(e)}")

        def buscar_cliente_por_clave(clave):
            with sqlite3.connect('Evidencia3_Prueba.db') as conn:
                mi_cursor = conn.cursor()
                mi_cursor.execute("SELECT * FROM clientes WHERE clave_cliente = ?", (clave,))
                cliente = mi_cursor.fetchone()

                if cliente:
                    print(f"Cliente encontrado por clave {clave}:")
                    print("{:<15} {:<20} {:<15} {:<20}".format("Clave cliente", "Nombre cliente", "RFC", "Correo cliente"))
                    print("{:<15} {:<20} {:<15} {:<20}".format(cliente[0], cliente[1], cliente[2], cliente[3]))
                else:
                    print("No se encontró ningún cliente con esa clave.")

        def buscar_cliente_por_nombre(nombre):
            with sqlite3.connect('Evidencia3_Prueba.db') as conn:
                mi_cursor = conn.cursor()
                mi_cursor.execute("SELECT * FROM clientes WHERE nombre_cliente = ?", (nombre,))
                clientes = mi_cursor.fetchall()

                if clientes:
                    print(f"Clientes encontrados por nombre '{nombre}':")
                    print("{:<15} {:<20} {:<15} {:<20}".format("Clave cliente", "Nombre cliente", "RFC", "Correo cliente"))
                    for cliente in clientes:
                        print("{:<15} {:<20} {:<15} {:<20}".format(cliente[0], cliente[1], cliente[2], cliente[3]))
                else:
                    print("No se encontraron clientes con ese nombre.")

        def agregar_servicio():
            while True:
                try:
                    nombre_servicio=input("Ingrese el nombre del servicio: ").strip()
                    nombre_servicio=nombre_servicio.capitalize()
                    if not nombre_servicio.strip():
                        print('NO SE PUEDE QUEDAR EL NOMBRE DEL SERVICIO EN BLANCO, INTENTE DE NUEVO')
                        continue
                    if nombre_servicio.isdigit():
                        print('EL NOMBRE DEL SERVICIO NO PUEDE SER UN NÚMERO, INTENTE DE NUEVO')
                        continue
                    else:
                        break
                except ValueError:
                    print('Ingrese un nombre válido. Intentélo de nuevo.')
                    continue


            while True:
                try:
                    costo_servicio=int(input('Ingrese el costo del servicio: '))
                    if costo_servicio == 0:
                        print('EL COSTO DEL SERVICIO NO PUEDE SER 0. INTENTE DE NUEVO')
                        continue
                    if not costo_servicio:
                        print('EL COSTO DEL SERVICIO NO PUEDE QUEDAR EN BLANCO. INTENTE DE NUEVO')
                        continue
                    elif costo_servicio <= 0:
                        print('EL COSTO DEL SERVICIO DEBE SER MAYOR A 0. INTENTE DE NUEVO')
                        continue
                    else:
                        with sqlite3.connect ('Evidencia3_Prueba.db') as conn:
                            mi_cursor= conn.cursor()
                            valores=(nombre_servicio, costo_servicio, 1)
                            mi_cursor.execute("INSERT INTO servicios (nombre_servicio, costo_servicio, estatus) VALUES (?,?,?)", valores)
                            conn.commit()

                            clave_servicio=mi_cursor.lastrowid
                            print(f'Se registró el servicio con la clave: {clave_servicio}')
                            break

                except ValueError:
                    print('Ingrese un costo válido. Intentélo de nuevo.')
                    continue


        def servicios_suspender():
          try:
            with sqlite3.connect('Evidencia3_Prueba.db') as conn:
                 mi_cursor = conn.cursor()
                 print("\nServicios:")
                 mi_cursor.execute("SELECT clave_servicio, nombre_servicio FROM servicios")
                 servicios_activos = mi_cursor.fetchall()

                 if not servicios_activos:
                     print("No se encontraron servicios para suspender por el momento.")
                     return

                 print("\nClave servicio\t\tNombre servicio")
                 for servicio in servicios_activos:
                     print(f"\t{servicio[0]}\t\t{servicio[1]}")

            while True:
                try:
                    clave_servicio_suspender = int(input("Ingrese la clave del servicio que quieres suspender o 0 para regresar al menú anterior."))
                    if clave_servicio_suspender == 0:
                        print("Regresando al menú anterior.")
                        return
                    elif mi_cursor.execute("SELECT COUNT (*) FROM servicios WHERE clave_servicio =? AND estatus= '1'", (clave_servicio_suspender,)).fetchone()[0] == 0:
                        print("La clave es incorrecta o no se encuentra disponible. Intente de nuevo")
                    else:
                        break
                except ValueError:
                    print("Ingrese una opción válida.")
                    mi_cursor.execute("SELECT * FROM servicios WHERE clave_servicio=?", (clave_servicio_suspender,))
                    servicio_suspender = mi_cursor.fetchone()
                    print("\tDatos del servicio a suspender:")
                    print(f"\nClave servicio\t\tNombre servicio\t\tCosto servicio")
                    print(f"\t{servicio_suspender[0]}\t\t{servicio_suspender[1]}\t\t{servicio_suspender[2]}")

            while True:
               confirmacion = input("\n¿Desea suspender este servicio? (Si/No):").strip().lower()
               if confirmacion == 'si' or confirmacion == 's':
                  mi_cursor.execute("UPDATE servicios SET estatus= '0' WHERE clave_servicio=?", (clave_servicio_suspender,))
                  conn.commit()
                  print(f"El servicio con clave {clave_servicio_suspender} se ha suspendido.")
                  return
               elif confirmacion == 'no' or confirmacion == 'n':
                    print("Se canceló la acción. Volviendo al menú anterior.")
                    return
               else:
                    print("Ingrese 'Si' o 'No'.")
          except Exception as e:
               print(f"Ocurrió un error: {str(e)}")


        def recuperar_servicio():
          try:
            with sqlite3.connect('Evidencia3_Prueba.db') as conn:
               mi_cursor = conn.cursor()
               print("\nServicios suspendidos")
               mi_cursor.execute("SELECT clave_servicio, nombre_servicio, costo_servicio FROM servicios WHERE estatus= '0'")
               servicios_suspendidos = mi_cursor.fetchall()

               if not servicios_suspendidos:
                  print("No se encuentran servicios suspendidos por el momento.")
                  return

               print("\nClave servicio\t\tNombre servicio\t\tCosto servicio")
               for servicio in servicios_suspendidos:
                   print(f"\t{servicio[0]}\t\t{servicio[1]}\t\t{servicio[2]}")

               while True:
                try:
                    clave_servicio_recuperar = int(input("Ingrese la clave del servicio a recuperar o 0 para regresar al menú anterior."))
                    if clave_servicio_recuperar == 0:
                        print("Volviendo al menú anterior.")
                        return
                    elif mi_cursor.execute("SELECT COUNT(*) FROM servicios WHERE clave_servicio=? AND estatus='0'", (clave_servicio_recuperar,)).fetchone()[0] == 0:
                        print("La clave es incorrecta o el servicio no se encuentra suspendido. Intente de nuevo.")
                    else:
                        break
                except ValueError:
                    print("Ingrese una opción válida.")

               mi_cursor.execute("SELECT * FROM servicios WHERE clave_servicio =?", (clave_servicio_recuperar,))
               servicio_recuperar = mi_cursor.fetchone()

               print("\nDatos del servicio a recuperar.")
               print("\nClave servicio\t\tNombre servicio\t\tCosto servicio")
               print(f"\t{servicio_recuperar[0]}\t\t{servicio_recuperar[1]}\t\t{servicio_recuperar[2]}")

               while True:
                  confirmacion = input("\n¿Desea recuperar el servicio suspendido? (Si/No):").strip().lower()
                  if confirmacion == 'si':
                     mi_cursor.execute("UPDATE servicios SET estatus= '1' WHERE clave_servicio=?", (clave_servicio_recuperar,))
                     conn.commit()
                     print(f"\nEl servicio con clave {clave_servicio_recuperar} se ha recuperado.")
                     return
                  elif confirmacion == 'no':
                       print("Se canceló la acción. Volviendo al menú anterior.")
                       return
                  else:
                       print("Ingrese 'Si' o 'No'.")
          except Exception as e:
                 print(f"Ocurrió un error: {str(e)}")

        
        def buscar_servicio_por_clave():
            print(f'\nLista de servicios: ')
            with sqlite3.connect ('Evidencia3_Prueba.db') as conn:
                mi_cursor= conn.cursor()
                mi_cursor.execute("SELECT clave_servicio, nombre_servicio FROM servicios WHERE estatus= '1'")
                lista_servicios=mi_cursor.fetchall()
                print(f"\nClave servicio\tNombre servicio")
                for servicio in lista_servicios:
                    print(f"\t{servicio[0]}\t{servicio[1]}")
            while True:
                try:
                    clave_servicio=int(input(f'\nIngrese la clave del servicio a consultar / Si no se va consultar un servicio escriba 0: '))
                    if clave_servicio==0:
                        print('USTED HA DECIDIDO NO CONSULTAR NINGUN SERVICIO')
                        break
                    if not clave_servicio:
                        print('LA CLAVE NO SE PUEDE QUEDAR EN BLANCO. INGRESE UNA CLAVE VÁLIDA')
                        continue
                    with sqlite3.connect ('Evidencia3_Prueba.db') as conn:
                        mi_cursor= conn.cursor()
                        mi_cursor.execute(f"SELECT * FROM servicios WHERE clave_servicio={clave_servicio}")
                        servicios_clave=mi_cursor.fetchall()
                        if clave_servicio not in [servicio[0] for servicio in servicios_clave]:
                            print('El servicio no se encuentra en el sistema. Por favor, ingrese una clave válida.')
                            continue
                        else:
                            print(f"\nClave servicio\t\tNombre servicio\t\tCosto servicio")
                            for servicio in servicios_clave:
                                print(f"\t{servicio[0]}\t\t{servicio[1]}\t\t{servicio[2]}")
                            break

                except ValueError:
                    print('Ingrese una clave válida. Intente de nuevo')

        def buscar_servicio_por_nombre():
            while True:
                try:
                    nombre_servicio_buscar=input(f'\nIngrese el nombre del servicio a buscar: ').strip()
                    nombre_servicio=nombre_servicio_buscar.capitalize()

                    if not nombre_servicio.strip():
                        print('NO SE PUEDE QUEDAR EL NOMBRE DEL SERVICIO EN BLANCO, INTENTE DE NUEVO')
                        continue
                    if nombre_servicio.isdigit():
                        print('EL NOMBRE DEL SERVICIO NO PUEDE SER UN NÚMERO, INTENTE DE NUEVO')
                        continue
                    with sqlite3.connect ('Evidencia3_Prueba.db') as conn:
                        mi_cursor= conn.cursor()
                        mi_cursor.execute(f"SELECT * FROM servicios WHERE nombre_servicio='{nombre_servicio} AND estatus= '1''")
                        servicios_nombre=mi_cursor.fetchall()
                        if nombre_servicio not in [servicio[1] for servicio in servicios_nombre]:
                            print('EL SERVICIO NO SE ENCUENTRA EN EL SISTEMA. INGRESE UN NOMBRE VÁLIDO')
                            continue
                        else:
                            print(f"\nClave servicio\t\tNombre servicio\t\tCosto servicio")
                            for servicio in servicios_nombre:
                                print(f"\t{servicio[0]}\t\t{servicio[1]}\t\t${servicio[2]}")
                            break
                except ValueError:
                    print('INGRESE UN NOMBRE VÁLIDO')

            
        def ordenar_servicio_por_clave():
            while True:
                try:
                    with sqlite3.connect ('Evidencia3_Prueba.db') as conn:
                        mi_cursor= conn.cursor()
                        print(f"\nServicios ordenados por clave: ")
                        mi_cursor.execute(f"SELECT * FROM servicios WHERE estatus= '1' ORDER BY clave_servicio")
                        servicios_orden_clave=mi_cursor.fetchall()
                        print(f"\nClave servicio\t\tNombre servicio\t\tCosto servicio")
                        for servicio in servicios_orden_clave:
                            print(f"\t{servicio[0]}\t\t{servicio[1]}\t\t${servicio[2]}")

                        print(f"\nOpciones de exportación:")
                        print(f"1. Excel")
                        print(f"2. CSV")
                        print(f"3. Volver a menú de reportes")

                        opcion_exportar=int(input(f'\nOpción a elegir: '))
                        match opcion_exportar:
                            case 1:
                                workbook = openpyxl.Workbook()
                                sheet = workbook.active
                                sheet.title = "Servicios_Ordenados_Clave"

                                sheet['A1'] = "Clave servicio"
                                sheet['B1'] = "Nombre servicio"
                                sheet['C1'] = "Costo servicio"

                                row = 2
                                for servicio in servicios_orden_clave:
                                    sheet[f'A{row}'] = servicio[0]
                                    sheet[f'B{row}'] = servicio[1]
                                    sheet[f'C{row}'] = servicio[2]
                                    row+=1

                                fecha_actual=datetime.date.today()
                                fecha_reporte = fecha_actual.strftime("%m-%d-%Y")

                                nombre_archivo_excel = f"ReporteServiciosPorClave_{fecha_reporte}.xlsx"
                                workbook.save(nombre_archivo_excel)
                                print(f"Se ha exportado la información a '{nombre_archivo_excel}'.")
                                break

                            case 2:
                                fecha_actual=datetime.date.today()
                                fecha_reporte = fecha_actual.strftime("%m-%d-%Y")

                                nombre_archivo_csv=f"ReporteServiciosPorClave_{fecha_reporte}.csv"
                                with open(nombre_archivo_csv, 'w', newline='') as file:
                                    writer = csv.writer(file)
                                    writer.writerow(["Clave servicio", "Nombre servicio", "Costo servicio"])
                                    for servicio in servicios_orden_clave:
                                        writer.writerow([servicio[0], servicio[1], servicio[2]])

                                    print(f"Se ha exportado la información a '{nombre_archivo_csv}'.")
                                    break
                            case 3:
                                print('VOLVIENDO AL MENÚ DE REPORTES.')
                                break
                            case _:
                                print("OPCIÓN NO VÁLIDA. INGRESE UN NÚMERO DEL 1 AL 3.")

                except ValueError:
                    print('INGRESE UNA OPCIÓN VÁLIDA')

                except Exception as e:
                    print(f"Ocurrió un error: {str(e)}")


        def ordenar_servicio_por_nombre():
            while True:
                try:
                    with sqlite3.connect ('Evidencia3_Prueba.db') as conn:
                        mi_cursor= conn.cursor()
                        print(f"\nServicios ordenados por nombre: ")
                        mi_cursor.execute(f"SELECT * FROM servicios WHERE estatus= '1' ORDER BY nombre_servicio")
                        servicios_orden_nombre=mi_cursor.fetchall()
                        print(f"\nClave servicio\t\tNombre servicio\t\tCosto servicio")
                        for servicio in servicios_orden_nombre:
                            print(f"\t{servicio[0]}\t\t{servicio[1]}\t\t${servicio[2]}")

                        print(f"\nOpciones de exportación:")
                        print(f"1. Excel")
                        print(f"2. CSV")
                        print(f"3. Volver a menú de reportes")

                        opcion_exportar=int(input(f'\nOpción a elegir: '))
                        match opcion_exportar:
                            case 1:
                                workbook = openpyxl.Workbook()
                                sheet = workbook.active
                                sheet.title = "Servicios_Ordenados_Clave"

                                sheet['A1'] = "Clave servicio"
                                sheet['B1'] = "Nombre servicio"
                                sheet['C1'] = "Costo servicio"

                                row = 2
                                for servicio in servicios_orden_nombre:
                                    sheet[f'A{row}'] = servicio[0]
                                    sheet[f'B{row}'] = servicio[1]
                                    sheet[f'C{row}'] = servicio[2]
                                    row+=1

                                fecha_actual=datetime.date.today()
                                fecha_reporte = fecha_actual.strftime("%m-%d-%Y")

                                nombre_archivo_excel = f"ReporteServiciosPorNombre_{fecha_reporte}.xlsx"
                                workbook.save(nombre_archivo_excel)
                                print(f"Se ha exportado la información a '{nombre_archivo_excel}'.")
                                break

                            case 2:
                                fecha_actual=datetime.date.today()
                                fecha_reporte = fecha_actual.strftime("%m-%d-%Y")

                                nombre_archivo_csv=f"ReporteServiciosPorNombre_{fecha_reporte}.csv"
                                with open(nombre_archivo_csv, 'w', newline='') as file:
                                    writer = csv.writer(file)
                                    writer.writerow(["Clave servicio", "Nombre servicio", "Costo servicio"])
                                    for servicio in servicios_orden_nombre:
                                        writer.writerow([servicio[0], servicio[1], servicio[2]])

                                    print(f"Se ha exportado la información a '{nombre_archivo_csv}'.")
                                    break
                            case 3:
                                print('VOLVIENDO AL MENÚ DE REPORTES.')
                                break
                            case _:
                                print("OPCIÓN NO VÁLIDA. INGRESE UN NÚMERO DEL 1 AL 3.")

                except ValueError:
                    print('INGRESE UNA OPCIÓN VÁLIDA')

                except Exception as e:
                    print(f"Ocurrió un error: {str(e)}")


 
