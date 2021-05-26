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
    print("0- Salir")

cont = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("\nInicializando....")
        cont = controller.init()

    elif int(inputs[0]) == 2:
        print("Cargando información de los archivos ....")
        controller.loadServices(cont, landingPointsFile, connectionsFile, countriesFile)        
        totalEdges = controller.totalConnections(cont)
        totalVertex = controller.totalStops(cont)
        totalCountries = controller.totalCountries(cont)
        print('\n')
        print('Cantidad total de arcos: ' + str(totalEdges))
        print('Cantidad total de vertices: ' + str(totalVertex))   
        print('Cantidad total de países: ' + str(totalCountries))
        print('El límite de recursión actual: ' + str(sys.getrecursionlimit()))

    else:
        sys.exit(0)
sys.exit(0)
