inventario = []

while True:
    print("\n--- MENÚ ---")
    print("1 -- ver inventario")
    print("2 -- conseguir objeto")
    print("3 -- usar objeto")
    print("4 -- contar objetos")
    print("5 -- salir")

    opcion = input("Elige una opción: ").strip().lower()
    if opcion == "1" or opcion == "ver inventario":
        if inventario:
            print("\nTu inventario contiene:")
            for item in inventario:
                print("-", item)
        else:
            print("\nTu inventario está vacío.")
    elif opcion == "2" or opcion == "conseguir objeto":
        nuevo_objeto = input("¿Qué objeto quieres conseguir? ").strip()
        inventario.append(nuevo_objeto)
        print(f"{nuevo_objeto} ha sido añadido a tu inventario.")
    elif opcion == "3" or opcion == "usar objeto":
        if not inventario:
            print("\nNo tienes objetos para usar.")
        else:
            objeto_a_usar = input("¿Qué objeto quieres usar? ").strip()
            if objeto_a_usar in inventario:
                inventario.remove(objeto_a_usar)
                print(f"Has usado {objeto_a_usar}.")
    elif opcion == "4" or opcion == "contar objetos":
        print(f"\nTienes {len(inventario)} objetos en tu inventario.")
    elif opcion == "5" or opcion == "salir":
        print("¡Hasta luego!")
        break