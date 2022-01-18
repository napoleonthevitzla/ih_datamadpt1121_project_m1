#!/usr/bin/env python
# coding: utf-8

# In[1]:


## IMPORTAMOS LIBRERÍAS
import pandas as pd
import os
import numpy as np
import requests
import geopandas as gpd 
from shapely.geometry import Point


# In[2]:


## Funciones a importar:

def distance_meters(lat_start, long_start, lat_finish, long_finish):
    # return the distance in metres between to latitude/longitude pair point in degrees (i.e.: 40.392436 / -3.6994487)
    start = to_mercator(lat_start, long_start)
    finish = to_mercator(lat_finish, long_finish)
    return start.distance(finish)

def distance_m(mercator_start, mercator_finish):
    return mercator_start.distance(mercator_finish)


def to_mercator(lat, long):
    # transform latitude/longitude data in degrees to pseudo-mercator coordinates in metres
    c = gpd.GeoSeries([Point(lat, long)], crs=4326)
    c = c.to_crs(3857)
    return c


# In[17]:



#FUNCIÓN QUE EXPORTA DATOS DE BICIMAD Y DEVUELVE EL DATASET CON EL MODELO DE DATOS QUE BUSCAMOS

def getdata_bicimad():
    bicimad_data = pd.read_json("../data/bicimad.json")
    bicimad_data = bicimad_data.drop(columns=['id','light',"number","activate","no_available","total_bases", "dock_bikes","free_bases","reservations_count","geometry_type"])
    bicimad_data['LONGITUD']=bicimad_data['geometry_coordinates'].map(lambda x:x.split(',')[0].replace("[","")).astype(float)
    bicimad_data['LATITUD']=bicimad_data['geometry_coordinates'].map(lambda x:x.split(',')[1].replace("]","")).astype(float)
    bicimad_data = bicimad_data.drop(columns=['geometry_coordinates'])
    bicimad_data = bicimad_data.rename(columns={'LONGITUD':'lat_finish','LATITUD':'long_finish'})
    bicimad_data["PUNTO B"] = bicimad_data.apply(lambda x: to_mercator(x["lat_finish"],x["long_finish"]), axis = 1)

    return bicimad_data


# In[6]:


#FUNCIÓN QUE EXPORTA DATOS DEL AYUNTAMIENTO Y DEVUELVE EL DATASET CON EL MODELO DE DATOS PARA UNIR CON ESCUELAS_INFANTILES

def getdata_colegios_publicos():
    colegios_publicos_data = requests.get('https://datos.madrid.es/egob/catalogo/202311-0-colegios-publicos.json')
    colegios_publicos_data = colegios_publicos_data.json()
    colegios_publicos_data = pd.json_normalize(colegios_publicos_data['@graph'])
    colegios_publicos_data = colegios_publicos_data.drop(columns=["@id","@type","id","relation","address.district.@id","address.area.@id","address.locality","address.postal-code","organization.organization-desc","organization.accesibility","organization.schedule","organization.services","organization.organization-name"])
    colegios_publicos_data = colegios_publicos_data.assign(Tipo_Centro = "Colegios Publicos")
    return colegios_publicos_data    
    


# In[7]:


#FUNCIÓN QUE EXPORTA DATOS DEL AYUNTAMIENTO Y DEVUELVE EL DATASET CON EL MODELO DE DATOS PARA UNIR CON COLEGIOS PUBLICOS

def getdata_escuelas_infantiles():
    escuelas_infantiles_data = requests.get('https://datos.madrid.es/egob/catalogo/202318-0-escuelas-infantiles.json')
    escuelas_infantiles_data = escuelas_infantiles_data.json()
    escuelas_infantiles_data = pd.json_normalize(escuelas_infantiles_data['@graph'])
    escuelas_infantiles_data = escuelas_infantiles_data.drop(columns=["@id","@type","id","relation","address.district.@id","address.area.@id","address.locality","address.postal-code","organization.organization-desc","organization.accesibility","organization.schedule","organization.services","organization.organization-name"])
    escuelas_infantiles_data =escuelas_infantiles_data.assign(Tipo_Centro = "Escuelas Infantiles")
    return escuelas_infantiles_data


# In[8]:


#FUNCIÓN QUE CONCATENA DATASETS

def concat_dataset_ayuntamiento(data1,data2):
    result = pd.concat([data1, data2], axis=0)
    return result

def concat_dataset_proyect(data1,data2):
    result2 = pd.merge(data1, data2 ,how="cross")
    return result2


# In[9]:


# FUNCIÓN QUE RENOMBRA LAS COLUMNAS DEL DATASET DEL AYUNTAMIENTO Y ASIGNA COORDENADA PUNTO A

def renamecols_ayuntamiento (ayuntamiento_data):
    ayuntamiento_data = ayuntamiento_data.rename(columns={'location.latitude':'lat_start','location.longitude':'long_start'})
    ayuntamiento_data["PUNTO A"] = ayuntamiento_data.apply(lambda x: to_mercator(x["lat_start"],x["long_start"]), axis = 1)


    


# In[11]:


# FUNCIÓN QUE AÑADE VALORES AL RESULTADO DE LA COLUMNA DE DISTANCIA Y ELIMINA LA INFORMACION NECESARIA Y LIMPIA LAS COLUMNAS RESTANTES

def distance_data (dataset, distancia):
    dataset["(distancia)"] = dataset.apply(lambda x: distance_m(x["PUNTO A"], x["PUNTO B"]), axis = 1)
    dataset = dataset.drop(['lat_start','long_start', 'long_finish', 'lat_finish','PUNTO A','PUNTO B'], axis='columns')    
    return dataset


# In[15]:


###
getdata_bicimad


# In[ ]:




