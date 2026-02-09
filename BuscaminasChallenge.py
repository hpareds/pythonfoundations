import random
import os
import time

#Variables global del tablero
tablero = []

#metodo main
def main():
    print("-------BUSCAMINAS-------\n created by Héctor Paredes\n all rights reserved\n")
    
    while True:
        iniciar_partida() #Inicia la partida y ejecuta todas las funciones de este programa
            
        # preguntar si reiniciar o salir
        while True:
            respuesta = input("\n¿Desea jugar otra partida? (s/n): ").strip().lower()
                
            if respuesta == 's':
                break #romper bucle y reiniciar 
            elif respuesta == 'n':
                print("\nGracias por jugar. ¡Hasta la próxima!")
                return # terminar programa
            else:
                print("Opción no válida. Por favor ingrese 's' para sí o 'n' para no.")
    
               
# ----- definicion de metodos -----

def iniciar_partida():
    """
    Ajustamos todo para reiniciar una partida,
    en caso que haya terminado recien una
    """
    
    global tablero
    tablero = [] #reset de tablero
    
    menu() #muestra el menu para seleccionar modo de juego ejecutar otras funciones del programa
    return

def menu():
    """
    Opciones de inicio
    """
    print("Seleccione el modo de juego (1 o 2)\n")

    while True:
        modo = input("1. Normal: Tablero: 9x9, bombas: 10\n2. Avanzado: Tablero: 16x16, bombas: 25\nOpción: ").strip()
        # inicia partida e imprime tablero con los parámetros, como asi ejecuta la partida

        if modo == "1": #9x9, 10 minas
            #parametros modo normal
            filas_cols = 9 
            num_minas = 10
                
            print("Iniciando nueva partida...")
            
            generar_tablero(filas_cols, num_minas)
            
            '''Imprimir minas donde realmente estan (motivos de test) 
            print("\n[DEBUG] Mapa de minas (TRAMPA):")
            
            # 1. Imprimir encabezado de números
            print("   ", end="")
            for i in range(filas_cols):
                print(f"{i+1:2}", end=" ")
            print()

            # 2. Imprimir filas con letras
            for i in range(filas_cols):
                letra_fila = chr(65 + i) # A, B, C...
                print(f"{letra_fila}  ", end="")
                
                for celda in tablero['minas'][i]:
                    # Si es espacio vacío, mostramos punto para que se vea mejor
                    visual = '.' if celda == ' ' else '*'
                    print(f"{visual} ", end=" ")
                print()
            print("-" * (filas_cols * 3 + 4) + "\n")
            '''
            
            imprimir_tablero()
            partida()
            break
            
        elif modo == "2": #16x16, 25 minas
            #parametros modo dificil
            filas_cols = 16
            num_minas = 25
                
            print("Iniciando nueva partida...")
            generar_tablero(filas_cols, num_minas)
            imprimir_tablero()
            partida()
            break
            
        else:
            print("\nOpción no válida, por favor seleccione 1 (normal) o 2 (dificil).")
    return



def generar_tablero(filas_cols, num_minas):
    """
    Crea el tablero con las filas y columnas numeradas
    inicialmente pone todas las casillas con un punto
    """
    global tablero
    # Crear matriz visual para el usuario (puntos)
    tablero_visual = [['.' for _ in range(filas_cols)]for _ in range(filas_cols)]
    # Generar matriz de minas
    tablero_minas = generar_minas(filas_cols, num_minas)
    
    # Guardar ambas matrices 
    tablero = {
        'visual': tablero_visual,
        'minas': tablero_minas,
        'tamaño': filas_cols
    } 
    return

def generar_minas(filas_cols, num_minas): 
    """
    Función para generar el tablero con las minas
    """
    global minas
    # Crear una lista con la cantidad de minas y espacios vacíos
    minas = ['*'] * num_minas + [' '] * (filas_cols **2 - num_minas)
    #crear minas aleatoriamente
    random.shuffle(minas)
    return [minas[i:i+filas_cols] for i in range(0, len(minas), filas_cols)]

def imprimir_tablero():
    """
    Imprime el tablero, 
    lo convierte de matriz a algo entendible para el usuario
    """
    global tablero
    if not tablero:
        return
    
    tamaño = tablero['tamaño']
    visual = tablero['visual']
    
    # Imprimir encabezado de columnas
    print("\n    ", end="")
    for i in range(tamaño):
        print(f"{i+1:2}", end=" ")
    print()
    
    # Imprimir filas con numeración
    for i in range(tamaño):
        letra_fila = chr(65 + i) #en ascii A=65, B=66 ...
        print(f"{letra_fila}   ", end="")
        
        for col in range(tamaño):
            print(f"{visual[i][col]} ", end=" ")
        print()
    
    return

def partida():
    """
    Mantiene el juego hasta que pierda o gane
    """
    global tablero
    jugando = True
    primer_movimiento = True
    tamaño = tablero['tamaño']
    
    inicio = time.time() #cronometro 
    
    os.system('cls' if os.name == 'nt' else 'clear') #limpiar consola 
    imprimir_tablero()

    while jugando:
        f, c = pedir_coordenada()   
        continuar = buscar_coordenada(f, c, primer_movimiento)
        primer_movimiento = False # si el primer movimiento es una mina este es desplazada
        
        if continuar:
            os.system('cls' if os.name == 'nt' else 'clear') #limpiar consola para mostrar el tablero actualizado 
            imprimir_tablero()

        # validar si perdio
        if not continuar:
            fin = time.time()
            tiempo_total = int(fin - inicio) #tiempo total en segundos
            print(f"\nDuraste {tiempo_total} segundos antes de explotar.")            
            jugando = False # Termina el juego

        # validar si gano
        else:
            victoria = True
            for i in range(tamaño):
                for j in range(tamaño):
                    if tablero['minas'][i][j] != '*' and tablero['visual'][i][j] == '.': #validar si hay casillas sin minas
                        victoria = False
                        break
                if not victoria: #si no exploto una mina o no gano sigue el juego dentro del bucle
                    break    

            if victoria: #victoria
                # Calculamos tiempo también al ganar
                fin = time.time()
                tiempo_total = int(fin - inicio)
                minutos = tiempo_total // 60
                segundos = tiempo_total % 60
                
                # Mostramos tablero final limpio
                imprimir_tablero()                

                print(f"\nTiempo: {minutos} min {segundos} s")
                
                jugando = False 
    return

def pedir_coordenada():
    """
    Pide una coordenada al usuario
    """
    global tablero
    tamaño = tablero['tamaño']
    
    while True:
        coordenada = input("\nIngrese una coordenada (Ejemplo A5): ").strip().upper() #convertir a mayusculas
        #valida formato
        if len(coordenada) < 2 or len(coordenada) > 3: #validar formato
            print("Formato inválido. Intente de nuevo.")
            continue
        
        #validar coordenada
        try:
            #separar letra y numero
            fila_letra = coordenada[0]
            col_num = int(coordenada[1:])
            #convertir indices
            f=ord(fila_letra) - ord('A') 
            c = col_num - 1
            #validar coordenada
            if 0 <= f < tamaño and 0 <= c < tamaño:
                #validar si ya fue revelada por medio del metodo
                resultado = esta_revelada(f, c)
                if resultado:
                    return resultado
            else:
                print("Coordenada fuera de rango. Intente de nuevo.")
                
        except ValueError:
            print("Formato inválido. Intente de nuevo.")   
                       
def esta_revelada(f, c):
    """
    Verifica si la coordenada ya ha sido revelada
    """
    #verificar si la casilla ya fue revelada, si es asi, pedir otra coordenada
    if tablero['visual'][f][c] != '.':
        print("Esa casilla ya está descubierta.")
        return False
    else:
        return f, c 

def buscar_coordenada(f,c, primer_movimiento = False):
    """
    Valida que la coordenada exista
    """
    
    if primer_movimiento and es_mina(f,c):
        desplazar_mina(f,c)
    
    #si es mina, mostrar minas y perder 
    if es_mina(f,c):
        mostrar_minas()
        print("\nLo siento, perdiste")
    else:
        revelar_coordenada(f,c)
        return True #continua jugando
    return

def es_mina(f,c):
    """
    Verifica si una coordenada corresponde a una mina
    """ 
    return tablero['minas'][f][c] == '*'

def revelar_coordenada(f,c):
    """
    Verifica si es una mina,
    si lo es, muestra todas las minas
    sino muestra el contenido de la coordenada
    """
    #si la casilla ya fue revelada, no hace nada
    if tablero['visual'][f][c] != '.':
        return
    #cuenta las minas cercanas 
    minas_cerca = contar_minas(f,c)
    mostrar_contenido(f,c, minas_cerca)
    
    if minas_cerca == 0:
        mostrar_contenido(f,c, ' ') 
        for nf, nc in vecinos(f,c):
            revelar_coordenada(nf, nc)
    return


def vecinos(f, c):
    """
    Recopila todos los vecinos de una casilla,
    verificando que no invente vecinos,
    osea que no vaya a crear casillas fuera del tablero
    (si la casilla esta en la orilla por ejemplo)
    """
    filas_totales = tablero['tamaño']
    col_totales = tablero['tamaño']
    lista_vecinos = []

    #recorre matriz alrededor de la casilla seleccionada 3x3
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            #calcula las coordenadas del vecino
            nf = f + i #filas
            nc = c + j #columnas
            #validar que este dentro del tablero
            if 0 <= nf < filas_totales and 0 <= nc < col_totales:
                lista_vecinos.append((nf, nc))
    
    return lista_vecinos

def contar_minas(f,c):
    """
    Cuenta el numero de minas alrededor de una casilla
    """
    minas = 0
    #recorre los vecinos de la casilla y cuenta cuantas minas hay
    for nf, nc in vecinos(f,c):
        if es_mina(nf, nc):
            minas += 1
    
    return minas

def desplazar_mina(f,c):
    """
    Si es el primer movimiento
    mueve la mina a otra casilla
    """
    #mueve la casilla a otro lado
    tablero['minas'][f][c] = ' '
    
    tamaño = tablero['tamaño']
    colocado = False
    
    for i in range (tamaño): #recorre la matriz buscando un lugar
        if colocado: break
        for j in range(tamaño):
            #si encuentra un lugar sin mina, coloca la mina ahi
            if tablero['minas'][i][j] != '*' and (i != f or j != c): 
                tablero['minas'][i][j] = '*'
                colocado = True
                break
            
    return


def mostrar_contenido(f,c, valor):
    """
    Muestra el contenido de la casilla,
    si tiene minas cercanas solo el valor de cuantas minas hay,
    sino crea una reaccion en cadena.

    (Para el segundo caso)
    Podemos simular una pila para esta reaccion en cadena
    e ir añadiendo los vecinos hasta que no hayan más
    valores libres en el perímetro
    """
    #mostrar el valor en la casilla
    tablero['visual'][f][c] = str(valor)
    
    return

def mostrar_minas():
    """
    Muestra todas las minas de un tablero
    en caso de perder o terminar la partida
    """
    #mostrar todas las minas
    tamaño = tablero['tamaño']
    for f in range(tamaño): #recorre filas y columnas para mostrar las minas
        for c in range(tamaño):
            if es_mina(f, c):
                tablero['visual'][f][c] = '*'
    return

if __name__ == "__main__": main()
