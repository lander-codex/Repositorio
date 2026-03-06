Vidas = 3
import random
Numero_secreto = random.randint(1, 10)
def pedir_numero(minimo: int, maximo: int) -> int:
    """Solicita un número válido dentro del rango indicado."""
    while True:
        entrada = input(f"Adivina el número secreto entre {minimo} y {maximo}: ").strip()
        if not entrada:
            print("⚠️ Debes escribir un número.")
            continue
        if not entrada.lstrip("-").isdigit():
            print("⚠️ Entrada inválida. Escribe solo números enteros.")
            continue

        numero = int(entrada)
        if not (minimo <= numero <= maximo):
            print(f"⚠️ El número debe estar entre {minimo} y {maximo}.")
            continue
        return numero


def jugar_partida(minimo: int = 1, maximo: int = 10, vidas_iniciales: int = 3) -> bool:
    """Ejecuta una partida. Devuelve True si el jugador gana, False si pierde."""
    vidas = vidas_iniciales
    numero_secreto = random.randint(minimo, maximo)

    print("\n🎮 Nueva partida iniciada")
    print(f"Tienes {vidas} vidas. ¡Buena suerte!")

    while vidas > 0:
        numero = pedir_numero(minimo, maximo)

        if numero == numero_secreto:
            print("✅ ¡Felicidades! Has adivinado el número secreto.")
            return True

        vidas -= 1
        if numero < numero_secreto:
            print("📈 Pista: el número secreto es mayor.")
        else:
            print("📉 Pista: el número secreto es menor.")

        if vidas > 0:
            print(f"❌ Incorrecto. Te quedan {vidas} vidas.")

    print(f"💀 Game Over. El número secreto era {numero_secreto}.")
    return False


def preguntar_revancha() -> bool:
    """Pregunta si el usuario quiere jugar de nuevo."""
    while True:
        respuesta = input("¿Quieres volver a jugar? (si/no): ").strip().lower()
        if respuesta in {"si", "sí", "s"}:
            return True
        if respuesta in {"no", "n"}:
            return False
        print("⚠️ Respuesta no válida. Escribe 'si' o 'no'.")


def main() -> None:
    print("=== Juego: Adivina el número ===")

    while True:
        jugar_partida(minimo=1, maximo=10, vidas_iniciales=3)

        if preguntar_revancha():
            print("\n🔁 ¡Vamos con otra ronda!")
            continue

        print("👋 Gracias por jugar. ¡Hasta la próxima!")
        break


if __name__ == "__main__":
    main()
    
