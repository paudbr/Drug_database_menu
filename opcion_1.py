#Importamos los módulos y clases necesarios
import mysql.connector
from mysql.connector import errorcode
from tabulate import tabulate
from conexion_bd import BD

class Uno:
    def uno_a():
        from menu_principal import Menu
        try: #para tratar posibles excepciones
            cursor = BD.db.cursor()

            # Consulta para obtener información general en una sola llamada
            consulta_general = """
                SELECT
                    (SELECT COUNT(*) FROM drug) AS NumDrugs,
                    (SELECT COUNT(DISTINCT disease_id) FROM disease) AS NumDiseases,
                    (SELECT COUNT(*) FROM phenotype_effect) AS NumPhenoEff,
                    (SELECT COUNT(DISTINCT target_id) FROM target) AS NumTargets;
            """
            cursor.execute(consulta_general)
            num_farmacos, num_enfermedades, num_efectos_fenotipicos, num_targets = cursor.fetchone()
            #utilizamos fetchone porque la consulta solo devuelve un elemento
            print(f"\nNumDrugs: {num_farmacos}")
            print(f"\nNumDiseases: {num_enfermedades}")
            print(f"\nNumPhenoEff: {num_efectos_fenotipicos}")
            print(f"\nNumTargets: {num_targets}\n")

            Menu.salir_menu(Uno.uno_a) #le damos al usuario la opción de volver al menú principal

        except mysql.connector.Error as err:
            print(f"Error de MySQL: {err}")
            BD.cerrar_conexion()
        except Exception as e:
            print(f"Error: {e}")

    def uno_b():
        from menu_principal import Menu
        try:
            cursor = BD.db.cursor()
            consultas = [
                "SELECT drug_id AS identificador, drug_name AS nombre, molecular_type AS tipo_molecular, chemical_structure AS estructura_quimica, inchi_key FROM drug WHERE COALESCE(drug_id, drug_name, molecular_type, chemical_structure, inchi_key) IS NOT NULL LIMIT 10",
                "SELECT disease_id AS identificador, disease_name AS nombre FROM disease WHERE COALESCE(disease_id, disease_name) IS NOT NULL LIMIT 10",
                "SELECT phenotype_id AS identificador, phenotype_name AS nombre FROM phenotype_effect WHERE COALESCE(phenotype_id, phenotype_name) IS NOT NULL LIMIT 10",
                "SELECT t.target_id AS identificador, t.target_name_pref AS nombre, t.target_type AS tipo, o.taxonomy_name AS nombre_organismo FROM target as t INNER JOIN organism as o ON t.organism_id = o.taxonomy_id WHERE COALESCE(t.target_id, t.target_name_pref, o.taxonomy_name) IS NOT NULL LIMIT 10"
            ]
            nombre_consultas = ["los fármacos", "las enfermedades", "los fenotipos", "las dianas"]

            for i, consulta in enumerate(consultas):
                cursor.execute(consulta)
                resultado = cursor.fetchall()

                # Obtener los nombres de las columnas directamente del cursor
                columnas = [desc[0] for desc in cursor.description]

                # Imprimir los resultados en formato tabular con encabezados
                print(f"\nResultados de {nombre_consultas[i]}:")
                print(tabulate(resultado, headers=columnas, tablefmt='pipe'))

            Menu.salir_menu(Uno.uno_b) #preguntamos al usuario si quiere salir al menú
                
        except mysql.connector.Error as err:
            print(f"Error de MySQL: {err}")
            BD.cerrar_conexion()
        except Exception as e:
            print(f"Error: {e}")