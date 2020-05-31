#!/usr/bin/env python3
import sys
from random import randint

def usage():
    print('''
    Uso: 
        python3 rutina.py $cantidadRepartidores $radioEntrega $tiempoFinal [debug]

    Ejemplo: 
        python3 rutina.py 2 5 1000
        python3 rutina.py 4 20 10000 debug
    '''
    )

def generarIntervaloPedido(tiempoActual):
    # Acá iría la FDP de intervaloPedido
    intervaloPedidoRandom = randint(5,20)
    return intervaloPedidoRandom

def generarTiempoEntrega(radioEntrega):
    # Acá iría la FDP de tiempoEntrega
    tiempoEntregaRandom = randint(10,20) * radioEntrega
    return tiempoEntregaRandom

def buscarMenorTiempoComprometido(tiempoComprometidoRepartidores):
    # Busco el repartidor con menor tiempo comprometido
    menorTiempoComprometido = tiempoComprometidoRepartidores.index(min(tiempoComprometidoRepartidores))
    return menorTiempoComprometido

def calcularMaximoTiempoEntrega(listaTiemposEntrega):
    # Calcula el máximo tiempo de atención en el que cae el 90% de los pedidos
    listaTiemposEntrega.sort()
    index = round(len(listaTiemposEntrega) * 0.9) - 1
    return listaTiemposEntrega[index]

def main():
    if len(sys.argv) < 4:
        usage()
        exit(1)

    # Leo argumentos
    cantidadRepartidores = int(sys.argv[1])
    radioEntrega = int(sys.argv[2])
    tiempoFinal = int(sys.argv[3])

    # Chequeo modo debug
    if len(sys.argv) == 5: 
        if sys.argv[4] == "debug": 
            debug = True
            print("\nModo debug habilitado")
    else: 
            debug = False

    print("\n#### Corriendo simulación con cantidad de repartidores = {0} y radio de entrega = {1} km ####".format(cantidadRepartidores, radioEntrega))
    
    # Seteo condiciones iniciales
    tiempoActual = tiempoProximoPedido = 0
    cantidadEntregas = tiempoTotalEspera = 0 
    tiempoComprometidoRepartidores = []
    listaTiemposEntrega = []

    for i in range(cantidadRepartidores):
        tiempoComprometidoRepartidores.append(randint(10,30))
        # tiempoComprometidoRepartidores.append(0)

    ## Inicio simulación ##

    if not debug: print("\nEntregas: ", end = "")
    
    while (tiempoActual < tiempoFinal):

        if not debug: print(".", end = "")

        if debug: print("\nNúmero entrega = {0}".format(cantidadEntregas))
        # Avanzo el tiempo
        tiempoActual = tiempoProximoPedido
        if debug: print("Tiempo actual = {0}".format(tiempoActual))

        # Genero intervalo de próximo de pedido
        intervaloPedido = generarIntervaloPedido(tiempoActual)
        if debug: print("Intervalo pedido = {0}".format(intervaloPedido))
        tiempoProximoPedido = tiempoActual + intervaloPedido
        if debug: print("Tiempo próximo pedido = {0}".format(tiempoProximoPedido))

        # Genero intervalo de tiempo de entrega
        tiempoEntrega = generarTiempoEntrega(radioEntrega)
        if debug: print("Intervalo entrega = {0}".format(tiempoEntrega))

        for i in range(cantidadRepartidores):
            if debug: print("Tiempo comprometido repartidor {0} = {1}".format(i, tiempoComprometidoRepartidores[i]))

        # Busco menor tiempo comprometido
        repartidor = buscarMenorTiempoComprometido(tiempoComprometidoRepartidores)

        
        if tiempoActual > tiempoComprometidoRepartidores[repartidor]:
            # Hay repartidores ociosos -> toman pedido inmediatamente
            tiempoComprometidoRepartidores[repartidor] = tiempoActual + tiempoEntrega
            listaTiemposEntrega.append(tiempoEntrega)
            tiempoTotalEspera = tiempoTotalEspera + tiempoEntrega
            cantidadEntregas += 1

        else:
            # No hay repartidores ociosos -> el pedido se demora
            tiempoComprometidoRepartidores[repartidor] = tiempoComprometidoRepartidores[repartidor] + tiempoEntrega
            tiempoTotalEspera = tiempoTotalEspera + tiempoComprometidoRepartidores[repartidor] - tiempoActual
            listaTiemposEntrega.append((tiempoComprometidoRepartidores[repartidor] - tiempoActual))
            cantidadEntregas += 1

    ## Fin simulación ##

    # Calculo resultados
    tiempoMaximoEspera = calcularMaximoTiempoEntrega(listaTiemposEntrega)
    if debug: print("\nLista de tiempos de entregas: ", listaTiemposEntrega, end = "")
    
    if tiempoMaximoEspera < 35: 
        resultadoExitoso = "SI"
    else:
        resultadoExitoso = "NO"

    # Imprimo resultados
    print("\n\n#### Resultados con cantidad de repartidores = {0} y radio de entrega = {1} km #### \n".format(cantidadRepartidores, radioEntrega))####")
    print("Tiempo máximo de atención en el 90% de pedidos = {0} min".format(tiempoMaximoEspera))
    print("Cantidad de entregas = {0}".format(cantidadEntregas))
    print("Conclusión: {0} se logra tiempo máximo de espera menor a 35 min\n".format(resultadoExitoso))

if __name__ == "__main__":
    try: 
        main()
    except ValueError:
        print ("ERROR!")
