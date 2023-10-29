#Entorno para realizar pruebas
from script_busqueda import busqueda



if __name__ == "__main__":
    
    texto = input("Hola! Estoy aquí para ayudarte a organizar un nuevo taller :)\nIntroduce una descripción del taller que te gustaría organizar: ")

    #Creamos una nueva busqueda
    nuevaBusqueda = busqueda(texto)

    #Creamos un taller con la búsqueda
    nuevoTaller = nuevaBusqueda.crearTaller()
    print("Nuevo taller: ", nuevoTaller.__dict__(), "\n")


    #Buscamos posibles talleristas para el taller
    nuevaRespuesta = nuevoTaller.buscarTallerista()


    #Dejamos que el usuario seleccione al tallerista
    nuevoTallerista = nuevaRespuesta.seleccionarTallerista()

    #Verificamos que se creó correctamente 
    print("Se ha creado exitosamente el tallerista, con la siguiente información: \n")
    print(nuevoTallerista.__dict__())
