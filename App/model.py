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

import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert config

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

        # analyzer['landingPoints'] = m.newMap(numelements=1280,
        #                              maptype='PROBING',
        #                              comparefunction=compareLandingPointsIds)

        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=3300,
                                              comparefunction=compareConnections)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para agregar informacion al catalogo

def addLandingPoint(analyzer, lp):
    try:
        if not gr.containsVertex(analyzer['connections'], lp):
            gr.insertVertex(analyzer['connections'], lp)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addLandingPoint')

def addConnection(analyzer, connection):

    origin = gr.vertices(analyzer["connections"])[connection["origin"]]
    destination = gr.vertices(analyzer["connections"])[connection["destination"]]

    edge = gr.getEdge(analyzer['connections'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['connections'], origin, destination, connection["cable_length"])
    return analyzer

# Funciones para creacion de datos

# Funciones de consulta

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


def compareConnections(connection1, connnection2):

    if (connection1["origin"] == connnection2["origin"]):
        if(connection1["destination"] == connnection2["destination"]):
            if(connection1["cable_id"] == connnection2["cable_id"]):
                return 0
    
    return -1

# Funciones de ordenamiento
