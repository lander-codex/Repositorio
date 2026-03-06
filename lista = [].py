while True:
    personajes = [
        {"nombre": "Guerrero", "salud": 100},
        {"nombre": "Mago", "salud": 80},
        {"nombre": "Arquero", "salud": 90},
]

    busqueda = input("Busca personaje: ").strip().lower()

    encontrado = False

    if busqueda == "borrar":
        for personaje in personajes:
            if personaje["nombre"].lower() == busqueda:
                personajes.remove(personaje)
                print("Personaje borrado!")
                encontrado = True

    for personaje in personajes:
        if personaje["nombre"].lower() == busqueda:
            print("Personaje encontrado!")
            print("Tiene", personaje["salud"], "de vida")
            encontrado = True

    if not encontrado:
        print("No existe ese personaje")

