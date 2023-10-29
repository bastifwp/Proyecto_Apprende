#Clase del taller
import requests

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




  #Función que crea 5 posibles talleristas relacionado al taller (Aquí ocupamos la api de búsqueda)
  def buscarTallerista(self):

    posibles_talleristas = []
    posibles_insumos = []  #Por implementar

    #Función que realiza consultas a API de google (para llamar recursivamente en caso de que no encuentre suficientes opciones)
    def make_query(api_key, se_id, start, search_query, n_talleristas_encontrados, n_iteraciones):

        '''
        api_key: kye de la api donde pedirá la request,
        se_id: motor de búsqueda que utilizará,
        start: desde que index de resultado buscará (si es 0 mostrara los primeros 10, si es 11, inicia del 11 y muestra los 10 siguientes)
        '''

        iteraciones_actual = n_iteraciones
        actual_start = start
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
            print(results["error"]["message"])

          #terminamos ejecución de función
          return


        #Filtraremos los resultados recorriendo cada respuesta, contaremos las válidas
        n_posibles_talleristas = n_talleristas_encontrados

        #Recorresmos los resultados
        for i in range(10):

          #Si hay resultados
          if "items" in results:

            #Filtramos algunos resultados según el dominio
            link = results["items"][i]["link"]
            #print("No filtrado: ", link)

            #Filtros para linkedin
            if "linkedin.com" in link:

              #Sólo queremos a personas
              if "/in/" in link:
                posibles_talleristas.append(link)
                n_posibles_talleristas += 1

            #Filtros para superprof
            if "superprof" in link:

              #Sólo queremos a personas
              if "/blog/" not in link and "/clases/" not in link:
                posibles_talleristas.append(link)
                n_posibles_talleristas += 1
                #print(results["items"][i])

            #Vemos si ya tenemos la cantidad de usuarios necesaria
            if n_posibles_talleristas >= 5:
              return


        #Luego de revisar los resultados, si no hemos encontrado 5 posibles talleristas volver a llamar a la función
        if n_posibles_talleristas < 5:

          #Verificamos número de iteraciones (requests a google)
          if iteraciones_actual >= 10:
            print("No se han encontrado más resultados")
            return

          #Se realiza otra request para que encuentre más talleristas
          make_query(api_key, se_id, actual_start+11, search_query, n_talleristas_encontrados, iteraciones_actual+1)



    #Ahora hay que llamar a la función de arriba, para esto tenemos que crear la descripción con el taller.
    busqueda = "Talleristas para un taller: " + self.tema + " en modalidad " + self.modalidad
    print("Búsqueda realizada: ", busqueda)

    #Determinamos las keys e ids:
    API_KEY = "AIzaSyDDqe8IL8-g4Wkl3YuxhNWsP04uvLad6Ug"
    SEARCH_ENGINE = "b0b920b1c91a044e5"

    #Ahora realizamos la llamada
    make_query(API_KEY, SEARCH_ENGINE, 0, busqueda, 0,0)

    #Creamos a los talleristas con el link y los demás atributos en null.
    resultado_talleristas = posibles_talleristas
    resultado_insumos = [] #Posteriormente los insumos los haremos de manera independiente.

    return respuesta(resultado_talleristas, resultado_insumos)