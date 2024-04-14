#clase de busuqeda
import openai
import re
import time
from datetime import datetime
import json

#Utiliza la(s) siguiente(s) clase(s)
from script_taller import taller

#UN arreglo rápido pa hacer pruebas sin chatgpt
class busqueda:
    
  #Constructor:
  def __init__(self, texto):
    #Definimos los valores de la búsqueda
    self.texto = texto


  #Con esta clase podemos crear un taller
  def crearTaller(self):
    descripcion = self.texto


    dicc = {
        "Tema": descripcion,
        "Duracion" : "5",
        "Cupos" : 5,
        "Modalidad" : "NULL",
        "Fecha" : "NULL",
        "Hora" : "NULL",
        "Nombre" : "NULL",
        "Recinto" : "NULL"
      }

    return dicc

''' 

ESTO SE OCUPA PERO NO QUIERO USAR LAS KEYS DEL CHAT GPT, para probar
class busqueda: 

  #Definimos valores de la búsqueda
  def __init__(self, texto):
    self.texto = texto

  
  #Función para crear una busqueda
  def crearTaller(self):

    #LLave para interactuar con la api de chat gpt
    openai.api_key = "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"
  
    attributes = [["Tema"],["Duración"],["Cupos"],["Modalidad","NULL"],["Fecha","NULL"],["Hora","NULL"],["Nombre","NULL"],["Recinto","NULL"]]

    #Le pedimos una descripción del taller que se quiere buscar
    description = self.texto

    #Creamos la consulta a chat gpt para que nos retorne datos del taller
    inicio = time.time()
    question = '"' + description.descripcion + '"' + 'De esta descripción de un taller, retorna un string con la temática del taller. El tema debe ser una frase corta, o incluso una palabra. Si no puedes deducir el tema, o de que se trata, retorna NULL'
    prompt = openai.Completion.create(engine="text-davinci-003",
                              prompt=question,
                              max_tokens = 2048)

    regex_temaynombre = "([a-zA-zÑñÁáÉéÍíÓóÚúÜü]+\s*)+"
    Tema = re.search(regex_temaynombre,prompt.choices[0].text).group()
    attributes[0].append(Tema)


    attributes

    question = '"' + description.descripcion + '"' + 'De esta descripción de un taller, retorna un string con el siguiente formato "duracionTaller;cuposTaller". Si en alguna parte menciona la duración que tendría el taller, entonces retorna el número de horas a las cuales corresponde (solo retorna un número) en el campo duracionTaller. Si por el contrario no se menciona, retorna NULL en ese campo.'
    question += ' Si en alguna parte menciona cuantos cupos tendra el taller (osea cuantas personas podran participar), retorna el numero de cupos (solo retorna un numero) en el campo cuposTaller, si no se menciona entonces retorna NULL en ese campo. Recuerda que no debes escribir el nombre del campo, ni poner en tu respuesta algo como "Duracion del taller: 2 horas", si no mas bien solo debes retornar un numero o NULL en cada campo.'
    question += ' Ejemplos de outputs correctos son "3;20", "NULL;25", etc. No deduzcas duracion del taller ni cupos si no lo dice explicitamente o no es obvio, solo extrae la información si es que puedes encontrarla dentro de la descripción.'
    prompt = openai.Completion.create(engine="text-davinci-003",
                              prompt=question,
                              max_tokens = 2048)

    regex_duracionycupos = "([A-Z]+|(\d+(\.)\d+|\d+));([A-Z]+|\d+)"
    Duracion = re.search(regex_duracionycupos,prompt.choices[0].text).group().strip().split(';')[0]
    Cupos = re.search(regex_duracionycupos,prompt.choices[0].text).group().strip().split(';')[1]
    attributes[1].append(Duracion)
    attributes[2].append(Cupos)

    dicc = {
      "Tema": attributes[0][1],
      "Duracion" : attributes[1][1],
      "Cupos" : attributes[2][1],
      "Modalidad" : "NULL",
      "Fecha" : "NULL",
      "Hora" : "NULL",
      "Nombre" : "NULL",
      "Recinto" : "NULL"
    }

    print(dicc)

    return dicc


'''