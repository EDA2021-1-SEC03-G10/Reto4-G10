"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
import model
import csv
import time
import tracemalloc
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def init():
    """
    Llama la funcion de inicializacion del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer

# Funciones para la carga de datos

def loadConnections(analyzer, landingPointsFile, connectionsFile, countriesFile):
    delta_time = -1.0
    delta_memory = -1.0
    
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    landingPointsList = lt.newList('ARRAY_LIST')
    landingPointsFile = cf.data_dir + landingPointsFile
    lpFile = csv.DictReader(open(landingPointsFile, encoding="utf-8"), delimiter=",")
    for lp in lpFile:
        lt.addLast(landingPointsList, lp)
        # Por cada landing point en el archivo de entrada, se llama a la función en el modelo
        model.addLandingPoint(analyzer, lp)
        model.addCountriesCodes(analyzer, lp)

    countriesList = lt.newList('ARRAY_LIST')
    countriesFile = cf.data_dir + countriesFile    
    cntFile = csv.DictReader(open(countriesFile, encoding="utf-8"), delimiter=",")
    for ctry in cntFile:
        lt.addLast(countriesList, ctry)
        # Por cada país en el archivo de entrada, se llama a la función en el modelo
        model.loadCountry(analyzer, ctry)
    
    connectionsFile = cf.data_dir + connectionsFile
    cnnFile = csv.DictReader(open(connectionsFile, encoding="utf-8-sig"), delimiter=",")
    for cnn in cnnFile:
        # Por cada conexión en el archivo de entrada, se llama a la función en el modelo
        model.addConnection(analyzer, cnn)
        model.addArchConnections(analyzer, cnn)

    # Se crean las conexiónes entre los vertices de cada landing point y entre estos y el vertice de la capital
    model.addPointConnections(analyzer)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return analyzer, lt.firstElement(landingPointsList), lt.firstElement(countriesList), delta_time, delta_memory

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def totalStops(analyzer):
    """
    Cantidad total de puntos de parada
    """
    return model.totalStops(analyzer)

def totalConnections(analyzer):
    """
    Cantidad total de conexiones
    """
    return model.totalConnections(analyzer)

def totalCountries(analyzer):
    """
    Cantidad total de países
    """
    return model.totalCountries(analyzer)

def findClusters(analyzer, landingPoint1, landingPoint2):
    delta_time = -1.0
    delta_memory = -1.0
    
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    landingPoint1 = landingPoint1.replace(' ', '').lower()
    landingPoint2 = landingPoint2.replace(' ', '').lower()

    answer = model.findClusters(analyzer, landingPoint1, landingPoint2)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return analyzer, answer[0], answer[1], delta_time, delta_memory

def findInterLandingPoints(analyzer):
    delta_time = -1.0
    delta_memory = -1.0
    
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    answer = model.findInterLandingPoints(analyzer)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return answer[0], answer[1], delta_time, delta_memory

def findShortestPath(analyzer, pais1, pais2):
    delta_time = -1.0
    delta_memory = -1.0
    
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    answer = model.findShortestPath(analyzer, pais1, pais2)

    path = []

    while st.size(answer[0]) > 0:
        step = st.pop(answer[0])
        path.append({'origin': step['vertexA'], 'destination': step['vertexB'], 'distance' :step['weight']})

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return analyzer, path, answer[1], delta_time, delta_memory

def criticalInfrastructure(analyzer):
    delta_time = -1.0
    delta_memory = -1.0
    
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    answer = model.criticalInfrastructure(analyzer)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return analyzer, answer[0], answer[1], answer[2], delta_time, delta_memory

def failImpact(analyzer, landingPoint):
    delta_time = -1.0
    delta_memory = -1.0
    
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    answer = model.failImpact(analyzer, landingPoint)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return analyzer, answer[0], answer[1], delta_time, delta_memory

# Funciones de cálculo de tiempo y memoria

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)

def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
