#Entorno para realizar pruebas
from script_busqueda import busqueda
from script_taller import taller
from script_tallerista import tallerista
from script_respuesta import respuesta
from fastapi import FastAPI
import json
from pydantic import BaseModel
from datetime import date,time
from typing import Optional
import re

class user_input(BaseModel):
    descripcion : str

class taller_listo(BaseModel):
    Tema : str
    Duracion : float
    Cupos : int
    Modalidad : str
    Fecha : date
    Hora : time
    Nombre : Optional[str]
    Recinto : str


class respuesta(BaseModel):
    link_talleristas : list
    #link_insumos : Optional[list]


class tallerista(BaseModel):
    Nombre : str
    link_contacto : str
    email : str
    numero : int


class para_pedir_nombre(BaseModel):
    texto : str
    tema : str
    nombre : str

class para_pedir_lista(BaseModel):
    tema : str
    modalidad : str

api_talleristas = FastAPI()


@api_talleristas.post("/Busqueda")
def obtener_taller(texto:user_input):

    #Creamos una nueva busqueda llamando al constructor y le pasamos un parámtro
    if re.fullmatch("\s*",texto.descripcion) or texto.descripcion == "":
        return 400
    else:
        nuevaBusqueda = busqueda(texto)

        #Creamos un taller con la búsqueda
        nuevoTaller = nuevaBusqueda.crearTaller()
        return nuevoTaller

@api_talleristas.put("/Taller")
def crear_nombre(datos:para_pedir_nombre):

    '''
    Esto se ocupa pero no lo hago pa no usar chatgpt

    nuevoTaller = taller.tema_nombre(datos.tema,datos.nombre)
    texto = datos.texto
    tema = nuevoTaller.tema
    nombre = nuevoTaller.nombre

    nuevoTaller.nombre = nuevoTaller.nombre_chatgpt(texto,tema,nombre)
    '''
    nuevoTaller = taller.tema_nombre(datos.tema,datos.nombre)

    return nuevoTaller.nombre


@api_talleristas.post("/Respuesta")
def buscar_talleristas(Taller:para_pedir_lista):
        
        #Buscamos posibles talleristas para el taller
        nuevoTaller = taller.tema_modalidad(Taller.tema,Taller.modalidad)
        if re.fullmatch("\s*",nuevoTaller.tema) or nuevoTaller.tema == "": 
            return 400 
        else: 
            print("Estamos aqui, vamos a buscar un tallerista")
            listaTalleristas = nuevoTaller.buscarTallerista()


        return listaTalleristas

        #Dejamos que el usuario seleccione al tallerista
        #nuevoTallerista = nuevaRespuesta.seleccionarTallerista()

        #Verificamos que se creó correctamente 
        #print("Se ha creado exitosamente el tallerista, con la siguiente información: \n")
        #print(nuevoTallerista.__dict__())

@api_talleristas.post("/Tallerista")
def ingresar_tallerista(Tallerista:tallerista):
        
    nuevoTallerista = tallerista(Tallerista)
    return nuevoTallerista

