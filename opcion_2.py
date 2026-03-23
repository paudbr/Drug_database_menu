#Importamos los módulos y clases necesarios
import mysql.connector
from mysql.connector import errorcode
from tabulate import tabulate
from conexion_bd import BD

class Dos:
    def dos_a():
        from menu_principal import Menu
        id_pedido= input (" Por favor escribe el id del fármaco del que quieras obtener más información: ")
        try: 
            cursor=BD.db.cursor()

            consulta = f"SELECT COUNT(*) FROM drug WHERE drug_id = '{id_pedido}';"
            cursor.execute(consulta)
            resultado=cursor.fetchone()

            if resultado [0] > 0: #Si al hacer un count el resultado es minimo 1, significa que existe en la base de datos
                print ("ID encontrado")
                consulta2= f"SELECT drug_name AS nombre, molecular_type AS tipo_molecular, chemical_structure AS estructura_quimica, inchi_key FROM drug WHERE COALESCE ( drug_name, molecular_type, chemical_structure, inchi_key) IS NOT NULL AND drug_id= '{id_pedido}';"
                cursor.execute (consulta2)
                resultado_consulta= cursor.fetchall()
                
                columnas = [desc[0] for desc in cursor.description]

                # Imprimir los resultados en formato tabular con encabezados
                print(f"Información para fármaco con ID: {id_pedido}")
                print(tabulate(resultado_consulta, headers=columnas, tablefmt='grid'))
                Menu.salir_menu(Dos.dos_a)
            else:
                print("No existe ese fármaco")
                Menu.salir_menu(Dos.dos_a)
        except mysql.connector.Error as err:
            print(f"Error de MySQL: {err}")
            BD.cerrar_conexion()
        except Exception as e:
            print(f"Error: {e}")         
    def dos_b():
        from menu_principal import Menu
        nombre_pedido= input (" Por favor escribe el nombre del fármaco del que quieras obtener su/s sinónimo/s: ")
        try: 
            cursor=BD.db.cursor()

            consulta = f"SELECT COUNT(*) FROM drug WHERE drug_name = %s;"
            cursor.execute(consulta, (nombre_pedido,))
            resultado=cursor.fetchone()
            
            if resultado [0] > 0:
                print ("Nombre encontrado")
                consulta2= f"SELECT s.synonymous_name AS nombre_sinonimo FROM synonymous as s INNER JOIN drug as d ON d.drug_id = s.drug_id WHERE d.drug_name= %s;"
                cursor.execute (consulta2,(nombre_pedido,))
                resultado_consulta= cursor.fetchall()
                
                columnas = [desc[0] for desc in cursor.description]

                # Imprimir los resultados en formato tabular con encabezados
                print(f"Sinónimos para fármaco con nombre: {nombre_pedido}")
                print(tabulate(resultado_consulta, headers=columnas, tablefmt='grid'))
                Menu.salir_menu(Dos.dos_b)
                
            else:
                print("No existe ese nombre, vuelve a intentarlo.")
                Menu.salir_menu(Dos.dos_b)

        except mysql.connector.Error as err:
            print(f"Error de MySQL: {err}")
            BD.cerrar_conexion()
        except Exception as e:
            print(f"Error: {e}")
    def dos_c():
        from menu_principal import Menu
        codigo_pedido= input("Por favor introduce un identificador de ChEMBL para el fármaco del que quieres obtener su código ATC: ")
        try: 
            cursor=BD.db.cursor()

            consulta = f"SELECT COUNT(*) FROM drug WHERE drug_id = %s;"
            cursor.execute(consulta, (codigo_pedido,))
            resultado=cursor.fetchone()
            
            if resultado [0] > 0:
                print ("Código CHEMBL encontrado")
                consulta_atc="SELECT ATC_code_id FROM atc_code WHERE drug_id= %s;"
                cursor.execute(consulta_atc,(codigo_pedido,))
                resultado_atc= cursor.fetchall()
                
                if resultado_atc:
                    columnas = [desc[0] for desc in cursor.description]

                    # Imprimir los resultados en formato tabular con encabezados
                    print(f"Código/s ATC para el fármaco con código CHEMBL {codigo_pedido}:")
                    print(tabulate(resultado_atc, headers=columnas, tablefmt='grid'))
                    Menu.salir_menu(Dos.dos_c)
                    
                else:
                    print(f"No hay códigos ATC para el fármaco con código CHEMBL {codigo_pedido}.")
                    Menu.salir_menu(Dos.dos_c)
            else:
                print("No existe ese código, vuelve a intentarlo" )
                Menu.salir_menu(Dos.dos_c)
        except mysql.connector.Error as err:
            print(f"Error de MySQL: {err}")
            BD.cerrar_conexion()
        except Exception as e:
            print(f"Error: {e}")