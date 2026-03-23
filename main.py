#!/usr/bin/env python

import mysql.connector
from tabulate import tabulate
from mysql.connector import errorcode 

from menu_principal import Menu
from conexion_bd import BD

if __name__ == "__main__":
    db = BD.conectar_a_bd()  # Conectamos con la base de datos 1 vez al comenzar el programa
    
    if db is None:  # Si se da un error, no se puede usar la base de datos.
        print("Error al conectar a la base de datos.")
        exit()

    Menu.menu_principal()