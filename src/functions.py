import requests
from functools import reduce
import operator
import pandas as pd
from dotenv import load_dotenv
import os


def geocode(direccion):
    """
    Esta función saca las coordenadas de la dirección que le pases.
    Args: una dirección (string).
    Return: Intenta devolver las coordeandas de la dirección que le paso como argumento (latitud y longitud) y sino, me devuelve el json resultante de la request a la api.
    """
    data = requests.get(f"https://geocode.xyz/{direccion}?json=1").json()
    try:
        return {"type": "Point", "coordinates": [data["latt"], data["longt"]]}
    except:
        return data


def request(ciudad,requirements, client_id, client_secret ):

    url_query = 'https://api.foursquare.com/v2/venues/search'

    dfciudad= pd.DataFrame(colums=["nombre","latitud","longitud","location", "categoria"])
    for requirement in requirements:
        parametros = {
            "client_id": client_id,
            "client_secret": client_secret,
            "v": "20180323",
            "ll": f"{ciudad['coordinates'][0]}, {ciudad['coordinates'][1]}",
            "query": requirement
        }
    
        result=requests.get(url_query, params = parametros).json()
        solucion=extraetodo(result["response"]["venues"])
        df2=pd.DataFrame(solucion)
        df2["categoria"]= requirement
        dfciudad.append(df2)
    return dfciudad






def getFromDict(diccionario,mapa):
    return reduce(operator.getitem,mapa,diccionario)


def type_point(lista):
    return {"type":"Point", "coordinates": lista}


def extraetodo(json):
    todo = {"nombre": ["name"], "latitud": ["location", "lat"], "longitud": ["location", "lng"]} 
    total = []
    for elemento in json:
        libre = {key: getFromDict(elemento, value) for key,value in todo.items()}
        libre["location"] = type_point([libre["latitud"], libre["longitud"]])
        total.append(libre)
    return total

def concat_requirements(df1,df2,df3,df4,df5):
    """
    Esta función concatena los df que le pase.
    Arg:df1,df2,df3,df4,df5 (dataframes)
    Return: una único df que es el resultado de la unión de todos los que le paso como parámetros.
    """
    return pd.concat([df1,df2,df3,df4,df5])



def normalize(df,col):
    result = []
    for i,row in df.iterrows():
        mini = df[col].min()
        maxi = df[col].max()
        result.append((row[col]- mini)/(maxi-mini))
    return result


def weights(df):
    lista_pesos=[]
    for i,row in df.iterrows():
        if row["categoria"]=="Disco":
            lista_pesos.append(row["normalizado"]*0.2)
        elif row["categoria"]=="Diseño":
            lista_pesos.append(row["normalizado"]*0.2)
        elif row["categoria"]=="Starbucks":
            lista_pesos.append(row["normalizado"]*0.4)
        elif row["categoria"]=="Vegan":
            lista_pesos.append(row["normalizado"]*0.1)
        else:
            lista_pesos.append(row["normalizado"]*0.1)
    return lista_pesos


def concat_ciudades(df1,df2,df3):
    """
    Esta función concatena los df que le pase.
    Arg:df1,df2,df3,df4,df5 (dataframes)
    Return: una único df que es el resultado de la unión de todos los que le paso como parámetros.
    """
    return pd.concat([df1,df2,df3])