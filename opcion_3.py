#Importamos los módulos y clases necesarios
import mysql.connector
from mysql.connector import errorcode
from tabulate import tabulate
from conexion_bd import BD

class Tres:
    def tres_a():
        from menu_principal import Menu
        nombre_enfermedad= input("Escribe el nombre de la enfermedad de la que quieras saber los fármacos asociados: ")
        try:
            cursor=BD.db.cursor()
            
            consulta=f"SELECT count(*) FROM disease_code WHERE name= %s"
            cursor.execute(consulta,(nombre_enfermedad,))
            comprobar=cursor.fetchone()
            
            if comprobar[0] > 0:
                print("El nombre de la enfermedad existe")
                consulta_farmaco= f"SELECT d.drug_id as id_farmaco, d.drug_name as nombre_farmaco from disease_code join drug_disease as dd on disease_code.code_id = dd.code_id join drug as d on dd.drug_id = d.drug_id where disease_code.name= %s";
                cursor.execute(consulta_farmaco,(nombre_enfermedad,))
                resultado_farmaco=cursor.fetchall()
                
                if resultado_farmaco:
                    # Obtener los nombres de las columnas directamente del cursor
                    columnas = [desc[0] for desc in cursor.description]

                    # Imprimir los resultados en formato tabular con encabezados
                    print(f"Fármacos asociados a la enfermedad {nombre_enfermedad}:")
                    print(tabulate(resultado_farmaco, headers=columnas, tablefmt='grid'))
                    Menu.salir_menu(Tres.tres_a)
                else:
                    print(f"No hay códigos de fármacos asociados para la enfermedad {nombre_enfermedad}.")
            else:
                print("No existe este nombre, vuelve a intentarlo" )
                Menu.salir_menu(Tres.tres_a)
        except mysql.connector.Error as err:
            print(f"Error de MySQL: {err}")
            BD.cerrar_conexion()
        except Exception as e:
            print(f"Error: {e}")

    def tres_b():
        from menu_principal import Menu
        try:
            cursor=BD.db.cursor()
            
            consulta= "SELECT disease_code.name as nombre_enfermedad, d.drug_name as nombre_farmaco, dd.inferred_score as score_asociacion FROM disease_code JOIN drug_disease as dd on disease_code.code_id = dd.code_id JOIN drug as d on dd.drug_id = d.drug_id ORDER BY dd.inferred_score DESC LIMIT 1";
            cursor.execute(consulta)
            resultado=cursor.fetchall()

            columnas = [desc[0] for desc in cursor.description]

            # Imprimir los resultados en formato tabular con encabezados
            print("El fármaco y la enfermedad con el mayor score de asociación son:")
            print(tabulate(resultado, headers=columnas, tablefmt='grid'))
            Menu.salir_menu(Tres.tres_b)
        except mysql.connector.Error as err:
            print(f"Error de MySQL: {err}")
            BD.cerrar_conexion()
        except Exception as e:
            print(f"Error: {e}")

    def tres_c():
        from menu_principal import Menu
        nombre_enfermedad= input("Escribe el nombre de la enfermedad de la que quieras saber el fármaco de mayor asociación ")
        try:
            cursor=BD.db.cursor()
            
            consulta=f"SELECT count(*) FROM disease_code WHERE name= %s"
            cursor.execute(consulta,(nombre_enfermedad,))
            comprobar=cursor.fetchone()
            
            if comprobar[0] > 0:
                print("El nombre de la enfermedad existe")
                consulta_farmaco= f"SELECT d.drug_id as id_farmaco, d.drug_name as nombre_farmaco, dd.inferred_score as score_asociacion FROM disease_code  JOIN drug_disease as dd on disease_code.code_id = dd.code_id JOIN drug as d on dd.drug_id = d.drug_id WHERE disease_code.name= %s ORDER BY dd.inferred_score DESC LIMIT 1;"

                cursor.execute(consulta_farmaco,(nombre_enfermedad,))
                resultado_farmaco=cursor.fetchall()
                
                if resultado_farmaco:
                    columnas = [desc[0] for desc in cursor.description]

                # Imprimir los resultados en formato tabular con encabezados
                    print(f"Fármaco de mayor asociación con la enfermedad {nombre_enfermedad}:")
                    print(tabulate(resultado_farmaco, headers=columnas, tablefmt='grid'))
                    Menu.salir_menu(Tres.tres_c)

                else:
                    print(f"No hay códigos fármacos asociados para la enfermedad {nombre_enfermedad}.")
                    Menu.salir_menu(Tres.tres_c)
            else:
                print("No existe este nombre, vuelve a intentarlo" )
        except mysql.connector.Error as err:
            print(f"Error de MySQL: {err}")
            BD.cerrar_conexion()
        except Exception as e:
            print(f"Error: {e}")