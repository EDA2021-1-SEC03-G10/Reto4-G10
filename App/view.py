"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import threading
import controller
from DISClib.ADT import list as lt
assert cf

initialPoints = None
landingPointsFile = 'landing_points.csv'
connectionsFile = 'connections.csv'
countriesFile = 'countries.csv'

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("\n")
    print("Bienvenido")
    print("1- Inicializar analizador")
    print("2- Cargar información")
    print("3- Encontrar cantidad de clusteres dentro de la red de cables submarinos")
    print("4- Encontrar landing points que sirven como punto de interconexión a más cables")
    print("5- Encontrar la ruta mínima para enviar información entre dos países")
    print("6- Identificar la infraestructura crítica para garantizar el mantenimiento preventivo")
    print("7- Conocer el impacto que tendría el fallo de un determinado landing point")    
    print("0- Salir")

cont = None

"""
Menu principal
"""

def thread_cycle():
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs[0]) == 1:
            print("\nInicializando....")
            cont = controller.init()

        elif int(inputs[0]) == 2:
            print("Cargando información de los archivos ....")
            answer = controller.loadConnections(cont, landingPointsFile, connectionsFile, countriesFile)        
            totalEdges = controller.totalConnections(cont)
            totalVertex = controller.totalStops(cont)
            totalCountries = controller.totalCountries(cont)
            print('\n')
            print('Cantidad total de arcos: ' + str(totalEdges))
            print('Cantidad total de vertices: ' + str(totalVertex))   
            print('Cantidad total de países: ' + str(totalCountries))
            print('El límite de recursión actual: ' + str(sys.getrecursionlimit()))

            firstLandingPoint = answer[1]
            print('')
            print('Primer landing point cargado: ')
            print('Identificador: ' + firstLandingPoint['id'])
            print('Nombre: ' + firstLandingPoint['name'])
            print('Latitud: ' + firstLandingPoint['latitude'])
            print('Longitud: ' + firstLandingPoint['longitude'])

            lastCountry = answer[2]
            print('')
            print('Último país cargado: ')
            print('Nombre: ' + lastCountry['CountryName'])
            print('Población: ' + lastCountry['Population'])
            print('Usuarios de internet: ' + lastCountry['Internet users'])

            print('')
            print("Tiempo [ms]: ", f"{answer[3]:.3f}", "  ||  ",
                "Memoria [kB]: ", f"{answer[4]:.3f}")

        elif int(inputs[0]) == 3:
            landingPoint1 = input("Ingrese el nombre del landing point 1: ")
            landingPoint2 = input("Ingrese el nombre del landing point 2: ")
            answer = controller.findClusters(cont, landingPoint1, landingPoint2)
            clusters = answer[1]
            sameCluster = answer[2]

            print('')
            print("Número total de clústeres: " + str(answer[1]))
            if sameCluster:
                print("¿Están en el mismo cluster?: Si")
            else:
                print("¿Están en el mismo cluster?: No")

            print('')
            print("Tiempo [ms]: ", f"{answer[3]:.3f}", "  ||  ",
                "Memoria [kB]: ", f"{answer[4]:.3f}")

        elif int(inputs[0]) == 4:
            answer = controller.findInterLandingPoints(cont)
            totalCables = answer[0]
            landingPoints = answer[1]

            print('')
            print("Lista de landing points: ")
            print(landingPoints)

            print('')
            print('Total de cables conectados: ' + str(totalCables))

            print('')
            print("Tiempo [ms]: ", f"{answer[2]:.3f}", "  ||  ",
                "Memoria [kB]: ", f"{answer[3]:.3f}")
            
        elif int(inputs[0]) == 5:
            pais1 = input("Ingrese el nombre del país 1: ")
            pais2 = input("Ingrese el nombre del país 2: ")

            answer = controller.findShortestPath(cont, pais1, pais2)
            connections = answer[1]
            distance = answer[2]

            print('')
            print("Ruta: ")

            for conn in connections:
                print('Origen: ' + conn['origin'] + ', Destino: ' + conn['destination'] + ', distancia: ' + str(conn['distance']))

            print('')
            print('Distancia total de la ruta: ' + str(distance))

            print('')
            print("Tiempo [ms]: ", f"{answer[3]:.3f}", "  ||  ",
                "Memoria [kB]: ", f"{answer[4]:.3f}")

        elif int(inputs[0]) == 6:
            answer = controller.criticalInfrastructure(cont)
            numNodes = answer[1]
            totalCost = answer[2]
            longestBranch = answer[3]

            print('')
            print("Número de nodos conectados a la red de expansión mínima: " + str(numNodes))

            print('')
            print('Costo total: ' + str(totalCost))

            print('')
            print('Rama más larga: ' + str(longestBranch))

            print('')
            print("Tiempo [ms]: ", f"{answer[4]:.3f}", "  ||  ",
                "Memoria [kB]: ", f"{answer[5]:.3f}")
            
        elif int(inputs[0]) == 7:
            landingPoint = input("Ingrese el nombre del landing point: ")
            answer = controller.failImpact(cont, landingPoint)
            totalCountries = answer[1]
            countries = answer[2]

            print('')
            print('Número de países afectados: ' + str(totalCountries))

            print('')
            print("Lista de países afectados: ")

            for country in countries:
                print(country)

            print('')
            print("Tiempo [ms]: ", f"{answer[3]:.3f}", "  ||  ",
                "Memoria [kB]: ", f"{answer[4]:.3f}")

        else:
            sys.exit(0)
    sys.exit(0)

if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()
