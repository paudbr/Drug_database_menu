#!/usr/bin/env python

#Importamos todos los módulos necesarios
from conexion_bd import BD
from submenus import Submenu

class Menu:

    ########################################################
    ##      *FUNCIÓN DE VOLVER AL MENÚ PRINCIPAL*         ##
    ########################################################

    #Para que fuese un menú más manejable e interactivo y el código más compacto, hemos creado esta función que le pregunta al usuario 
    #si quiere volver al menu principal:
    def salir_menu(funcion_actual):
        salida=input("¿Quieres salir al menú principal? y/n: ")
        if salida.lower() == "y":
            Menu.menu_principal()
        elif salida.lower() == "n":
            funcion_actual() #toma de argumento el nombre de la funcion desde el que hemos llamado a salir_menu() y la vuelve a llamar
        else:
            print("Opción no válida. Vuelve a intentarlo.")
            Menu.salir_menu(funcion_actual)

    ########################################
    ##           MENÚ PRINCIPAL           ##
    ########################################

    #ESTE ES EL MENÚ QUE APARECERÁ EN LA TERMINAL 
    def mostrar_menu():
        print("\n              BIENVENIDO A\n"
            "  ____  _                _     ____  ____ \n"
        " |  _ \(_)___ _ __   ___| |_  | __ )|  _ \ \n"
        " | | | | / __| '_ \ / _ \ __| |  _ \| | | | \n"
        " | |_| | \__ \ | | |  __/ |_  | |_) | |_| | \n"
        " |____/|_|___/_| |_|\___|\__| |____/|____/  \n")
        print("----------------------------------------")
        print("1. Información general de la base de datos:\n")
        print("2. Información de los fármacos:\n")
        print("3. Información de las enfermedades:\n")
        print("4. Información de los efectos fenotípicos:\n")
        print("5. Información de los targets:\n")
        print("6. Borrado de asociación:\n")
        print("7. Inserción de codificaciones en un fármaco:\n")
        print("8. Modificación de score:")
        print("----------------------------------------")
        print("9. Salir\n")

    #FUNCIÓN DE FUNCIONAMIENTO DEL MENÚ 
    def exit_program():
        print("\nSaliendo del programa. ¡Hasta luego!")
        BD.cerrar_conexion()
        exit()

    def menu_principal():
        while True:
            Menu.mostrar_menu()

            opcion = input("Por favor, selecciona una de las siguientes opciones escribiendo su número: ")

            opciones = {
                "1": Submenu.opcion_1,
                "2": Submenu.opcion_2,
                "3": Submenu.opcion_3,
                "4": Submenu.opcion_4,
                "5": Submenu.opcion_5,
                "6": Submenu.opcion_6,
                "7": Submenu.opcion_7,
                "8": Submenu.opcion_8,
                "9": lambda: Menu.exit_program(),
            }

            if opcion in opciones:
                opciones[opcion]()
            else:
                print("Opción no válida. Por favor, elige una opción válida.")


