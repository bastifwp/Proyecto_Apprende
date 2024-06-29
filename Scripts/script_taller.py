#Clase del taller
import requests
import openai
import re
import time
from bs4 import BeautifulSoup

#Utiliza las siguientes clases 
from script_respuesta import respuesta


class taller:

  #Definimos los datos para cada taller
  def __init__(self, nombre, tema, duracion, fecha, hora, cupos, modalidad, recinto):
    self.nombre = nombre
    self.tema = tema
    self.duracion = duracion
    self.fecha = fecha
    self.hora = hora
    self.cupos = cupos
    self.modalidad = modalidad
    self.recinto = recinto

  @classmethod
  def tema_nombre(cls, tema, nombre):
    nuevo_taller = cls.__new__(cls)
    nuevo_taller.nombre = nombre
    nuevo_taller.tema = tema
    nuevo_taller.duracion = "NULL"
    nuevo_taller.fecha = "NULL"
    nuevo_taller.hora = "NULL"
    nuevo_taller.cupos = "NULL"
    nuevo_taller.modalidad = "NULL"
    nuevo_taller.recinto = "NULL"

    return nuevo_taller
  
  @classmethod
  def tema_modalidad(cls, tema, modalidad):
    nuevo_taller = cls.__new__(cls)
    nuevo_taller.nombre = "NULL"
    nuevo_taller.tema = tema
    nuevo_taller.duracion = "NULL"
    nuevo_taller.fecha = "NULL"
    nuevo_taller.hora = "NULL"
    nuevo_taller.cupos = "NULL"
    nuevo_taller.modalidad = modalidad
    nuevo_taller.recinto = "NULL"

    return nuevo_taller

  #Función que retorna los datos del taller en forma de diccionario
  def __dict__(self):
    return {
        "nombre" : self.nombre,
        "tema": self.tema,
        "duracion": self.duracion,
        "fecha" : self.fecha,
        "hora" : self.hora,
        "cupos" : self.cupos,
        "modalidad" : self.modalidad,
        "recinto" : self.recinto
    }


  #Funciones que modifica los datos del talller
  def updateDuracion(self, nueva_duracion):
    self.duracion = nueva_duracion

  def updateFecha(self, nueva_fecha):
    self.fecha = nueva_fecha

  def updateHora(self, nueva_hora):
    self.hora = nueva_hora

  def updateCupos(self, nuevo_cupos):
    self.cupos = nuevo_cupos

  def updateModalidad(self, nueva_modalidad):
    self.modalidad = nueva_modalidad
  
  def updateRecinto(self, nuevo_recinto):
    self.recinto = nuevo_recinto


  def nombre_chatgpt(self,texto,tema,nombre_antiguo):

    regex_temaynombre = "([a-zA-zÑñÁáÉéÍíÓóÚúÜü]+\s*)+"
    question = '"' + texto + '"' + 'De esta descripción de un taller, cuya temática es ' +tema+ ', inventa un nombre para el taller sin usar caracteres especiales y retornalo (no retornes Nombre del taller: blablabla, solo retorna el nombre a secas)'
    if nombre_antiguo != '':
      question += ' El nombre no debe ser este: '+ nombre_antiguo
    question += '. Devuelve solo el string correspondiente al nombre, sin comillas, y que comience con mayúscula'
    #print("\nEstoy pensando en un nuevo nombre para tu taller...")
    time.sleep(10)
    prompt = openai.Completion.create(engine="text-davinci-003",
                                      prompt=question,
                                      max_tokens = 2048)
    Nombre = re.search(regex_temaynombre,prompt.choices[0].text).group().strip()

    return Nombre


  #Función que crea 5 posibles talleristas relacionado al taller (Aquí ocupamos la api de búsqueda)
  def buscarTallerista(self):


    #haremos que un tallerista sea un diccionario. e iremos haciendo append para tener una lista de diccionarios 
    posibles_talleristas = []


    #Función que realiza una busqueda en la API de google
    def make_query(api_key, se_id, start, search_query):
        
        #api_key: kye de la api donde pedirá la request,
        #se_id: motor de búsqueda que utilizará,
        #start: desde que index de resultado buscará (si es 0 mostrara los primeros 10, si es 11, inicia del 11 y muestra los 10 siguientes)
  
        url = "https://www.googleapis.com/customsearch/v1"#Aquí mandaremos nuestra request

        #parámetros para la búsqueda
        params = {
            "q" : search_query, #Lo que buscaremos
            "key" : api_key,  #Key de la api
            "cx" : se_id, #id del motor de busqueda
            "num" : 10, #Resultados a mostrar(max=10)
            "gl" : "cl", #Donde buscar
            "start" : start
        }

        #Realizamos la consulta
        response = requests.get(url,params=params)
        results = response.json() 

        #Verificamos si nos pudimos conectar con la API
        if(response.status_code != 200):
          print("Comunicación con API de google fallida")

          #Mostramos el error
          if "error" in results:
            print("Errores: \n")
            print(results["error"]["message"])
            print(results["error"])

          #terminamos ejecución de función
          return


        #Si la busqueda otorga resultados.
        if "items" in results:
          
          #veamos que hay en resultados

          #Recorremos los resultados
          for i in range(0, len(results["items"])):

            #Debemos filtrar los resultados según los dominios
            link = results["items"][i]["link"]
            resp = requests.get(link) #Así tenemos el html jeje
            doc = BeautifulSoup(resp.text, "html.parser")
            tallerista_data = {}
            print(link)


            #Linkedin RIP
            '''#Si encontró un tallerista de linkedin
            if "linkedin.com" in link:

              #Sólo queremos a personas
              if "/in/" in link:
                posibles_talleristas.append(link)'''

            #Filtros para superprof
            if "superprof" in link:

              #Sólo queremos a personas
              if "/blog/" not in link and "/clases/" not in link:
                #posibles_talleristas.append(link)

                #-----SCRAPPER-----
                nombre = doc.find("div", class_="name").text.strip() #Lo cambié un poco porque guardaba cosas de más
                nombre = nombre.split()[0] #DETALLE: sólo se almacena el primer nombre (se pierde 2° nombre/apellido en caso de que haya)
                print("Nombre:", nombre)
                tallerista_data["Nombre"] = nombre

                #En este caso hay varias tarjetas, considearemos sólo online y presencial
                tag_ubicacion_presencial1 = doc.find("li", class_="home")
                tag_ubicacion_presencial2 = doc.find("span", class_="picto pin")
                tag_ubicacion_online = doc.find("li", class_="webcam")

                modalidad = []

                if tag_ubicacion_presencial1 or tag_ubicacion_presencial2:
                    modalidad.append("Presencial")

                if tag_ubicacion_online:
                    modalidad.append("Online")

                print("Modalidad:", modalidad)
                tallerista_data["Modalidad"] = "" #Lo hice str para efectos del frontend
                for mod in modalidad:
                  if tallerista_data["Modalidad"] != "":
                    tallerista_data["Modalidad"] += ", "+mod
                  else:
                    tallerista_data["Modalidad"] += mod

                #Buscamos el precio (Aqui podría haber errores en caso de que no pille precio, pero no debería)          
                precio = doc.find("ul", class_="infos").find("span", class_="value").text
                print("Precio:", precio)
                tallerista_data["Precio"] = precio

                temas = doc.find("div", class_="subjects cat-trigger").find_all("li")
                temas_final="" #Lo hice str para efectos del frontend
                for tema in temas:
                    if temas_final != "":
                      temas_final += ", "+tema.text.strip()
                    else:
                      temas_final += tema.text.strip()
                tallerista_data["Tema"] = temas_final
                print("Temas:", temas_final)

                tallerista_data["Enlace"] = link

                fuente = "superprof"
                print("Fuente:", fuente)
                tallerista_data["Fuente"] = fuente

                

                print(tallerista_data)

                #Guardamos el tallerista como diccionario en la lista de posibles
                if nombre != None:
                  posibles_talleristas.append(tallerista_data)


            #Filtros para tusclasesparticulares
            if "tusclasesparticulares" in link:
              
              print("El link contiene tus clases particulares")

              #Sólo queremos personas
              if "/profesores/" in link and ".aspx" in link: #El ".aspx" es para que no salgan páginas con varios resultados de búsqueda
                #posibles_talleristas.append(link)

                if doc.find("img", class_= "notfound"): #Esto es porque a veces salían páginas que ya no existían
                  print("El aviso ya no está disponible")

                else:

                  #-----SCRAPPER-----
                  nombre_tag = doc.find(["a"], id="lnkProfile")
                  nombre ="-"
                  if nombre_tag:
                    nombre = nombre_tag.text

                  print("Nombre:", nombre)
                  tallerista_data["Nombre"] = nombre

                  #ESTO DE MODALIDAD HAY QUE PROBARLO
                  
                  #Si el tag ubicacion tiene el texto online -> es online, sino es presencial  
                  tag_ubicacion = doc.find("div", id="line_location").find("span")

                  #Si se encontró el tag:
                  modalidad = ""
                  if tag_ubicacion:
                      if tag_ubicacion.text.strip() == "On-line":
                          modalidad = "Online"
                      else:
                          modalidad = "Presencial"

                  print("Modalidad:", modalidad)
                  tallerista_data["Modalidad"] = str(modalidad) #Lo hice str para efectos del frontend

                  #Buscamos el precio 
                  precio = "-"
                  precio_tag = doc.find("div", class_="price").find("b")
                  if precio_tag:
                    precio = "$" + precio_tag.text
                  print("Precio:", precio)
                  tallerista_data["Precio"] = precio

                  #Buscamos el tema
                  Tema = "-"
                  tema_tag = doc.find("span", class_= "subject")
                  if tema_tag:
                    Tema = tema_tag.text
                  print("Tema:", Tema)
                  tallerista_data["Tema"] = Tema

                  tallerista_data["Enlace"] = link                  

                  Fuente = "tusclasesparticulares"
                  print("Fuente:",Fuente)
                  tallerista_data["Fuente"] = Fuente


                  
                  print(tallerista_data)

                  #Guardamos el tallerista como diccionario en la lista de posibles
                  if nombre != None:
                    posibles_talleristas.append(tallerista_data)

  
  

    #Ahora hay que llamar a la función de arriba, para esto tenemos que crear la descripción con el taller.
    busqueda = "Profesores para clases de " + self.tema + " con modalidad de la clase " + self.modalidad
    print("Búsqueda realizada: ", busqueda)

    #Determinamos las keys e ids de google:
    claves = open("Clave_google.txt", "r")
    API_KEY =  claves.readline().strip()#la del dc
    SEARCH_ENGINE = "250f16f81b8ac49dc" #la del dc


    #Realizamos búsqueda hasta tener al menos 5 talleristas
    make_query(API_KEY, SEARCH_ENGINE, 0, busqueda)

    #Si luego de la busqueda no tenemos suficientes -> iterar máximo 2 veces (para no sobrepasar máximo de querys de google)
    for i in range(1, 3):

      if len(posibles_talleristas) >= 5:
        break

      else:
        make_query(API_KEY, SEARCH_ENGINE, 11*i, busqueda)






    #Creamos a los talleristas con el link y los demás atributos en null.
    resultado_talleristas = posibles_talleristas
    resultado_insumos = [] #Posteriormente los insumos los haremos de manera independiente.

    respuesta = {
      "link_talleristas" : resultado_talleristas
    }

    print("data:", respuesta["link_talleristas"])
    print("primero:", respuesta["link_talleristas"][0])

    return respuesta