def mostrar_menu():
    print("\n📌 Seleccione una opción para procesar:")
    print("1. Procesar Seguridad Social")
    print("2. Procesar Prestaciones Sociales")
    print("3. Procesar Nómina")
    print("0. Salir")

def ejecutar_opcion(opcion):
    if opcion == "1":
        print("\n🔄 Procesando Seguridad Social...")
        # Llamar a la función correspondiente aquí
    elif opcion == "2":
        print("\n🔄 Procesando Prestaciones Sociales...")
        # Llamar a la función correspondiente aquí
    elif opcion == "3":
        print("\n🔄 Procesando Nómina...")
        # Llamar a la función correspondiente aquí
    elif opcion == "0":
        print("\n✅ Saliendo del programa. ¡Hasta pronto!")
        exit(0)  # Finaliza el programa de forma limpia

def main():
    while True:
        mostrar_menu()
        opcion = input("\nIngrese el número de la opción deseada: ").strip()

        if opcion in ["0", "1", "2", "3"]:
            ejecutar_opcion(opcion)
        else:
            print("\n❌ Opción no válida. Intente de nuevo ingresando un número del 0 al 3.")

if __name__ == "__main__":
    main()