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

from DISClib.DataStructures.adjlist import indegree, vertices
import config as cf
from DISClib.ADT import graph as gr
from DISClib.ADT import map as mp
from DISClib.ADT import list as lt
from DISClib.DataStructures import mapentry as me
from DISClib.DataStructures import linkedlistiterator as lli
from DISClib.Algorithms.Graphs import scc as kos
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
                    'landingPointsNames': None,
                    'connections': None,
                    'countries': None,
                    'countriesCodes': None
                    }

        analyzer['landingPoints'] = mp.newMap(numelements=1280,
                                     maptype='PROBING',
                                     comparefunction=compareLandingPoints)

        analyzer['landingPointNames'] = mp.newMap(numelements=1280,
                                     maptype='PROBING',
                                     comparefunction=compareLandingPointNames)

        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=3300,
                                              comparefunction = compareLandingPoints)

        analyzer['countries'] = mp.newMap(numelements=300,
                                          maptype='PROBING')

        analyzer['countriesCodes'] = mp.newMap()

        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para agregar informacion al catalogo

def addLandingPoint(analyzer, landingPoint):
    # Se obtiene el nombre del landing point, pero se le quitan los espacios y se pasa a minúsculas
    lpName = landingPoint['name'].replace(' ', '').lower()
    entry = mp.get(analyzer['landingPoints'], landingPoint['landing_point_id'])
    if entry is None:
        # Para cada landing point en el archivo, se crea una entrada en el mapa de landing points
        entry = newLandingPointEntry(landingPoint)
        # La entrada se identifica con una llave igual a su columna landing_point_id
        mp.put(analyzer['landingPoints'], landingPoint['landing_point_id'], entry)
    # También se crea una entrada en el mapa que relaciona los nombres de los landin points con sus ids (Req 1)
    mp.put(analyzer['landingPointNames'], lpName, landingPoint['landing_point_id'])

def addCodes(analyzer, info):
    mp.put(analyzer["countriesCodes"], str(info["landing_point_id"]), info)

def newLandingPointEntry(landingPoint):
    # Se obtiene el nombre del país del landing point (-1 es para obtener la última palabra del campo)
    country = landingPoint['name'].split(',')[-1].strip()
    # Cada entrada del mapa tiene los datos del archivo junto con una lista de vertices y el país
    entry = {'landingPointId': landingPoint['landing_point_id'], 
                'id': landingPoint['id'],
                'name': landingPoint['name'],
                'latitude': landingPoint['latitude'],
                'longitude': landingPoint['longitude'],
                'country': country, # Sirve para identificar rápidamente el país del landing point
                'vertices': None} # En este listado se relacionan los vertices que pertenecen al mismo landing point (Mismo landing point, diferente cable)
    
    entry['vertices'] = lt.newList('SINGLE_LINKED', compareVertices)
    return entry

def loadCountry(analyzer, country):
    entry = mp.get(analyzer['countries'], country['CountryName'])
    if entry is None:
        # Para cada país en el archivo, se crea una entrada en el mapa de paises
        entry = newCountryEntry(country)
        # La entrada se identifica con una llave igual a su columna con el nombre del país
        mp.put(analyzer['countries'], country['CountryName'], entry)
    addPoint(analyzer, country['CapitalName'] + "-" + country['CountryName'])

def newCountryEntry(country):
    # Cada entrada del mapa tiene los datos del país junto con una referencia al vertice de la capital
    entry = {'data': country, 
                'vertex': country['CapitalName'] + "-" + country['CountryName']}
    return entry

def addPoint(analyzer, pID):
    try:
        # Se intenta crear un vertice. Primero se verifica si existe
        if gr.containsVertex(analyzer['connections'], pID) == False:
            gr.insertVertex(analyzer['connections'], pID)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addPoint')

def addConnection(analyzer, cnn):
    # Para cada conexión, se crea un vertice con el landing point de origen y el cable correspondiente
    originPoint = cnn["origin"] + '-' + cnn["cable_name"]
    # Se obtiene la entrada del mapa de landing point correspondiente al landing point de origen
    originLP = me.getValue(mp.get(analyzer['landingPoints'], cnn['origin']))
    # Si el vertice que relaciona al landing point con el cable no existe, se crea
    if lt.isPresent(originLP['vertices'], originPoint) == 0:
        lt.addLast(originLP['vertices'], originPoint)
    # Se añade el vertice al grafo
    addPoint(analyzer, originPoint)

    # Se crea un vertice con el landing point de destino y el cable correspondiente
    destinationPoint = cnn["destination"] + '-' + cnn["cable_name"]
    # Se obtiene la entrada del mapa de landing point correspondiente al landing point de destino
    destinationLP = me.getValue(mp.get(analyzer['landingPoints'], cnn['destination']))
    # Si el vertice que relaciona al landing point con el cable no existe, se crea
    if lt.isPresent(destinationLP['vertices'], destinationPoint) == 0:
        lt.addLast(destinationLP['vertices'], destinationPoint)
    # Se añade el vertice al grafo
    addPoint(analyzer, destinationPoint)

    # Se determina la distancia (peso) del arco
    if cnn["cable_length"] != "n.a.":
        length = float(cnn["cable_length"].replace(",", "").split()[0])
    else:
        # Si la distancia no se da en el archivo de entrada, se calcula a partir de las coordenadas de los landing points
        origin = (float(originLP["latitude"]), float(originLP["longitude"]))
        destination = (float(destinationLP["latitude"]), float(destinationLP["longitude"]))
        length = round(hs.haversine(origin, destination), 2)
    # Se añade el arco al grafo
    addEdge(analyzer, originPoint, destinationPoint, length)

def addEdge(analyzer, originPoint, destinationPoint, distance):
    edge = gr.getEdge(analyzer['connections'], originPoint, destinationPoint)
    # Se intenta crear un arco. Primero se verifica si existe
    if edge is None:
        gr.addEdge(analyzer['connections'], originPoint, destinationPoint, distance)
    return analyzer

def addPointConnections(analyzer):
    # Para cada landing point es necesario realizar dos acciones:
    # 1. Crear arcos entre los vertices correspondientes al landing point, con un peso mínimo
    # 2. Crear arcos entre los vertices del landing point y el vertice correspondiente a la capital del país
    for lp in lt.iterator(mp.valueSet(analyzer['landingPoints'])):
        vertices = lp['vertices']
        originIndex = lt.size(vertices)
        
        # Se obtiene el vertice de la capital del país
        country = me.getValue(mp.get(analyzer['countries'], lp['country']))
        countryVertex = country['vertex']

        # Se calcula la distancia del landing point a la capital, mediante coordenadas
        origin = (float(lp["latitude"]), float(lp["longitude"]))
        destination = (float(country['data']["CapitalLatitude"]), float(country['data']["CapitalLongitude"]))
        haversineLength = round(hs.haversine(origin, destination), 2)

        # Para cada vertice del landing point, se crean los arcos correspondientes
        for vertex in lt.iterator(vertices):
            addEdge(analyzer, vertex, countryVertex, haversineLength)
            addEdge(analyzer, countryVertex, vertex, haversineLength)

        # Si el landing point solo tiene un vertice (solo se conecta a un cable) no es necesario crear más arcos
        if originIndex <= 1:
            continue

        # Si el landing point tiene más de un vertice, se crean arcos entre ellos. La distancia se considera mínima
        for i in range(1, lt.size(vertices)):
            originVertex = lt.getElement(vertices, originIndex)
            destinationVertex = lt.getElement(vertices, i)
            addEdge(analyzer, originVertex, destinationVertex, 0.1)
            addEdge(analyzer, destinationVertex, originVertex, 0.1)
            originIndex = i

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

def findClusters(analyzer, landingPoint1, landingPoint2):
    #Se ejecuta el algotimo de Kosaraju
    scc = kos.KosarajuSCC(analyzer['connections'])

    #Se obtienen los ids de los landing points a partir de sus nombres
    vertexAId = me.getValue(mp.get(analyzer['landingPointNames'], landingPoint1))
    vertexBId = me.getValue(mp.get(analyzer['landingPointNames'], landingPoint2))

    # Se obtiene la entrada del mapa para cada uno de los landing points
    lpA = me.getValue(mp.get(analyzer['landingPoints'], vertexAId))
    lpB = me.getValue(mp.get(analyzer['landingPoints'], vertexBId))

    # Se obtiene el primer vertice de cada uno de los landing points
    vertexA = lt.getElement(lpA['vertices'], 1)
    vertexB = lt.getElement(lpB['vertices'], 1)

    # Se retornan los valores devueltos por las funciones de componentes conectados y vertices fuertemente conectados    
    return kos.connectedComponents(scc), kos.stronglyConnected(scc, vertexA, vertexB)

def findInterLandingPoints(analyzer):
    ammount = 0
    iterator = lli.newIterator(gr.vertices(analyzer["connections"]))
    vertexList = lt.newList()

    while lli.hasNext(iterator):
        vertex = lli.next(iterator)
        inDeg = gr.indegree(analyzer["connections"], vertex)
        ouDeg = gr.outdegree(analyzer["connections"], vertex)
        if (inDeg >= 1) and (ouDeg > 1):
            lt.addLast(vertexList, vertex)
            ammount += 1

    final = lt.newList
    newIterator = lli.newIterator(vertexList)

    while lli.hasNext(newIterator):
        elt = lli.next(newIterator)
        cpl = mp.get(analyzer["countriesCodes"], elt)
        value = me.getValue(cpl)
        lt.addLast(final, value["id"])
        lt.addLast(final, value["name"])
    
    return ammount, final
    

def findShortestPath(analyzer, pais1, pais2):
    # Se obtiene el vertice correspondiente al primer país
    country1 = me.getValue(mp.get(analyzer['countries'], pais1))
    vertex1 = country1['vertex']

    # Se obtiene el vertice correspondiente al segundo país
    country2 = me.getValue(mp.get(analyzer['countries'], pais2))
    vertex2 = country2['vertex']

    # Se ejecuta el algoritmo de Dijkstra
    search = djk.Dijkstra(analyzer['connections'], vertex1)

    # Se obtiene la distancia y el camino
    dist = djk.distTo(search, vertex2)
    path = djk.pathTo(search, vertex2)

    return path, dist

def criticalInfrastructure(analyzer):
    return 0, 0, 0

def failImpact(analyzer, landingPoint):
    return 0, []

# Funciones utilizadas para comparar elementos dentro de una lista

# def compareLandingPointsIds(landingPoint, keyvalueLandingPoint):

#     landingPointCode = keyvalueLandingPoint['key']
#     if (landingPoint == landingPointCode):
#         return 0
#     elif (landingPoint > landingPointCode):
#         return 1
#     else:
#         return -1

def compareLandingPoints(landingPoint, keyvalueLandingPoint):

    landingPointCode = keyvalueLandingPoint['key']
    if (landingPoint == landingPointCode):
        return 0
    elif (landingPoint > landingPointCode):
        return 1
    else:
        return -1

# def compareConnections(firstCnn, secondCnn):

#     if firstCnn == secondCnn:
#         return 0
#     elif firstCnn > secondCnn:
#         return 1
#     else:
#         return -1

def compareLandingPointNames(landingPoint1, landingPoint):

    landingPoint2 = landingPoint['key']
    if (landingPoint1 == landingPoint2):
        return 0
    else:
        return 1

def compareVertices(vertex1, vertex2):
    if(vertex1 == vertex2):
        return 0
    else:
        return 1

# Funciones de ordenamiento
