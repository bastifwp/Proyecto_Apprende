#Clase del tallerista
class tallerista:

  #Crear un tallerista:
  def __init__(self, nombre, link_contacto, email, numero):
    self.nombre = nombre
    self.link_contacto = link_contacto
    self.email = email
    self.numero = numero


  #Función que muestra la información del tallerista
  def __dict__(self):
    return {
        "nombre" : self.nombre,
        "link_contacto" : self.link_contacto,
        "email" : self.email,
        "numero" : self.numero,
    }

  #Funciones para cambiar datos
  def updateNombre(self, nuevo_nombre):
    self.nombre = nuevo_nombre

  def updateNumero(self, nuevo_numero):
    self.numero = nuevo_numero

  def updateEmail(self, nuevo_email):
    self.email = nuevo_email