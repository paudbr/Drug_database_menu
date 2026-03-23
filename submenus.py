#Importamos las clases necesarias:
from opcion_1 import Uno
from opcion_2 import Dos
from opcion_3 import Tres
from opcion_4 import Cuatro
from opcion_5 import Cinco
from opcion_6_7_8 import Modif


class Submenu:
    ###################################
    ##           SUBMENÚS            ##
    ###################################

    def opcion_1():
        from menu_principal import Menu
        print("\n--------Has seleccionado la Opción 1--------\n")
        print("\ta. Número total de fármacos, enfermedades, efectos fenotípicos y targets.\n")
        print("\tb. Primeras 10 instancias.\n")
        print("\tc. Volver al menú principal.\n")
        seleccion= input(" Por favor, selecciona una letra: ").lower()
        if seleccion == "a":
            Uno.uno_a()
        elif seleccion == "b":
            Uno.uno_b()
        elif seleccion == "c":
            Menu.menu_principal()
        else:
            print("Ups... opción no válida. Por favor, elige una opción válida:")
            Submenu.opcion_1()

    def opcion_2():
        from menu_principal import Menu
        print("\n--------Has seleccionado la Opción 2--------\n")
        print("\ta. Información de un fármaco.\n")
        print("\tb. Sinónimos de un fármaco.\n")
        print("\tc. Código ATC de un fármaco.\n")
        print("\td. Volver al menú principal.\n")
        seleccion = input(" Por favor, selecciona una letra: ").lower()
        if seleccion == "a":
            Dos.dos_a()       
        elif seleccion == "b":
            Dos.dos_b()
        elif seleccion == "c":
            Dos.dos_c()
        elif seleccion == "d":
            Menu.menu_principal()
        else:
            print("Ups... opción no válida. Por favor, elige una opción válida:")
            Submenu.opcion_2()

    def opcion_3():
        from menu_principal import Menu
        print("\n--------Has seleccionado la Opción 3--------\n")
        print("\ta. Fármacos para una enfermedad. \n")
        print("\tb. Fármaco y enfermedad con el mayor score de asociación. \n")
        print("\tc. Fármaco de mayor score de asociacion para una enfermedad. \n")
        print("\td. Volver al menú principal. \n")
        seleccion= input(" Por favor, selecciona una letra: ").lower()
        if seleccion == "a":
            Tres.tres_a()
        elif seleccion == "b":
            Tres.tres_b()
        elif seleccion == "c":
            Tres.tres_c()
        elif seleccion == "d":
            Menu.menu_principal()
        else:
            print("Ups... opción no válida. Por favor, elige una opción válida:")
            Submenu.opcion_3()

    def opcion_4():
        from menu_principal import Menu
        print("\n--------Has seleccionado la Opción 4--------\n")
        print("\ta. Indicaciones de un fármaco dado.\n")
        print("\tb. Efectos secundarios de un fármaco dado.\n")
        print("\tc. Volver al menú principal.\n")
        seleccion= input(" Por favor, selecciona una letra: ").lower()
        if seleccion == "a":
            Cuatro.cuatro_a()
        elif seleccion == "b":
            Cuatro.cuatro_b()
        elif seleccion == "c":
            Menu.menu_principal()
        else:
            print("Ups... opción no válida. Por favor, elige una opción válida")
            Submenu.opcion_4()

    def opcion_5():
        from menu_principal import Menu
        print("\n--------Has seleccionado la Opción 5--------\n")
        print("\ta. Dianas de un tipo dado.\n")
        print("\tb. Organismo al cual se asocian un mayor número de dianas.\n")
        print("\tc. Volver al menú principal.\n")
        seleccion= input(" Por favor, selecciona una letra: ").lower()
        if seleccion == "a":
            Cinco.cinco_a()
        elif seleccion == "b":
            Cinco.cinco_b()
        elif seleccion == "c":
            Menu.menu_principal()
        else:
            print("Ups... opción no válida. Por favor, elige una opción válida:")
            Submenu.opcion_5()

    def opcion_6():
        print("------Has seleccionado la Opción 6.-------")
        Modif.seis()

    def opcion_7():
        print("------Has seleccionado la Opción 7.-------")
        Modif.siete()

    def opcion_8():
        print("------Has seleccionado la Opción 8.-------")
        Modif.ocho()
