import requests
from functools import reduce
import operator
import pandas as pd



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



def getFromDict(diccionario,mapa):
    """
    Esta función accede a los values de los diccionarios que contiene un json.
    Args: diccionario y posición dentro del diccionario donde se encuentra el value que deseo. 
    Return: Value de un diccionario.
    """
    return reduce(operator.getitem,mapa,diccionario)



def type_point(lista):
    """
    Esta función sirve para devolver un tipo "point" a partir de una lista de coordenadas.
    Arg: coordenadas (lista)
    Return: diccionario donde el primer par es el tipo y el segundo la lista de coordenadas.
    """
    return {"type":"Point", "coordinates": lista}



def extraetodo(json):
    """
    Esta función sirve para convertir un json en una lista de diccionarios con las keys seleccionadas.
    Args:json
    Return: lista de diccionarios.
    """
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
    """
    Esta función normaliza los datos de una columna de un dataframe.
    Args:dataframe(df) y columna.
    Return:lista con los datos normalizados de la columna argumento.
    """
    result = []
    for i,row in df.iterrows():
        mini = df[col].min()
        maxi = df[col].max()
        result.append((row[col]- mini)/(maxi-mini))
    return result



def weights(df):
    """
    Esta función itera por un df multiplicando el dato contenido en la columna "normalizado" por un peso específicco dado.
    Arg: df.
    Return: lista de los datos norlizados multiplicados por su peso.

    """
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
    Arg:df1,df2,df3 (dataframes)
    Return: una único df que es el resultado de la unión de todos los que le paso como parámetros.
    """
    return pd.concat([df1,df2,df3])