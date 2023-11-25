import streamlit as st
import requests
import json

st.set_page_config(page_title="Apprende",page_icon="Images/logo.png", layout="wide")

#Resetear variables de estado que se activa con button "Reset"
def reset_session_state():
    st.session_state.response = {}
    st.session_state.links = []
    st.session_state.texto = ''
    st.session_state.option = ''
    st.session_state.newName = ''
    st.session_state.name_done = ''
    st.session_state.create_name = False
    st.session_state.tallerista = {}

#No las usamos ahora
def get_attributes1(response):
    newResponse = response
    with st.form(key="1"):
        newResponse["Tema"] = st.text_input("¿De que te gustaría que se tratase el taller?")
        newResponse["Duracion"] = st.slider("Muy bien, ¿Cuánto tiempo tienes planeado que dure el taller?",0.0,12.0)
        newResponse["Cupos"] = st.slider("¿Y para cuantas personas tienes pensado que sea el taller?",0,100)
        newResponse["Modalidad"] = st.selectbox("¿En qué modalidad te gustaría que se realizace el taller?",["Presencial","Online"])
        newResponse["Fecha"] = st.date_input("¿Y en que fecha se realizaría este taller?", value=None)
        newResponse["Hora"] = st.time_input("¿A qué hora comenzaría el taller?")
        newResponse["Recinto"] = st.selectbox("¿En donde se realizará el taller?",["Oficinas Apprende","USM Casa Central","USM Sede San Joaquín","USM Sede Viña del Mar", "USM Sede Vitacura", "USM Sede Concepción"])
        st.session_state.response = newResponse
        st.form_submit_button("Listo")
        
    return newResponse

def get_attributes2(response):
    newResponse = response
    with st.form(key="2"):
        newResponse["Duracion"] = st.slider("Muy bien, ¿Cuánto tiempo tienes planeado que dure el taller?",0.0,12.0)
        newResponse["Cupos"] = st.slider("¿Y para cuantas personas tienes pensado que sea el taller?",0,100)
        newResponse["Modalidad"] = st.selectbox("¿En qué modalidad te gustaría que se realizace el taller?",["Presencial","Online"])
        newResponse["Fecha"] = st.date_input("¿Y en que fecha se realizaría este taller?", value=None)
        newResponse["Hora"] = st.time_input("¿A qué hora comenzaría el taller?")
        newResponse["Recinto"] = st.selectbox("¿En donde se realizará el taller?",["Oficinas Apprende","USM Casa Central","USM Sede San Joaquín","USM Sede Viña del Mar", "USM Sede Vitacura", "USM Sede Concepción"])
        st.session_state.response = newResponse
        st.form_submit_button("Listo")
    return newResponse

def get_attributes3(response):
    newResponse = response
    with st.form(key="3"):
        newResponse["Cupos"] = st.slider("¿Y para cuantas personas tienes pensado que sea el taller?",0,100)
        newResponse["Modalidad"] = st.selectbox("¿En qué modalidad te gustaría que se realizace el taller?",["Presencial","Online"])
        newResponse["Fecha"] = st.date_input("¿Y en que fecha se realizaría este taller?", value=None)
        newResponse["Hora"] = st.time_input("¿A qué hora comenzaría el taller?")
        newResponse["Recinto"] = st.selectbox("¿En donde se realizará el taller?",["Oficinas Apprende","USM Casa Central","USM Sede San Joaquín","USM Sede Viña del Mar", "USM Sede Vitacura", "USM Sede Concepción"])
        st.session_state.response = newResponse
        st.form_submit_button("Listo")
    return newResponse

def get_attributes4(response):
    newResponse = response
    with st.form(key="4"):
        newResponse["Duracion"] = st.slider("Muy bien, ¿Cuánto tiempo tienes planeado que dure el taller?",0.0,12.0)
        newResponse["Modalidad"] = st.selectbox("¿En qué modalidad te gustaría que se realizace el taller?",["Presencial","Online"])
        newResponse["Fecha"] = st.date_input("¿Y en que fecha se realizaría este taller?", value=None)
        newResponse["Hora"] = st.time_input("¿A qué hora comenzaría el taller?")
        newResponse["Recinto"] = st.selectbox("¿En donde se realizará el taller?",["Oficinas Apprende","USM Casa Central","USM Sede San Joaquín","USM Sede Viña del Mar", "USM Sede Vitacura", "USM Sede Concepción"])
        st.session_state.response = newResponse
        st.form_submit_button("Listo")
    return newResponse

def get_attributes5(response):
    newResponse = response
    with st.form(key="5"):
        newResponse["Modalidad"] = st.selectbox("¿En qué modalidad te gustaría que se realizace el taller?",["Presencial","Online"])
        newResponse["Fecha"] = st.date_input("¿Y en que fecha se realizaría este taller?", value=None)
        newResponse["Hora"] = st.time_input("¿A qué hora comenzaría el taller?")
        newResponse["Recinto"] = st.selectbox("¿En donde se realizará el taller?",["Oficinas Apprende","USM Casa Central","USM Sede San Joaquín","USM Sede Viña del Mar", "USM Sede Vitacura", "USM Sede Concepción"])
        st.session_state.response = newResponse
        st.form_submit_button("Listo")
    return newResponse


#Desde aquí si se usa

with st.container():

    #Inicializamos los sesion_state para guardar datos
    if "response" not in st.session_state:
        st.session_state.response = {}
    if "links" not in st.session_state:
        st.session_state.links = []
    if "texto" not in st.session_state:
        st.session_state.texto = ''
    if "option" not in st.session_state:
        st.session_state.option = ''
    if "newName" not in st.session_state:
        st.session_state.newName = ''
    if "name_done" not in st.session_state:
        st.session_state.name_done = ''
    if "create_name" not in st.session_state:
        st.session_state.create_name = False
    if "tallerista" not in st.session_state:
        st.session_state.tallerista = {}

    #Texto para presentar la página
    st.subheader("Organizador de talleres de Apprende")
    st.title("Hola!")
    st.write("Estoy aquí para ayudarte a organizar un nuevo taller :)")
   
    texto = st.text_input("¿Qué tipo de taller te gustaría realizar?")
    response = st.session_state.response
    links = st.session_state.links
            



    if st.button("Enviar") and response == {}:
        
        #Verificamos que haya proporcionado alguna descripción
        if texto != "":
            input = {"descripcion" : texto}
            st.session_state.texto = texto
            processed_input = requests.post(url="http://127.0.0.1:8000/Busqueda", data=json.dumps(input))
            #st.write(f"Respuesta de API = {processed_input.text}")
            response = processed_input.json()
            st.session_state.response = response

        else:
            st.write("Debe ingresar una descripción")
        
    if response != {}:
        
        with st.form(key="main_form"):
            
            #Pediremos los datos para el taller, en caso de que chatgpt haya identificado algunos se da la oportunidad de cambiarlos
            #TEMA DEL TALLER
            if response["Tema"] == "NULL":
                response["Tema"] = st.text_input("¿De qué te gustaría que se tratase el taller?")
            else:
                response["Tema"] = st.text_input("¿De qué te gustaría que se tratase el taller? (la búsqueda de talleristas se basa en el tema del taller)", value=response["Tema"])
            
            #DURACIÓN DEL TALLER
            if response["Duracion"] == "NULL":
                response["Duracion"] = st.slider("¿Cuántas horas tienes planeado que dure el taller?",min_value=0.0, max_value =12.0, value=0.0)
                #st.write(response["Duracion"])
            else:
                response["Duracion"] = st.slider("¿Cuántas horas tienes planeado que dure el taller?",min_value=0.0, max_value=12.0, value= float(response["Duracion"]))

            #CUPOS DEL TALLER
            if response["Cupos"] == "NULL":
                response["Cupos"] = st.slider("¿Para cuántas personas tienes pensado que sea el taller?",min_value=0, max_value=50, step=1, value=0)
            else:
                response["Cupos"] = st.slider("¿Para cuántas personas tienes pensado que sea el taller?",min_value=0, max_value=50, step=1, value=int(response["Cupos"]))
            
            response["Modalidad"] = st.selectbox("¿En qué modalidad te gustaría que se realizace el taller?",["Presencial","Online"])
            response["Fecha"] = st.date_input("¿Y en que fecha se realizaría este taller?", value=None)
            response["Hora"] = st.time_input("¿A qué hora comenzaría el taller?")
            response["Recinto"] = st.selectbox("¿En donde se realizará el taller?",["Oficinas Apprende","USM Casa Central","USM Sede San Joaquín","USM Sede Viña del Mar", "USM Sede Vitacura", "USM Sede Concepción"])
            

            if  st.form_submit_button("Listo"): 

                    #Acá se guardan los datos del form
                    st.session_state.response = response
                    datos = {
                        "texto" : st.session_state.texto,
                        "tema" : st.session_state.response["Tema"],
                        "nombre" : st.session_state.response["Nombre"]
                    }
                    st.session_state.newName = requests.put(url="http://127.0.0.1:8000/Taller",data=json.dumps(datos))
                    st.session_state.name_done = 'no'
                    
        #st.write("Se me ocurre que tu taller podría llamarse ", st.session_state.newName, " ¿Te gusta este nombre?")
        if st.session_state.newName != '' and st.session_state.name_done == 'no' and st.session_state.create_name == False:
            st.write("Se me ocurre que tu taller podría llamarse ", st.session_state.newName.text, " ¿Te gusta este nombre?")
            if st.button("Si, utilizaré ese nombre"):
                st.session_state.response["Nombre"] = st.session_state.newName.text
                st.session_state.name_done = 'si'
            elif st.button("No mucho, ¿Puedes inventar otro?"):
                datos = {
                    "texto" : st.session_state.texto,
                    "tema" : st.session_state.response["Tema"],
                    "nombre" : st.session_state.newName.text
                }
                st.session_state.newName = requests.put(url="http://127.0.0.1:8000/Taller",data=json.dumps(datos))
                st.rerun()
            elif st.button("Prefiero inventar un nombre yo mism@"):
                st.session_state.create_name = True

        if st.session_state.create_name:
            with st.form(key="name_ready"):
                response["Nombre"] = st.text_input("Ingresa el nombre de tu taller")

                if st.form_submit_button("Nombre listo"):
                    st.session_state.response["Nombre"] = response["Nombre"]
                    st.session_state.name_done = 'si'

        #st.write(st.session_state.name_done)
        
        if st.session_state.name_done == 'si':

            st.write("Okey, ", st.session_state.response["Nombre"], "será el nombre de tu taller entonces")
            st.write("En base a la información que me diste, buscaré talleristas que puedan ser de utilidad para su realización :)")

            datos = {
                "tema" : st.session_state.response["Tema"],
                "modalidad" : st.session_state.response["Modalidad"]
            }

            processed_links = requests.post(url="http://127.0.0.1:8000/Respuesta", data=json.dumps(datos))
            links = processed_links.json()
            #st.write(links)
            st.session_state.links = links["link_talleristas"]


            st.write("Estos son los links a los perfiles que he encontrado:")
            for i, link in enumerate(st.session_state.links, start=1):
                st.write(f"{i}. {link}")


            
            with st.form(key="Tallerista"):
                st.write("Rellena esta información sobre el tallersita escogido (si la hay):")
                st.session_state.tallerista["option"] = st.number_input("Escoge el link del tallerista que más te gustó", 1,len(st.session_state.links))
                st.session_state.tallerista["nombre"] = st.text_input("Ingresa el nombre del tallerista")
                st.session_state.tallerista["email"] = st.text_input("Ingresa el email del tallerista")
                st.session_state.tallerista["numero"] = st.text_input("Ingresa el número de teléfono del tallerista")

                #Mostramos la información del taller y el tallerista a cargo al apretar el botón hecho
                if st.form_submit_button("Hecho"):
                    st.write('El taller "',st.session_state.response["Nombre"],'" ha sido creado con la siguiente información: ')
                    st.write("Temática: ",st.session_state.response["Tema"])
                    st.write("Duración: ",st.session_state.response["Duracion"])
                    st.write("Cupos: ",st.session_state.response["Cupos"])
                    st.write("Modalidad: ",st.session_state.response["Modalidad"])
                    st.write("Fecha: ",st.session_state.response["Fecha"])
                    st.write("Hora: ",st.session_state.response["Hora"])
                    st.write("Recinto: ",st.session_state.response["Recinto"])
                    st.write('---')
                    st.write("Y el tallerista a cargo de realizarlo será ",st.session_state.tallerista["nombre"])
                    st.write("Numero: ",st.session_state.tallerista["numero"])
                    st.write("Email: ",st.session_state.tallerista["email"])


if st.button("Reiniciar"): 
    reset_session_state()
    st.experimental_rerun()