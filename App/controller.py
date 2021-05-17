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

def loadServices(analyzer, lpsfile, connectionsfile, countriesfile):

    lpsfile = cf.data_dir + lpsfile
    input_file = csv.DictReader(open(lpsfile, encoding="utf-8"), delimiter=",")

    for lp in input_file:
        model.addLandingPoint(analyzer, lp)

    connectionsfile = cf.data_dir + connectionsfile
    input_file = csv.DictReader(open(connectionsfile, encoding="utf-8"), delimiter=",")

    for connection in input_file:
        model.addConnection(analyzer, connection)

    

    # lastservice = None
    # for service in input_file:
    #     if lastservice is not None:
    #         sameservice = lastservice['ServiceNo'] == service['ServiceNo']
    #         samedirection = lastservice['Direction'] == service['Direction']
    #         samebusStop = lastservice['BusStopCode'] == service['BusStopCode']
    #         if sameservice and samedirection and not samebusStop:
    #             model.addStopConnection(analyzer, lastservice, service)
    #     lastservice = service
    # model.addRouteConnections(analyzer)
    return analyzer

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
