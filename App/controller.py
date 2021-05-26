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
from DISClib.ADT import list as lt

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
    
    landingPointsList = lt.newList('ARRAY_LIST')
    landingPointsFile = cf.data_dir + landingPointsFile
    lpFile = csv.DictReader(open(landingPointsFile, encoding="utf-8"), delimiter=",")
    for lp in lpFile:
        lt.addLast(landingPointsList, lp)
        model.prepareData(analyzer, lp)

    connectionsList = lt.newList('ARRAY_LIST')
    connectionsFile = cf.data_dir + connectionsFile
    cnnFile = csv.DictReader(open(connectionsFile, encoding="utf-8-sig"), delimiter=",")
    for cnn in cnnFile:
        # model.loadData(analyzer, cnn)
        lt.addLast(connectionsList, cnn)

    countriesList = lt.newList('ARRAY_LIST')
    countriesFile = cf.data_dir + countriesFile    
    cntFile = csv.DictReader(open(countriesFile, encoding="utf-8"), delimiter=",")
    for ctry in cntFile:
        lt.addLast(countriesList, ctry)
        model.loadCountry(analyzer, ctry)

    for point in lt.iterator(landingPointsList):
        name = point['name'].split(", ")
        if len(name) < 2:
            ctry = 'Micronesia'
        else:
            ctry = name[1]
        for country in lt.iterator(countriesList):
            if country['CountryName'] == ctry:
                capital = country['CapitalName'] + "-" + ctry
                model.addPoint(analyzer, capital)
                capitalData = country
                break
        actualPointList = None
        for connection in lt.iterator(connectionsList):
            if connection['origin'] == point['landing_point_id']:
                actualPointList = model.addLandingPoint(analyzer, point,
                                                       connection,
                                                       actualPointList,
                                                       capitalData)
        model.addPointConnections(analyzer, actualPointList)

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
