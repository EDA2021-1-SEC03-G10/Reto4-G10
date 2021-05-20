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

def loadServices(analyzer, landingPointsFile, connectionsFile, countriesFile):

    landingPointsFile = cf.data_dir + landingPointsFile
    lpFile = csv.DictReader(open(landingPointsFile, encoding="utf-8"), delimiter=",")
    for lp in lpFile:
        model.prepareData(analyzer, lp)

    connectionsFile = cf.data_dir + connectionsFile
    cnnFile = csv.DictReader(open(connectionsFile, encoding="utf-8-sig"), delimiter=",")
    for connection in cnnFile:
        model.loadData(analyzer, connection)

    countriesFile = cf.data_dir + countriesFile    
    cntFile = csv.DictReader(open(countriesFile, encoding="utf-8"), delimiter=",")
    for country in cntFile:
        model.loadCountry(analyzer, country)

    model.addLandingPoints(analyzer)
    model.addPointConnections(analyzer)

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
