from utils.JournalNetsuiteTools import JournalNetsuiteTools
JournalTools = JournalNetsuiteTools()

def mostrar_menu():
    print("\n📌 Seleccione una opción para procesar:\n")
    print("1. Procesar Seguridad Social")
    print("2. Procesar Prestaciones Sociales")
    print("3. Procesar Nómina")
    print("0. Salir")

def ejecutar_opcion(opcion):
    if opcion == "1":
        print("\n🔄 Procesando Seguridad Social...")
        journal = JournalTools.prestaciones_sociales_journal()
        if journal["success"]:
            print("\n✅ Journal de Seguridad Social creado correctamente en NetSuite.")
            print(f" - Link en NetSuite: {journal['data']}")
            print(f" - Revisa el historial de cargues en la caperta data/historial/")
    
    elif opcion == "2":
        print("\n🔄 Procesando Prestaciones Sociales...")
        journal = JournalTools.seguridad_journal()
        if journal["success"]:
            print("\n✅ Journal de Seguridad Social creado correctamente en NetSuite.")
            print(f" - Link en NetSuite: {journal['data']}")
            print(f" - Revisa el historial de cargues en la caperta data/historial/")
            
    elif opcion == "3":
        print("\n🔄 Procesando Nómina...")
        journal = JournalTools.nomina_journal()
        if journal["success"]:
            print("\n✅ Journal de Seguridad Social creado correctamente en NetSuite.")
            print(f" - Link en NetSuite: {journal['data']}")
            print(f" - Revisa el historial de cargues en la caperta data/historial/")
            
    elif opcion == "0":
        print("\n✅ Saliendo del programa. ¡Hasta pronto!")
        exit(0)  

def main():
    while True:
        mostrar_menu()
        opcion = input("\nIngrese el número de la opción deseada: ").strip()

        if opcion in ["0", "1", "2", "3"]:
            ejecutar_opcion(opcion)
            
            while True:
                continuar = input("\n¿Desea seleccionar otra opción? (S/N): ").strip().lower()
                if continuar == "s":
                    break  # Regresa al menú principal
                elif continuar == "n":
                    print("\n✅ Finalizando el programa. ¡Hasta pronto!")
                    exit(0)
                else:
                    print("\n❌ Opción no válida. Ingrese 'S' para continuar o 'N' para salir.")
        else:
            print("\n❌ Opción no válida. Intente de nuevo ingresando un número del 0 al 3.")

if __name__ == "__main__":
    main()
