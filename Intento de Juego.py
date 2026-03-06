
import random

MAX_SALUD = 100
DANO_MINIMO = 10
DANO_MAXIMO = 20

def generar_arsenal():
    return [
        {"nombre": "Espada corta", "dano_min": 12, "dano_max": 20, "tipo": "arma"},
        {"nombre": "Hacha de guerra", "dano_min": 10, "dano_max": 22, "tipo": "arma"},
        {"nombre": "Lanza", "dano_min": 11, "dano_max": 19, "tipo": "arma"},
        {"nombre": "Arco", "dano_min": 10, "dano_max": 18, "tipo": "arma"},
        {"nombre": "Flechas", "cantidad": 5, "tipo": "consumible"},
        {"nombre": "Poción de curación", "curacion": 25, "tipo": "consumible"},
    ]


def abrir_cofre(inventario, arsenal):
    """Devuelve el objeto encontrado respetando duplicados (salvo flechas/pociones)."""
    objetos_poseidos = {item["nombre"] for item in inventario if item.get("tipo") == "arma"}

    opciones = []
    for item in arsenal:
        if item["tipo"] == "arma" and item["nombre"] in objetos_poseidos:
            continue
        opciones.append(item)

    premio = random.choice(opciones)
    return premio.copy()


def dano_jugador(arma):
    dano_min = max(DANO_MINIMO, arma.get("dano_min", DANO_MINIMO))
    dano_max = max(dano_min, arma.get("dano_max", DANO_MAXIMO))
    return random.randint(dano_min, dano_max)


def dano_enemigo(base_min=8, base_max=16, penalizacion=0):
    dano = random.randint(base_min, base_max)
    return max(1, dano - penalizacion)


def usar_pocion(estado):
    if estado["pociones"] <= 0:
        print("No tienes pociones disponibles.")
        return

    if estado["salud"] >= MAX_SALUD:
        print("Ya tienes la salud al máximo.")
        return

    curacion = min(25, MAX_SALUD - estado["salud"])
    estado["salud"] += curacion
    estado["pociones"] -= 1
    print(f"Te curas {curacion} PS. Salud actual: {estado['salud']} PS.")


def seleccionar_arma(inventario):
    armas = [item for item in inventario if item["tipo"] == "arma"]
    if not armas:
        return {"nombre": "Puños", "dano_min": 10, "dano_max": 12, "tipo": "arma"}

    return random.choice(armas)


def turno_enemigo(estado, aturdimiento):
    if aturdimiento["activo"]:
        prob_fallo = random.random()
        if prob_fallo < 0.4:
            print("El enemigo está aturdido y falla su ataque.")
            aturdimiento["turnos_restantes"] -= 1
            if aturdimiento["turnos_restantes"] <= 0:
                aturdimiento["activo"] = False
            return

        dano = dano_enemigo(penalizacion=4)
        aturdimiento["turnos_restantes"] -= 1
        if aturdimiento["turnos_restantes"] <= 0:
            aturdimiento["activo"] = False
    else:
        dano = dano_enemigo()

    estado["salud"] -= dano
    print(f"El enemigo te golpea y te quita {dano} PS. Te quedan {max(0, estado['salud'])} PS.")


def combate(estado, inventario, arsenal):
    enemigo_vida = 80
    aturdimiento = {"activo": False, "turnos_restantes": 0}

    print("\n¡Empieza el combate!")
    while enemigo_vida > 0 and estado["salud"] > 0:
        print("\n--- Tu turno ---")
        print(f"Tu salud: {estado['salud']} PS | Salud del enemigo: {enemigo_vida} PS")
        print("1 -- atacar")
        print("2 -- habilidades (usar poción)")
        print("3 -- defenderse")

        opcion = input("Elige una opción: ").strip()

        if opcion == "2":
            usar_pocion(estado)
            continue

        if opcion == "1":
            arma = seleccionar_arma(inventario)
            dano = dano_jugador(arma)
            enemigo_vida -= dano
            print(f"Atacas con {arma['nombre']} e infliges {dano} de daño.")
            if enemigo_vida <= 0:
                print("¡Has derrotado al enemigo!")
                break
            turno_enemigo(estado, aturdimiento)

        elif opcion == "3":
            print("Te defiendes. Bloqueas este ataque y aturdes al enemigo.")
            aturdimiento["activo"] = True
            aturdimiento["turnos_restantes"] = 2

        else:
            print("Opción no válida. Escribe 1, 2 o 3.")
            continue

    if estado["salud"] <= 0:
        print("\nHas muerto. Fin de la partida.")
        return False

    premio = abrir_cofre(inventario, arsenal)
    if premio["tipo"] == "arma":
        inventario.append(premio)
        print(f"\nHas conseguido otro cofre y contiene: {premio['nombre']}.")
    elif premio["nombre"] == "Flechas":
        estado["flechas"] += premio["cantidad"]
        print(f"\nHas conseguido otro cofre y contiene: {premio['cantidad']} flechas.")
    elif premio["nombre"] == "Poción de curación":
        estado["pociones"] += 1
        print("\nHas conseguido otro cofre y contiene: 1 Poción de curación.")

    print("¡Victoria!")
    return True


def jugar():
    arsenal = generar_arsenal()
    inventario = []
    estado = {"salud": MAX_SALUD, "pociones": 1, "flechas": 0}

    primer_premio = abrir_cofre(inventario, arsenal)
    print("\nHas conseguido un cofre.")
    if primer_premio["tipo"] == "arma":
        inventario.append(primer_premio)
        print(f"En él te ha salido: {primer_premio['nombre']}.")
    elif primer_premio["nombre"] == "Flechas":
        estado["flechas"] += primer_premio["cantidad"]
        print(f"En él te han salido: {primer_premio['cantidad']} flechas.")
    else:
        estado["pociones"] += 1
        print("En él te ha salido: 1 Poción de curación.")

    combate(estado, inventario, arsenal)


def menu_principal():
    while True:
        print("\n=== MENÚ ===")
        print("1 -- Jugar")
        print("2 -- Salir")
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            jugar()
        elif opcion == "2":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Elige 1 o 2.")


if __name__ == "__main__":
    menu_principal()