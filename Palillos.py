import numpy as np 
import random 
import time
import sys

# Definicion de variables globales
PUNTOS_JUGADOR = 0
PUNTOS_ORDENADOR = 0

# Configuración Q-Learning
TASA_APRENDIZAJE = 0.1 
FACTOR_DESCUENTO = 0.95 
EPISODIOS_ENTRENAMIENTO = 30000 

class AgenteQLearning:
    def __init__(self, max_palillos):
        # Crea una tabla, Filas = Palillos, Columnas = Acciones 
        self.tabla_q = np.zeros((max_palillos + 1, 4))  #

    def aprender(self, estado, accion, recompensa, proximo_estado):
        # Mira cuál es la mejor recompensa posible en el futuro
        max_q_futuro = np.max(self.tabla_q[proximo_estado]) if proximo_estado > 0 else 0.0
        q_actual = self.tabla_q[estado, accion]
        # Ecuación de Bellman: Actualiza el valor de la celda en la tabla
        self.tabla_q[estado, accion] = q_actual + TASA_APRENDIZAJE * (recompensa + FACTOR_DESCUENTO * max_q_futuro - q_actual)

    def elegir_mejor_accion(self, estado):
        # Filtra movimientos ilegales 
        acciones_validas = [a for a in [1, 2, 3] if estado - a >= 0]
        if not acciones_validas: return 1
        
        mejor_accion = acciones_validas[0]
        mejor_valor = -np.inf
        # Random shuffle para variedad en empates
        random.shuffle(acciones_validas)
        
        for accion in acciones_validas:
            valor = self.tabla_q[estado, accion]
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_accion = accion
                # Busca en la tabla cuál acción tiene el valor más alto y la elige
        return mejor_accion

# Logica de IA

def logica_teoria_juegos(palillos):
    objetivo = (palillos - 1) % 4
    if objetivo == 0:
        return random.choice([1, 1, 2]) # Posición defensiva
    return objetivo

def minimax_recur(palillos, es_maximizando):
    if palillos == 0: return 1 if es_maximizando else -1 
    if es_maximizando: 
        mejor = -np.inf
        for a in [1, 2, 3]:
            if palillos - a >= 0: melhor = max(mejor, minimax_recur(palillos - a, False))
        return mejor
    else: 
        peor = np.inf
        for a in [1, 2, 3]:
            if palillos - a >= 0: peor = min(peor, minimax_recur(palillos - a, True))
        return peor

def obtener_minimax(palillos):
    mejor_jugada = 1
    mejor_valor = -np.inf
    acciones = [a for a in [1, 2, 3] if palillos - a >= 0]
    for accion in acciones:
        val = minimax_recur(palillos - accion, False)
        if val > mejor_valor:
            mejor_valor = val
            mejor_jugada = accion
    return mejor_jugada

def entrenar_agente_ia():
    print("INCIANDO IA")
    agente = AgenteQLearning(50)
    for _ in range(EPISODIOS_ENTRENAMIENTO):
        p = random.randint(10, 30)
        while p > 0:
            acc = random.randint(1, 3)
            if p - acc < 0: acc = p
            estado = p
            p -= acc
            r = -100 if p == 0 else 1
            agente.aprender(estado, acc, r, p)
    return agente

# Interfaz de Usuafio

def presentacion_1():
    print("\n" + "="*60)
    print("JUEGO DE LOS PALILLOS_Seleccion de Dificultad")
    print("="*60)
    print(" 1.-Muy baja   ")
    print(" 2.-Baja")
    print(" 3.-Media   ")
    print(" 4.-Medio-alta")
    print(" 5.-Imposible")
    print("-" * 60)
    while True:
        try:
            op = int(input("Seleccione Nivel (1-5): "))
            if 1 <= op <= 5: return op
        except ValueError: pass

def menu_seleccion_turno():
   #Nuevo menu para seleccionar quien empieza
    print("\n" + "-"*60)
    print("CONFIGURACION DE TURNO INICIAL")
    print("-" * 60)
    print("1. Empiezo Yo")
    print("2. Empieza la Computadora")
    print("3. Aleatorio")
    
    while True:
        try:
            op = int(input("Elija quién inicia la partida (1-3): "))
            if 1 <= op <= 3: return op
            print("Por favor elija un numero valido (1-3).")
        except ValueError:
            print("Entrada invalida.")


#Segunda pantalla con los datos del juego y un enter para comenzar
def presentacion_2(quien_empieza_texto, num_palillos):
    print("\n" + "#"*60)
    print(f"RESUMEN DE PARTIDA")
    print(f"-Palillos en mesa : {num_palillos}")
    print(f"-Turno inicial    : {quien_empieza_texto}")
    print(f"-Marcador Global  : Jugador {PUNTOS_JUGADOR} / {PUNTOS_ORDENADOR} Ordenador")
    print("#"*60)
    input("Presione [ENTER] para comenzar la partida")

def sorteo_opciones():
    return random.randint(20, 25), 3

def area_de_juego(palillos):
    print("\n" + " " * 4 + f"MESA ({palillos}): " + "| " * palillos)
    print("_" * 60)

def movimiento_jugador(palillos):
    while True:
        try:
            q = int(input(f"-- Tu turno,¿Cuantos quitas (1-3)?: "))
            if 1 <= q <= 3 and (palillos - q) >= 0: return q
            print("Movimiento invalido.")
        except ValueError: print("Error: Ingrese numero.")

def movimiento_ordenador_aleatorio(palillos):
    pos = [x for x in [1, 2, 3] if palillos - x >= 0]
    j = random.choice(pos)
    print(f">> Ordenador (Aleatorio) quita {j} palillos.")
    return j

def movimiento_ordenador_con_ia(palillos, nivel, agente):
    jugada = 1
    nom = "IA"
    if nivel == 2:
        nom = "Heurística"
        if palillos <= 3: jugada = palillos 
        else: jugada = random.choice([1, 2, 3])
        if palillos == 2: jugada = 1
        elif palillos == 3: jugada = 2
        elif palillos == 4: jugada = 3
    elif nivel == 3:
        nom = "Teoría"
        jugada = logica_teoria_juegos(palillos)
    elif nivel == 4:
        nom = "Minimax"
        if palillos > 12: jugada = logica_teoria_juegos(palillos)
        else: jugada = obtener_minimax(palillos)
    elif nivel == 5:
        nom = "Nivel 5"
        jugada = agente.elegir_mejor_accion(palillos)
        obj = (palillos - 1) % 4
        if obj != 0 and jugada != obj: jugada = obj

    if palillos - jugada < 0 or jugada < 1: jugada = 1
    print(f">> Ordenador ({nom}) quita {jugada} palillos.")
    return jugada

def mostrar_ganador(ganador):
    print("\n" + "*"*40)
    if ganador == "jugador": print(" ¡FELICIDADES! Has ganado.")
    else: print(" EL ORDENADOR GANA. Has tomado el último.")
    print("*"*40 + "\n")

def main():
    global PUNTOS_JUGADOR, PUNTOS_ORDENADOR
    agente = entrenar_agente_ia()
    
    while True:
        # Selección de Nivel
        nivel = presentacion_1()
        
        #  Sorteo base de palillos
        total_palillos, _ = sorteo_opciones()
        
        # Selección de Turno 
        opcion_turno = menu_seleccion_turno()
        
        # LOGICA DE TURNO Y AJUSTEPARA IA NIVEL ALTO
        turno_humano = True
        txt_inicio = ""

        if opcion_turno == 1: # SI EL USUARIO ELIGE EMPEZAR 
            turno_humano = True
            txt_inicio = "JUGADOR" 
            if nivel >= 3:
                resto = (total_palillos - 1) % 4
                if resto != 0: 
                    total_palillos -= resto 
                    if total_palillos < 15: total_palillos += 4

        elif opcion_turno == 2: # Usuario  elige que empiece CPU
            turno_humano = False
            txt_inicio = "ORDENADOR"
           #SI EL NIVEL ES DIFICIL AJUSTAMOS EL NUMERO DE PALILLOS PARA LA VENTAJA DE LA IA
            if nivel >= 3:
                resto = (total_palillos - 1) % 4
                if resto == 0:
                    total_palillos += 1 

        else: #EL USUARIO ELIGIO TURNO ALEATORIO
            if nivel >= 3:
                resto = (total_palillos - 1) % 4
                if resto == 0: # 21 palillos, Empieza el USAURIO
                    turno_humano = True
                    txt_inicio = "Aleatorio -> JUGADOR"
                else: # 20 palillos,Empieza EL ordenador
                    turno_humano = False
                    txt_inicio = "Aleatorio -> ORDENADOR"
            else:
                if random.random() > 0.5:
                    turno_humano = True
                    txt_inicio = "Aleatorio -> JUGADOR"
                else:
                    turno_humano = False
                    txt_inicio = "Aleatorio -> ORDENADOR"

        # Mostrar Datos y Enter
        presentacion_2(txt_inicio, total_palillos)
        
        # Bucle de Juego
        while total_palillos > 0:
            area_de_juego(total_palillos)
            
            quita = 0
            if turno_humano:
                quita = movimiento_jugador(total_palillos)
            else:
                time.sleep(0.6)
                if nivel == 1: quita = movimiento_ordenador_aleatorio(total_palillos)
                else: quita = movimiento_ordenador_con_ia(total_palillos, nivel, agente)
            
            total_palillos -= quita
            
            if total_palillos == 0:
                if turno_humano:
                    mostrar_ganador("ordenador")
                    PUNTOS_ORDENADOR += 1
                    PUNTOS_JUGADOR -= 1
                else:
                    mostrar_ganador("jugador")
                    PUNTOS_JUGADOR += 1
                    PUNTOS_ORDENADOR -= 1
                break
            turno_humano = not turno_humano

        if input("¿Otra partida? (s/n): ").lower() != 's': break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt: pass