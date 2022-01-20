####IMPORTAMOS LIBRERÍAS
from email import parser
import pandas as pd
import os
import numpy as np
import requests
import geopandas as gpd 
from shapely.geometry import Point
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument(
    "--ejecucion",
    dest = "ejecucion",
    default = "MasCercana",
    help = "parametro para selecionar el tipo de ejecucion. Posibles valores: MasCercana , TodasEstaciones"
)
args = parser.parse_args(sys.argv[1:])


#### DEFINIMOS FUNCIONES 
def distance_m(mercator_start, mercator_finish):
    return mercator_start.distance(mercator_finish)


def to_mercator(lat, long):
    # transform latitude/longitude data in degrees to pseudo-mercator coordinates in metres
    c = gpd.GeoSeries([Point(lat, long)], crs=4326)
    c = c.to_crs(3857)
    return c

#FUNCIÓN QUE RECIBE DATOS DE BICIMAD Y DEVUELVE EL DATASET CON EL MODELO DE DATOS QUE BUSCAMOS

def getdata_bicimad(json):
    bicimad_data = pd.read_json(json)
    bicimad_data = bicimad_data.drop(columns=['id','light',"number","activate","no_available","total_bases", "dock_bikes","free_bases","reservations_count","geometry_type"])
    bicimad_data['LONGITUD']=bicimad_data['geometry_coordinates'].map(lambda x:x.split(',')[0].replace("[","")).astype(float)
    bicimad_data['LATITUD']=bicimad_data['geometry_coordinates'].map(lambda x:x.split(',')[1].replace("]","")).astype(float)
    bicimad_data = bicimad_data.drop(columns=['geometry_coordinates'])
    bicimad_data = bicimad_data.rename(columns={'LATITUD':'lat_finish','LONGITUD':'long_finish','name':'BiciMAD station','address':'Station location'})
    bicimad_data["PUNTO B"] = bicimad_data.apply(lambda x: to_mercator(x["lat_finish"],x["long_finish"]), axis = 1)
    result = bicimad_data

    return result


#FUNCIÓN QUE RECIBE URL DE AYUNTAMIENTO Y DEVUELVE EL DATASET DE COLEGIOS CON EL MODELO DE DATOS LIMPIO

def getdata_public_school(url):
    colegios_publicos_data = requests.get(url)
    colegios_publicos_data = colegios_publicos_data.json()
    colegios_publicos_data = pd.json_normalize(colegios_publicos_data['@graph'])
    colegios_publicos_data = colegios_publicos_data.drop(columns=["@id","@type","id","relation","address.district.@id","address.area.@id","address.locality","address.postal-code","organization.organization-desc","organization.accesibility","organization.schedule","organization.services","organization.organization-name"])
    result = colegios_publicos_data.assign(Tipo_Centro = "Colegios Publicos")
    return result


#FUNCIÓN QUE RECIBE URL DE AYUNTAMIENTO Y DEVUELVE EL DATASET DE ESCUELAS CON EL MODELO DE DATOS LIMPIO

def getdata_escuelas_infantiles(url):
    escuelas_infantiles_data = requests.get(url)
    escuelas_infantiles_data = escuelas_infantiles_data.json()
    escuelas_infantiles_data = pd.json_normalize(escuelas_infantiles_data['@graph'])
    escuelas_infantiles_data = escuelas_infantiles_data.drop(columns=["@id","@type","id","relation","address.district.@id","address.area.@id","address.locality","address.postal-code","organization.organization-desc","organization.accesibility","organization.schedule","organization.services","organization.organization-name"])
    result =escuelas_infantiles_data.assign(Tipo_Centro = "Escuelas Infantiles")
    return result

#FUNCIÓN QUE MERGEA DATASET DE AYUNTAMIENTO Y LOS LIMPIA Y AÑADE COLUMNA PUNTO A

def concat_dataset_ayuntamiento(data1,data2):
    ayuntamiento_data = pd.concat([data1, data2], axis=0)
    ayuntamiento_data['address.street-address']=ayuntamiento_data['address.street-address'].str.title()
    ayuntamiento_data = ayuntamiento_data.rename(columns={'location.latitude':'lat_start','location.longitude':'long_start','title':'Place of interest','address.street-address':'Place address'})
    ayuntamiento_data["PUNTO A"] = ayuntamiento_data.apply(lambda x: to_mercator(x["lat_start"],x["long_start"]), axis = 1)
    result = ayuntamiento_data
    return result

#FUNCIÓN QUE MERGEA DATASET DEL PROYECTO Y CREA LA COLUMNA CON EL RESULTADO DE LA DISTANCIA EN METROS ENTRE LOS PUNTOS A Y B

def concat_dataset_proyect(data1,data2):
    proyect_data = pd.merge(data1, data2 ,how="cross")
    proyect_data['Distancia'] = proyect_data.apply(lambda x: distance_m(x["PUNTO A"], x["PUNTO B"]), axis = 1)
    result = proyect_data.drop(['lat_start','long_start', 'long_finish', 'lat_finish','PUNTO A','PUNTO B'], axis='columns')
    # proyect_data['address.street-address']=ayuntamiento_data['address.street-address'].str.title() ##ELIMINAR SI EJECUTA ##
    return result


## FUNCIÓN PARA RECIBIR EL INPUT Y DEVOLVER LA DISTANCIA MÍNIMA

def result_one(data):
    all_results = data[data["Place of interest"] == input('Pon el lugar de interés: ')]
    selection = all_results[all_results['Distancia'] == all_results['Distancia'].min()] # Comprobar si es Distancia o Distance
    result_one = selection[["Place of interest","Tipo_Centro","Place address","BiciMAD station","Station location"]]
    return result_one

## FUNCIÓN PARA RECIBIR EL INPUT Y DEVOLVER TODOS LOS RESULTAOS

def result_all(data):
    all_results = data[data["Place of interest"] == input('Pon el lugar de interés: ')]
    selection = all_results[all_results['Distancia'] == all_results['Distancia']]
    result = selection[["Place of interest","Tipo_Centro","Place address","BiciMAD station","Station location"]]
    return result


## FUNCIÓN PARA RECIBIR UN DATAFRAME Y DESCARGA UN CSV EN CARPETA "data"
def create_csv(df_result):
    #df_csv = df_result.sort_values(ascending=False)
    df_result.to_csv('../data/bicimad_AH.csv', index=False)
    return print("Comprueba tu carpeta")


    #### DEFINIMOS CONSTANTES
# Estas constantes pueden ser argumentos para argparse?

json_bicimad = "../data/bicimad.json"
url_colegios_json ='https://datos.madrid.es/egob/catalogo/202311-0-colegios-publicos.json'
url_escuelas_json ='https://datos.madrid.es/egob/catalogo/202318-0-escuelas-infantiles.json'

### PROGRAMA A EJECUTAR:

# Punto de partida: obtenemos los 3 dataset
data_bicimad = getdata_bicimad(json_bicimad)
data_kindergarten = getdata_escuelas_infantiles(url_escuelas_json)
data_public_school =getdata_public_school(url_colegios_json)
# 1º Merge del Dataset ayuntamientos
data_city_hall = concat_dataset_ayuntamiento(data_kindergarten,data_public_school)
# 2º Merge dataset de ayuntamiento y bicimad para la consulta
data_project = concat_dataset_proyect(data_city_hall,data_bicimad)
# 3º Ejecutamos las funciones para obtener ambos resultados
data_one = result_one(data_project)
data_all = result_all(data_project)
#Escuela infantil municipal Doña Francisquita

# 4º Creamos los CSV con el resultado 
todas_ubicaciones1 =create_csv (data_all)
ubicacion_mas_cercana1 = create_csv (data_one)

## FUNCIÓN EJECUCIÓN

if args.ejecucion == "MasCercana":
    ubicacion_mas_cercana = ubicacion_mas_cercana1
    #ubicacion_mas_cercana.to_csv("../output/ubicacion_mas_cercana.csv", sep= ";")
    print("archivo estacion mas cercana guardado en la carpeta de output")
elif args.ejecucion == "TodasEstaciones":
    todas_ubicaciones = todas_ubicaciones
    #todas_ubicaciones.to_csv("../output/todas_las_ubicaciones.csv", sep= ";")
    print("archivo de todas las estaciones guardado en la carpeta de output")
else:
    print("opcion erronea, solo podemos meter: MasCercana o TodasEstaciones")
