#Importamos los módulos y clases necesarios
import mysql.connector
from mysql.connector import errorcode
from tabulate import tabulate
from conexion_bd import BD

class Cinco:
    def cinco_a():
        from menu_principal import Menu
        target_type= input("Escribe el tipo de diana del que quieras saber más información: ")
        try :
            cursor=BD.db.cursor()
            
            consulta = f"SELECT COUNT(*) FROM target WHERE target_type = %s;"
            cursor.execute(consulta, (target_type,))
            resultado=cursor.fetchone()
            
            if resultado [0] > 0:
                print ("Tipo de diana encontrada")
                consulta_diana=f"SELECT target_name_pref FROM target WHERE target_type=%s ORDER BY target_name_pref ASC LIMIT 20;"
                cursor.execute(consulta_diana,(target_type,))
                resultado_diana=cursor.fetchall()
                if resultado_diana:
                    # Obtener los nombres de las columnas directamente del cursor
                    columnas = [desc[0] for desc in cursor.description]

                    # Imprimir los resultados en formato tabular con encabezados
                    print(f"20 primeras dianas del tipo {target_type}, ordenadas alfabéticamente:")
                    print(tabulate(resultado_diana, headers=columnas, tablefmt='grid'))
                    Menu.salir_menu(Cinco.cinco_a)
                else:
                    print(f"No hay dianas asociadas al tipo {target_type}.")
                    Menu.salir_menu(Cinco.cinco_a)
            else:
                print("No existe ese tipo de diana, vuelve a intentarlo" )
                Menu.salir_menu(Cinco.cinco_a)
        except mysql.connector.Error as err:
            print(f"Error de MySQL: {err}")
            BD.cerrar_conexion()
        except Exception as e:
            print(f"Error: {e}")

    def cinco_b():
        from menu_principal import Menu
        try:
            cursor=BD.db.cursor()
            consulta= "SELECT o.taxonomy_name AS organismo, COUNT(DISTINCT t.target_id) AS numero_dianas FROM organism o JOIN target t ON t.organism_id=o.taxonomy_id GROUP BY o.taxonomy_name ORDER BY numero_dianas DESC LIMIT 1;"
            cursor.execute(consulta)
            resultado=cursor.fetchall()
            
            if resultado:
                # Obtener los nombres de las columnas directamente del cursor
                columnas = [desc[0] for desc in cursor.description]

                # Imprimir los resultados en formato tabular con encabezados
                print("El organismo con mayor número de dianas distintas es:")
                print(tabulate(resultado, headers=columnas, tablefmt='grid'))
                Menu.salir_menu(Cinco.cinco_b)
            else:
                print("No hay resultados para la consulta.")
                Menu.salir_menu(Cinco.cinco_b)
        except mysql.connector.Error as err:
            print(f"Error de MySQL: {err}")
            BD.cerrar_conexion()
        except Exception as e:
            print(f"Error: {e}")


