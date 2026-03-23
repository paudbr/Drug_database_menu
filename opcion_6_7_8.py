#Importamos los módulos y clases necesarios
import mysql.connector
from mysql.connector import errorcode
from tabulate import tabulate
from conexion_bd import BD

class Modif:
    def delete_association(association_number):
        from menu_principal import Menu
        try: #para manejar excepciones
            cursor = BD.db.cursor()

            # Se valida el número de la tabla de asociaciones que quiere borrar el usuario
            if not association_number.isdigit():
                print("Número de asociación no válido.")
                return

            association_number = int(association_number)

            # Se hace una consulta para obtener la información de las 10 asociaciones con el menor score
            consulta = "SELECT disease_code.name as nombre_enfermedad, d.drug_name as nombre_farmaco, dd.inferred_score as score_asociacion FROM disease_code JOIN drug_disease as dd on disease_code.code_id = dd.code_id JOIN drug as d on dd.drug_id = d.drug_id WHERE dd.inferred_score IS NOT NULL ORDER BY dd.inferred_score ASC LIMIT 10;"
            cursor.execute(consulta)
            associations = cursor.fetchall()

            if 1 <= association_number <= len(associations): #verifica que el número de asociación es mayor o igual a 1 y menor o igual al número total de asociaciones en la lista (10)
                association_info = associations[association_number - 1]
                disease_name = association_info[0]
                drug_name = association_info[1]

                print("Association Info:", association_info)  #Le muestra al usuario la información que va a borrar

                # Confirma el borrado de la asociación
                confirmation = input(f"¿Estás seguro de querer borrar la asociación número {association_number}? (y/n): ").lower()

                if confirmation == 'y':
                    # Query para borrar esa infroación
                    delete_query = "DELETE FROM drug_disease WHERE code_id=(SELECT code_id FROM disease_code WHERE name=%s) AND drug_id=(SELECT drug_id FROM drug WHERE drug_name=%s);"
                    cursor.execute(delete_query, (disease_name, drug_name))
                    print(f"Filas afectadas por el borrado: {cursor.rowcount}")
                    BD.db.commit() #actualización de la base de datos 
                    print(f"Asociación número {association_number} eliminada con éxito.")
                    Menu.salir_menu(Modif.seis) #pregunta al usuario sobre salida al menú
                else:
                    print("Operación de borrado cancelada por el usuario.")
                    Menu.salir_menu(Modif.seis)
            else:
                print("Número de asociación no válido.")

        except mysql.connector.Error as err:
            print(f"Error de MySQL: {err}")
            BD.cerrar_conexion()
        except Exception as e:
            print(f"Error: {e}")

    def seis():
        from menu_principal import Menu
        try:
            cursor = BD.db.cursor() 
            # Te da las 10 asociaciones con menor score
            consulta = "SELECT disease_code.name as nombre_enfermedad, d.drug_name as nombre_farmaco, dd.inferred_score as score_asociacion FROM disease_code JOIN drug_disease as dd on disease_code.code_id = dd.code_id JOIN drug as d on dd.drug_id = d.drug_id WHERE dd.inferred_score IS NOT NULL ORDER BY dd.inferred_score ASC LIMIT 10;"
            cursor.execute(consulta)
            resultado = cursor.fetchall()

            # Agregar una columna con el número de fila
            resultado_con_numeros = [(i + 1,) + row for i, row in enumerate(resultado)]

            # Obtener los nombres de las columnas
            columnas = ['Número'] + [desc[0] for desc in cursor.description]

            # Imprimir los resultados en formato tabulate
            print("A continuación, se muestran las 10 primeras interacciones con un score menor:")
            print(tabulate(resultado_con_numeros, headers=columnas, tablefmt='grid'))
            
            borrar= input("Escribe el número de la asociación que quieras borrar o 0 para salir: ")
            
            if borrar.isdigit() and int(borrar) != 0:
                Modif.delete_association(borrar) #llama a la función definida previamente
            else:
                print("Borrado cancelado por el usuario, saliendo...")
        except mysql.connector.Error as err:
            print(f"Error de MySQL: {err}")
            BD.cerrar_conexion()
        except Exception as e:
            print(f"Error: {e}")

    def siete():
        from menu_principal import Menu
        nombre_farmaco=input ("Por favor, introduce el nombre del fármaco al que quieras añadir nueva codificación: ")
        try:
                cursor = BD.db.cursor()

                # Comprueba que el fármaco introducido por el usuario existe
                consulta = "SELECT COUNT(*) FROM drug WHERE drug_name = %s;"
                cursor.execute(consulta, (nombre_farmaco,))
                resultado = cursor.fetchone()

                if resultado[0] > 0:
                    print("El fármaco existe en la base de datos, puedes continuar.")
                    try:
                        salida2=input("Si quieres volver al menú principal pulsa 0, si quieres continuar teclea cualquier otro número: ")
                        if int(salida2) == 0:
                            print("Inserción cancelada, saliendo...")
                            Menu.menu_principal()
                        else:
                            nueva_codif = input("Introduce el nuevo identificador del fármaco: ")
                            nuevo_vocab = input("Introduce el nombre del vocabulario correspondiente: ")

                            if not nueva_codif or not nuevo_vocab:
                                print("Por favor, introduce códigos/nombres no nulos")
                                Menu.salir_menu(Modif.siete)
                            else:

                                # Insert new codification
                                consulta_dos = "INSERT INTO drug_has_code (drug_id, code_id, vocabulary) " \
                                            "SELECT drug.drug_id, %s, %s FROM drug WHERE drug.drug_name = %s;"
                                asegurar=input("¿Seguro que quieres añadir estos valores a la base de datos? y/n: ")
                                if asegurar.lower() == "y":
                                    cursor.execute(consulta_dos, (nueva_codif, nuevo_vocab, nombre_farmaco))
                                    BD.db.commit()
                                    print('Número de filas afectadas: %s' % (cursor.rowcount))
                                    Menu.salir_menu(Modif.siete)
                                elif asegurar.lower() == "n":
                                    Menu.salir_menu(Modif.siete)
                                else:
                                    print("Opción no válida.")
                                    Menu.salir_menu(Modif.siete)
                    except ValueError:
                        print("Opción no válida...debes ingresar un número entero.")
                        Menu.salir_menu(Modif.siete)
                else:
                    print("No existe ese fármaco en la base de datos")
                    Menu.salir_menu(Modif.siete)
        except mysql.connector.Error as err:
            print(f"Error de MySQL: {err}")
            BD.cerrar_conexion()
        except Exception as e:
            print(f"Error: {e}")

    def ocho():
        from menu_principal import Menu
        try:
            numero_score=input("Por favor, introduce un valor numérico para actualizar todos los scores asociados a efectos secundarios menores que ese valor a 0: ")
            if numero_score.replace('.', '', 1).isdigit():
                cursor = BD.db.cursor()
                consulta_update="UPDATE drug_phenotype_effect SET score=0 WHERE score < %s AND phenotype_type='SIDE EFFECT';"
                asegurar=input('¿Seguro que quieres cambiar el valor de este score por 0? y/n: ')
                if asegurar.lower() == "y":
                    cursor.execute(consulta_update,(numero_score,))
                    BD.db.commit()
                    print('Número de filas afectadas: %s' % (cursor.rowcount))
                    Menu.salir_menu(Modif.ocho)              
                elif asegurar.lower() == "n":
                    Menu.salir_menu(Modif.ocho)
            else:
                print("\nEl valor introducido no es válido.")
                Modif.ocho()
        except mysql.connector.Error as err:
            print(f"Error de MySQL: {err}")
            BD.cerrar_conexion()
        except Exception as e:
            print(f"Error: {e}")

