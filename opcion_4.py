#Importamos los módulos y clases necesarios
import mysql.connector
from mysql.connector import errorcode
from tabulate import tabulate
from conexion_bd import BD

class Cuatro:
    def cuatro_a():
        from menu_principal import Menu
        id_farmaco=input("Introduce el codigo CHEMBL del fármaco del que quieras saber sus indicaciones: ")
        try :
            cursor=BD.db.cursor()
            
            consulta = f"SELECT COUNT(*) FROM drug WHERE drug_id = %s;"
            cursor.execute(consulta, (id_farmaco,))
            resultado=cursor.fetchone()
            
            if resultado [0] > 0:
                print ("Código CHEMBL encontrado")
                consulta_indicaciones=f"SELECT pe.phenotype_id, pe.phenotype_name FROM phenotype_effect AS pe JOIN drug_phenotype_effect AS dpe ON pe.phenotype_id=dpe.phenotype_id JOIN drug AS d ON d.drug_id=dpe.drug_id WHERE d.drug_id= %s AND dpe.phenotype_type='INDICATION';"
                cursor.execute(consulta_indicaciones, (id_farmaco,))
                resultado_indicaciones=cursor.fetchall()
                if resultado_indicaciones:
                    columnas = [desc[0] for desc in cursor.description]

                    # Imprimir los resultados en formato tabular con encabezados
                    print(f"Indicaciones asociadas a un fármaco con el código {id_farmaco}:")
                    print(tabulate(resultado_indicaciones, headers=columnas, tablefmt='grid'))
                    Menu.salir_menu(Cuatro.cuatro_a)
                else:
                    print(f"No hay indicaciones asociadas al código {id_farmaco}.")
                    Menu.salir_menu(Cuatro.cuatro_a)
            else:
                print("No existe este código, vuelve a intentarlo" )
                Menu.salir_menu(Cuatro.cuatro_a)

        except mysql.connector.Error as err:
            print(f"Error de MySQL: {err}")
            BD.cerrar_conexion()
        except Exception as e:
            print(f"Error: {e}")
            
    def cuatro_b():
        from menu_principal import Menu
        id_farmaco=input("Introduce el código CHEMBL del fármaco del que quieras saber su efecto secundario: ")
        try :
            cursor=BD.db.cursor()
            
            consulta = f"SELECT COUNT(*) FROM drug WHERE drug_id = %s;"
            cursor.execute(consulta, (id_farmaco,))
            resultado=cursor.fetchone()
            
            if resultado [0] > 0:
                print ("Código CHEMBL encontrado")
                consulta_secundarios=f"select pe.phenotype_id as identificador_fenotipo, pe.phenotype_name as nombre_fenotipo from phenotype_effect as pe join drug_phenotype_effect as dpe ON pe.phenotype_id=dpe.phenotype_id join drug as d on dpe.drug_id = d.drug_id WHERE d.drug_id=%s and dpe.phenotype_type ='SIDE EFFECT' ORDER BY dpe.score DESC;"
                cursor.execute(consulta_secundarios,(id_farmaco,))
                resultado_secundarios=cursor.fetchall()
                if resultado_secundarios:
                    # Obtener los nombres de las columnas directamente del cursor
                    columnas = [desc[0] for desc in cursor.description]

                    # Imprimir los resultados en formato tabular con encabezados
                    print(f"Efectos secundarios asociados a un fármaco con el código {id_farmaco}, ordenados de mayor a menor asociación:")
                    print(tabulate(resultado_secundarios, headers=columnas, tablefmt='grid'))
                    Menu.salir_menu(Cuatro.cuatro_b)
                else:
                    print(f"No hay efectos secundarios asociados al código {id_farmaco}.")
                    Menu.salir_menu(Cuatro.cuatro_b)
            else:
                print("No existe este código CHEMBL, vuelve a intentarlo" )
                Menu.salir_menu(Cuatro.cuatro_b)

        except mysql.connector.Error as err:
            print(f"Error de MySQL: {err}")
            BD.cerrar_conexion()
        except Exception as e:
            print(f"Error: {e}")