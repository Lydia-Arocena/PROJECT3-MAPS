import requests
from functools import reduce
import operator

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

def sum_requirements(l1,l2,l3,l4,l5):
    """
    Esta función suma las listas que le pase.
    Arg:l1,l2,l3,l4,l5 (list)
    Return: una única lista que es el resultado de la unión de todas las que le paso como parámetros.
    """
    return [*l1,*l2,*l3,*l4,*l5]