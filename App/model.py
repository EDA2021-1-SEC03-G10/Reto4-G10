﻿"""
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


# import config as cf
# from DISClib.ADT import list as lt
# from DISClib.ADT import map as mp
# from DISClib.DataStructures import mapentry as me
# from DISClib.Algorithms.Sorting import shellsort as sa
# assert cf

import config as cf
from DISClib.ADT import graph as gr
from DISClib.ADT import map as mp
from DISClib.ADT import list as lt
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert cf
# Se instala Haversine a través del comando "pip install haversine" para calcular distancias en un globo
import haversine as hs

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newAnalyzer():
    """ Inicializa el analizador
    """
    try:
        analyzer = {
                    'landingPoints': None,
                    'connections': None,
                    'countries': None
                    }

        analyzer['landingPoints'] = mp.newMap(numelements=1280,
                                     maptype='PROBING',
                                     comparefunction=compareLandingPointsIds)

        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=3300)
                                              # comparefunction=compareConnections)

        analyzer['countries'] = mp.newMap(numelements=300,
                                          maptype='PROBING')

        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

def prepareData(analyzer, point):
    coords = (float(point["latitude"]), float(point["longitude"]))
    mp.put(analyzer['landingPoints'], point['landing_point_id'], coords)

# def loadData(analyzer, connection):
#     entry = mp.get(analyzer['landingPoints'], connection['origin'])
#     cList = entry['value']
#     cName = connection['cable_name']
#     if not lt.isPresent(cList, cName):
#         lt.addLast(cList, cName)
#     pName = formatVertex[connection]
#     entry = mp.get(analyzer['info'], pName)
#     if entry is None:
#         connectionsList = lt.newList()
#         mp.put(analyzer['info'], pName, connectionsList)
#     else:
#         connectionsList = me.getValue(entry)
#     lt.addLast(connectionsList, connection)

def loadCountry(analyzer, country):
    mp.put(analyzer['countries'], country['CountryName'], country)

# def addLandingPoints(analyzer):
#     pList = mp.keySet(analyzer['landing_points'])
#     for key in lt.iterator(pList):
#         cList = mp.get(analyzer['landing_points'], key)['value']
#         for cName in lt.iterator(cList):
#             LPname = key + "-" + cName
#             addPoint(analyzer, LPname)

def addPointConnections(analyzer, actualPointList):
    for fP in lt.iterator(actualPointList):
        for sP in lt.iterator(actualPointList):
            if fP != sP:
                addConnection(analyzer, fP, sP, 0.1)

# def addPointConnections(analyzer):
#     pList = mp.keySet(analyzer['landing_points'])
#     for key in lt.iterator(pList):
#         cList = mp.get(analyzer['landing_points'], key)['value']
#         prevPoint = None
#         for cable in lt.iterator(cList):
#             origin = key + "-" + cable
#             info = mp.get(analyzer['info'], origin)["value"]
#             for connection in lt.iterator(info):
#                 destination = connection['destination'] + "-" + cable
#                 addConnection(analyzer, origin, destination, info)
#                 addConnection(analyzer, destination, origin, info)

def addPoint(analyzer, pID):
    try:
        if gr.containsVertex(analyzer['connections'], pID) == False:
            gr.insertVertex(analyzer['connections'], pID)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addPoint')

def addConnection(analyzer, originPoint, destinationPoint, distance):
    edge = gr.getEdge(analyzer['connections'], originPoint, destinationPoint)
    if edge is None:
        gr.addEdge(analyzer['connections'], originPoint, destinationPoint, distance)
    return analyzer

# Funciones para agregar informacion al catalogo

def addLandingPoint(analyzer, lp, cnn, actualPointList, capitalData):

    if actualPointList is None:
        actualPointList = lt.newList("ARRAY_LIST")
    originPoint = cnn["origin"] + '-' + cnn["cable_name"]
    addPoint(analyzer, originPoint)
    destinationPoint = cnn["destination"] + '-' + cnn["cable_name"]
    addPoint(analyzer, destinationPoint)

    if cnn["cable_length"] != "n.a.":
        length = float(cnn["cable_length"].replace(",", "").split()[0])
    else:
        origin = (float(lp["latitude"]), float(lp["longitude"]))
        destination = mp.get(analyzer["landingPoints"], cnn["destination"])["value"]
        length = round(hs.haversine(origin, destination), 2)
    addConnection(analyzer, originPoint, destinationPoint, length)
    fP = (float(lp["latitude"]), float(lp["longitude"]))
    laP = (float(capitalData["CapitalLatitude"]), float(capitalData["CapitalLongitude"]))
    capital = capitalData["CapitalName"] + "-" + capitalData["CountryName"]
    haversineLength = round(hs.haversine(fP, laP), 2)
    addConnection(analyzer, originPoint, capital, haversineLength)
    lt.addLast(actualPointList, originPoint)
    # try:
    #     if not gr.containsVertex(analyzer['connections'], lp):
    #         gr.insertVertex(analyzer['connections'], lp)
    #     return analyzer
    # except Exception as exp:
    #     error.reraise(exp, 'model:addLandingPoint')
    return actualPointList

# Funciones para creacion de datos

# Funciones de consulta

def totalStops(analyzer):
    """
    Retorna la cantidad total de vertices del grafo
    """
    return gr.numVertices(analyzer['connections'])

def totalConnections(analyzer):
    """
    Retorna la cantidad total de arcos del grafo
    """
    return gr.numEdges(analyzer['connections'])

def totalCountries(analyzer):
    """
    Retorna la cantidad total de países
    """
    return mp.size(analyzer['countries'])

def formatVertex(landingPoint):
    vertexId = landingPoint['landing_point_id']
    return vertexId

# Funciones utilizadas para comparar elementos dentro de una lista

def compareLandingPointsIds(landingPoint, keyvalueLandingPoint):

    landingPointCode = keyvalueLandingPoint['key']
    if (landingPoint == landingPointCode):
        return 0
    elif (landingPoint > landingPointCode):
        return 1
    else:
        return -1

def compareConnections(firstCnn, secondCnn):

    if firstCnn == secondCnn:
        return 0
    elif firstCnn > secondCnn:
        return 1
    else:
        return -1

# Funciones de ordenamiento
