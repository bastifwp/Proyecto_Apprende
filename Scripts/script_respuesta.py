#Clase respuesta

#Utiliza la siguente clase de otro script
from script_tallerista import tallerista

class respuesta:

  def __init__(self, link_talleristas, link_insumos):
    self.link_talleristas = link_talleristas
    self.link_insumos = link_insumos

  def __dict__(self):
    return {
        "link_talleristas" : self.link_talleristas,
        "link_insumos" : self.link_insumos
    }

  #Crearmos al tallerista seleccionado
  def seleccionarTallerista(self):

    #nombre, link_contacto, email, numero
    print("Posibles talleristas encontrados:")
    numeros = []

    for i in range(len(self.link_talleristas)):
      print(str(i+1) + ":", self.link_talleristas[i])
      numeros.append(str(i+1))

    #Ahora el usuario debe rellenar los datos del usuario
    n_link = input("Ingrese el número de link del tallerista que desee: ")

    #Verificamos que haya seleccionado un número válido
    while n_link.strip() not in numeros:
      n_link = input("Ingrese un número válido: ")
    n_link = int(n_link)

    while n_link > len(self.link_talleristas) or n_link <= 0:
      n_link = int(input("Ingrese un número dentro del rango mostrado: "))


    #Pedimos que rellene los datos
    print("\nIngrese los datos necesarios del tallerista (ingrese" +  " \"null\" "  + "en caso de no encontrar datos): ")
    nombre = input("Nombre del tallerista: ").strip()
    email = input("Email del tallerista: ").strip()
    numero = input("Numero del tallerista: ").strip()

    #Aqui podríamos verificar los datos

    #Creamos al tallerista
    return tallerista(nombre, self.link_talleristas[n_link-1], email, numero)