# Importamos todos los módulos necesarios
import mysql.connector
from mysql.connector import errorcode 

########################################################
##            APERTURA Y CIERRE CONEXIÓN              ##
########################################################  
#Abrimos la conexión con la base de datos al usar la aplicación y la cerramos cuando el usuario decide salir (opción 9)
#Hacemos un try de forma que si hay algún tipo de error aparezca en la terminal 
#y que no deje al usuario utilizar la aplicación hasta que la conexión se establezca correctamente
class BD:
    #cls.db ?
    db = None 

    @classmethod
    def conectar_a_bd(cls):
        try:
            config = {
                'user': 'disnet_user',
                'password': 'disnet_pwd',
                'host': 'localhost',
                'database': 'disnet_drugslayer',
            }
            cls.db = mysql.connector.connect(**config)
            print("Conexión con la base de datos establecida")
            return cls.db

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Algo ha ido mal con la contraseña o el usuario")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("La base de datos no existe")
            else:
                print(err)

    @classmethod
    def cerrar_conexion(cls):
        if 'db' in cls.__dict__ and cls.db.is_connected():
            cls.db.close()
            # Verificar que la conexión se ha cerrado
            if not cls.db.is_connected():
                    print("Conexión con la base de datos cerrada")
                    print("-------------------------------------------------------------")
                    print("BDD - Lucía de Lamadrid Ordoñez y Paula de Blas Rioja - 2023\n")
                    exit()
            else:
                    print("Error al cerrar la conexión")