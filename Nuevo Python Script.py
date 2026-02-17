Vidas = 3
import random
Numero_secreto = random.randint(1, 10)
while True:
    Numero = int(input("Adivina el número secreto entre 1 y 10: "))
    if Numero == Numero_secreto:
        print("¡Felicidades! Has adivinado el número secreto.")
        break
    else:
        Vidas -= 1
        if Numero < Numero_secreto:
            print("El número secreto es mayor.")
        else:
            print("El número secreto es menor.")
        print(f"¡Incorrecto! Te quedan {Vidas} vidas.")
        if Vidas == 0:
            print(f"Game Over. El número secreto era {Numero_secreto}.")
            break
