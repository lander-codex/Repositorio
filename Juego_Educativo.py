"""Juego educativo de Física y Química en consola.

Incluye:
- Preguntas de opción múltiple por materias.
- Sistema de vidas y puntuación.
- Ronda relámpago con bonus.
- Resumen final del desempeño.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Pregunta:
    materia: str
    enunciado: str
    opciones: List[str]
    correcta: int  # índice 0-based
    explicacion: str
    dificultad: int = 1


BANCO_PREGUNTAS: List[Pregunta] = [
    Pregunta(
        materia="Física",
        enunciado="¿Cuál es la unidad de fuerza en el Sistema Internacional?",
        opciones=["Joule", "Newton", "Pascal", "Watt"],
        correcta=1,
        explicacion="La fuerza se mide en newtons (N).",
        dificultad=1,
    ),
    Pregunta(
        materia="Física",
        enunciado="Si un objeto se mueve con velocidad constante en línea recta, su aceleración es:",
        opciones=["Positiva", "Negativa", "Cero", "Infinita"],
        correcta=2,
        explicacion="Sin cambio en la velocidad, no hay aceleración.",
        dificultad=1,
    ),
    Pregunta(
        materia="Física",
        enunciado="¿Qué ley relaciona voltaje (V), corriente (I) y resistencia (R)?",
        opciones=["Ley de Boyle", "Ley de Ohm", "Ley de Coulomb", "Ley de Hooke"],
        correcta=1,
        explicacion="Ley de Ohm: V = I · R.",
        dificultad=2,
    ),
    Pregunta(
        materia="Física",
        enunciado="Un cuerpo de 2 kg recibe una fuerza neta de 10 N. ¿Cuál es su aceleración?",
        opciones=["2 m/s²", "5 m/s²", "10 m/s²", "20 m/s²"],
        correcta=1,
        explicacion="Por la 2ª ley de Newton: a = F/m = 10/2 = 5 m/s².",
        dificultad=2,
    ),
    Pregunta(
        materia="Física",
        enunciado="¿Qué tipo de energía almacena un resorte comprimido?",
        opciones=["Térmica", "Cinética", "Potencial elástica", "Nuclear"],
        correcta=2,
        explicacion="La energía potencial elástica se almacena por deformación.",
        dificultad=1,
    ),
    Pregunta(
        materia="Química",
        enunciado="¿Cuál es el símbolo químico del sodio?",
        opciones=["So", "S", "Na", "Sd"],
        correcta=2,
        explicacion="El símbolo del sodio es Na, del latín natrium.",
        dificultad=1,
    ),
    Pregunta(
        materia="Química",
        enunciado="El pH de una disolución ácida es:",
        opciones=["Menor que 7", "Igual a 7", "Mayor que 7", "Siempre 14"],
        correcta=0,
        explicacion="Una disolución ácida tiene pH menor que 7.",
        dificultad=1,
    ),
    Pregunta(
        materia="Química",
        enunciado="¿Cuál de estos enlaces implica compartición de electrones?",
        opciones=["Iónico", "Covalente", "Metálico", "Puente de hidrógeno"],
        correcta=1,
        explicacion="En los enlaces covalentes los átomos comparten electrones.",
        dificultad=2,
    ),
    Pregunta(
        materia="Química",
        enunciado="¿Qué partícula determina principalmente el número atómico de un elemento?",
        opciones=["Neutrones", "Electrones", "Protones", "Iones"],
        correcta=2,
        explicacion="El número atómico es el número de protones del núcleo.",
        dificultad=2,
    ),
    Pregunta(
        materia="Química",
        enunciado="Balancea: H₂ + O₂ → H₂O. ¿Cuál es la opción correcta?",
        opciones=["H₂ + O₂ → H₂O", "2H₂ + O₂ → 2H₂O", "H₂ + 2O₂ → H₂O", "2H₂ + 2O₂ → H₂O"],
        correcta=1,
        explicacion="La ecuación balanceada es 2H₂ + O₂ → 2H₂O.",
        dificultad=3,
    ),
]


def limpiar_pantalla_simbolica() -> None:
    print("\n" + "=" * 60)


def pedir_entero(msg: str, minimo: int, maximo: int) -> int:
    while True:
        entrada = input(msg).strip()
        if not entrada.isdigit():
            print("⚠️ Introduce un número válido.")
            continue

        valor = int(entrada)
        if minimo <= valor <= maximo:
            return valor

        print(f"⚠️ Elige un valor entre {minimo} y {maximo}.")


def configurar_juego() -> Dict[str, int]:
    limpiar_pantalla_simbolica()
    print("🧪⚛️  BIENVENIDO/A A LAB AVENTURA: FÍSICA Y QUÍMICA")
    print("Demuestra tus conocimientos para ganar el juego.\n")

    print("Selecciona dificultad:")
    print("1) Fácil   (5 vidas, +10 puntos por acierto)")
    print("2) Media   (4 vidas, +15 puntos por acierto)")
    print("3) Difícil (3 vidas, +20 puntos por acierto)")

    opcion = pedir_entero("Tu elección (1-3): ", 1, 3)

    if opcion == 1:
        return {"vidas": 5, "puntos_por_acierto": 10}
    if opcion == 2:
        return {"vidas": 4, "puntos_por_acierto": 15}
    return {"vidas": 3, "puntos_por_acierto": 20}


def seleccionar_preguntas(total: int = 8) -> List[Pregunta]:
    preguntas = BANCO_PREGUNTAS[:]
    random.shuffle(preguntas)
    return preguntas[:total]


def jugar_pregunta(pregunta: Pregunta, puntos_base: int) -> int:
    limpiar_pantalla_simbolica()
    print(f"📘 Materia: {pregunta.materia} | Dificultad: {pregunta.dificultad}")
    print(f"\n❓ {pregunta.enunciado}\n")

    for i, opcion in enumerate(pregunta.opciones, start=1):
        print(f"  {i}. {opcion}")

    respuesta = pedir_entero("\nTu respuesta (1-4): ", 1, 4) - 1

    if respuesta == pregunta.correcta:
        puntos = puntos_base * pregunta.dificultad
        print(f"\n✅ ¡Correcto! +{puntos} puntos")
        return puntos

    print(
        "\n❌ Incorrecto. "
        f"La respuesta correcta era: {pregunta.opciones[pregunta.correcta]}"
    )
    print(f"💡 Explicación: {pregunta.explicacion}")
    return 0


def ronda_relampago() -> int:
    limpiar_pantalla_simbolica()
    print("⚡ RONDA RELÁMPAGO ⚡")
    print("Si aciertas esta pregunta final, ganas +25 puntos extra.\n")

    pregunta = random.choice(BANCO_PREGUNTAS)
    print(f"❓ {pregunta.enunciado}")
    for i, opcion in enumerate(pregunta.opciones, start=1):
        print(f"  {i}. {opcion}")

    respuesta = pedir_entero("\nRespuesta (1-4): ", 1, 4) - 1
    if respuesta == pregunta.correcta:
        print("\n🚀 ¡Bonus conseguido! +25 puntos")
        return 25

    print("\n🧯 No hubo bonus esta vez.")
    return 0


def mostrar_resumen(nombre: str, puntos: int, aciertos: int, total: int) -> None:
    limpiar_pantalla_simbolica()
    precision = (aciertos / total) * 100 if total else 0

    print(f"🏁 Fin del juego, {nombre}.")
    print(f"Puntuación final: {puntos}")
    print(f"Aciertos: {aciertos}/{total} ({precision:.1f}%)")

    if puntos >= 120:
        print("\n🏆 ¡Nivel experto! Dominas Física y Química.")
    elif puntos >= 75:
        print("\n🎖️ ¡Muy buen resultado! Sigue así.")
    else:
        print("\n📚 Buen intento. Repasa conceptos y vuelve a jugar.")


def jugar() -> None:
    nombre = input("¿Cómo te llamas? ").strip() or "Estudiante"
    cfg = configurar_juego()

    vidas = cfg["vidas"]
    puntos = 0
    aciertos = 0

    preguntas = seleccionar_preguntas(total=8)

    for numero_ronda, pregunta in enumerate(preguntas, start=1):
        if vidas <= 0:
            break

        print(f"\n🔬 Ronda {numero_ronda} | Vidas: {vidas} | Puntos: {puntos}")
        ganados = jugar_pregunta(pregunta, cfg["puntos_por_acierto"])

        if ganados > 0:
            puntos += ganados
            aciertos += 1
        else:
            vidas -= 1
            print(f"💔 Pierdes una vida. Te quedan {vidas}.")

        input("\nPulsa Enter para continuar...")

    if vidas > 0:
        puntos += ronda_relampago()

    mostrar_resumen(nombre, puntos, aciertos, len(preguntas))


if __name__ == "__main__":
    jugar()
