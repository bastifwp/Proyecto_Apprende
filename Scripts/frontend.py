import streamlit as st
import requests
import json
from sqlalchemy import create_engine,text
import psycopg2
import pandas as pd


#Librerias para los formularios de google
from apiclient import discovery
from httplib2 import Http
from oauth2client.service_account import (ServiceAccountCredentials)
import json #Este creo q no es necesario


st.set_page_config(page_title="Apprende",page_icon="Images/logo.png", layout="wide")


#Conección a base de datos, cambiar con el url correspondiente (postgresql://[usuario]:secret@localhost:5432/[nombre_de_bd])
#engine = create_engine("postgresql://postgres:secret@localhost:5432/app?client_encoding=utf8") 

#Nos conectamos con la base de datos
#try:
con = psycopg2.connect(
    dbname="prueba",
    user="postgres",
    password="bfwp1234",
    host="localhost",
    port="5432",

    client_encoding='utf8'
        )
#print("NOS CONECTAMOS SEÑORES")
#except:
    #print("Failed to connect to database")

#Este cursor es el que nos permite realizar operaciones sql
cur = con.cursor()

#Usuarios, registrarse directamente del script pues no hay registro en el frontend
st.session_state.users = {
    "Scarl3th": "@Leprechaun10",
    "xltn": "ayrton1208"
}

#Inicializamos variables de estado relacionadas a usuario
st.session_state.user = ""
st.session_state.password = ""

#Resetear variables de estado que se activa con button "Reset"
def reset_session_state():
    st.session_state.response = {}
    st.session_state.links = []
    st.session_state.texto = ''
    st.session_state.option = ''
    st.session_state.newName = ''
    st.session_state.name_done = ''
    st.session_state.create_name = False
    st.session_state.talleristas = {}
    st.session_state.saved = []

#Inicializamos variable de estado relacionada a la view
if "page" not in st.session_state:
        st.session_state.page = 'Login'


#Inicializamos variable de estado relacionada con las propuestas
if "show_link_formulario_propuestas" not in st.session_state:
    st.session_state.show_link_formulario_propuestas = False

if "form_link" not in st.session_state:
    st.session_state.form_link = ""


#Implementación de login
if st.session_state.page == 'Login':

    col1, col2, col3 = st.columns(3)

    with col2:

        st.title("Log in")

        username = st.text_input("Username").strip()
        password = st.text_input("Password",type='password').strip()
        
        if st.button('Iniciar Sesión'):
            if username in st.session_state.users and st.session_state.users[username] == password:
                st.session_state.page = 'Buscador'
                st.rerun()
            if st.session_state.user == "":
                st.write("Your username or password is incorrect")

#Menú que se muestra en todas las views menos la de login
else:

    with st.sidebar:
        st.title("Menú")
        if st.button("Buscador",use_container_width = True):
            st.session_state.page = 'Buscador'
        if st.button("Talleristas",use_container_width = True):
            st.session_state.page = 'Talleristas'
        if st.button("Propuestas",use_container_width = True):
            st.session_state.page = 'Propuestas'
        if st.button("Log out",use_container_width = True):
            st.session_state.username = ""
            st.session_state.password = ""
            st.session_state.page = 'Login'
            st.rerun()

#View del buscador
if st.session_state.page == 'Buscador':

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
        if "talleristas" not in st.session_state:
            st.session_state.talleristas = {}
        if "saved" not in st.session_state:
            st.session_state.saved = []

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

                #Response contendrá un taller
                response = processed_input.json()
                st.session_state.response = response

            else:
                st.write("Debe ingresar una descripción")
        
        #Si es que se tiene un taller
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
                

                #Botón para subir el formulario
                if st.form_submit_button("Listo"): 

                        #Acá se guardan los datos del form
                        st.session_state.response = response
                        datos = {
                            "texto" : st.session_state.texto,
                            "tema" : st.session_state.response["Tema"],
                            "nombre" : st.session_state.response["Nombre"]
                        }

                        st.session_state.newName = requests.put(url="http://127.0.0.1:8000/Taller",data=json.dumps(datos))
                        st.session_state.name_done = 'no'
                        
            #Creacion de nombre
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
            
            if st.session_state.name_done == 'si':
                
                st.write("Okey, ", st.session_state.response["Nombre"], "será el nombre de tu taller entonces")
                st.write("En base a la información que me diste, buscaré talleristas que puedan ser de utilidad para su realización :)")

                #Verificamos que no se haya realizado ya la búsqueda
                if st.session_state.links == []:
                    datos = {
                        "tema" : st.session_state.response["Tema"],
                        "modalidad" : st.session_state.response["Modalidad"]
                    }

                    processed_links = requests.post(url="http://127.0.0.1:8000/Respuesta", data=json.dumps(datos))
                    print("Se hará lo de processed_links")
                    links = processed_links.json()
                    print("Se hizo lo de processed_links")
                    st.session_state.links = links["link_talleristas"]


                st.write("Estos son los links a los perfiles que he encontrado:")


                df = st.session_state.talleristas    
                #Verificamos que no se hayan guardado ya los talleristas encontrados
                if st.session_state.talleristas == {}:
                    #Creamos un diccionario con los datos al reves porq asi se muestra más bonito jeje
                    #Ademas agregamos una columna de Guardados donde se guardaran valores booleanos
                    df = {
                        'Nombre':[],
                        'Modalidad':[],
                        'Precio':[],
                        'Tema':[],
                        'Enlace':[],
                        'Fuente':[],
                        'Guardado':[],
                        }
                    for i, link in enumerate(st.session_state.links, start=1):
                        for a in df:
                            if a != 'Guardado':
                                df[a].append(link[a])
                            else:
                                df[a].append(False)
                        st.session_state.saved.append(False)
                    st.session_state.talleristas = df
                    print(df["Guardado"])

                
                #Mostramos datos encontrados además de la casilla de checkboxes
                #Cada vez que se edita una casilla de la columnda de guardados se vuelve a cargar la página
                edited_df = st.data_editor(
                    st.session_state.talleristas,
                    use_container_width=True,
                    column_config={
                        "Guardado": st.column_config.CheckboxColumn(
                            "Guardar",
                            help="Seleccionar checkbox para guardar",
                            default=False
                        )
                    },
                    disabled=["Nombre","Modalidad","Precio","Tema","Enlace","Fuente"],
                    hide_index=True
                    #on_change=st.rerun()
                )
                #Esto es para que no se buguee
                if not edited_df == st.session_state.talleristas:
                    st.session_state.talleristas = edited_df
                    st.rerun()


                #Buscamos si hubo algún cambio en las checkbox y actualizamos base de datos
                i=0 #index auxiliar, nos ayudara a saber a que tallerista nos referimos
                for a in st.session_state.talleristas['Guardado']: #Recorremos lista 'Guardados' de df, 'a' es un valor booleano
                    if a != st.session_state.saved[i]: #Si el valor cambió
                        st.session_state.saved[i] = a
                        if a == True: #Si esta la checkbox marcada, guardamos en bd
                            q = ''
                            for b in st.session_state.talleristas:
                                if q != '':
                                    if isinstance(st.session_state.talleristas[b][i],str):
                                        q += ", '"+(st.session_state.talleristas[b][i])+"'"
                                    else:
                                        print(st.session_state.talleristas[b][i],'is not str')
                                        q += ", "+str(st.session_state.talleristas[b][i])
                                else:
                                    q = 'INSERT INTO talleristas (Nombre,Modalidad,Precio,Tema,Enlace,Fuente,Guardado) VALUES ('
                                    q += "'"+st.session_state.talleristas[b][i]+"'"
                            q += ");"
                            
                            print("\n \n Esto es q: ", q, "\n \n")
                            #with engine.connect() as con:

                                #Le puse esto
                            #    with con.begin():
                            #        print(q)


                            cur.execute(q)
                            con.commit()
                      

                        else: #Si a == False
                            q = "DELETE FROM Talleristas WHERE Enlace = '"+st.session_state.talleristas['Enlace'][i]+"';"
                            #with engine.connect() as con:

                                #with con.begin():
                                    #print(q)
                          
                            cur.execute(q)
                            con.commit()

                       

                    i += 1 #Actualizamos index


    if st.button("Reiniciar"): 
        reset_session_state()
        st.experimental_rerun()

#View de Talleristas guardados
elif st.session_state.page == 'Talleristas':

    st.title('Talleristas')

    cur.execute("SELECT * FROM talleristas;")

    struct = {
        "ID": [],
        "Nombre": [],
        "Modalidad": [],
        "Precio": [],
        "Temas": [],
        "Enlace": [],
        "Fuente": [],
        "Guardado": []
    }
    tdf = cur.fetchall()
    for a in tdf:
        struct["ID"].append(a[0])
        struct["Nombre"].append(a[1])
        struct["Modalidad"].append(a[2])
        struct["Precio"].append(a[3])
        struct["Temas"].append(a[4])
        struct["Enlace"].append(a[5])
        struct["Fuente"].append(a[6])
        struct["Guardado"].append(a[7])
        
                
    print("SE realizo un SELECT")
    print("EL TDF ES ESTE: ", tdf)
    st.dataframe(struct ,hide_index=True)

#View de Propuestas de taller escritas por talleristas
elif st.session_state.page == 'Propuestas':
    st.title('Propuestas')

    #Botón para generar formulario
    if st.button("Generar link de formulario"):
        st.session_state.show_link_formulario_propuestas = True

        #Generamos el formulario:

        #Cosas de google xd
        SCOPES = "https://www.googleapis.com/auth/forms.body"
        DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"
    
        #Credenciales para autenticarse
        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', SCOPES)

        #Se lo enviamos a google para que nos autentique y tener un cliente http autenticado
        http = creds.authorize(Http())

        #Ahora creamos interfaz con la que interactuaremos con la api de google
        form_service = discovery.build(
            'forms',
            'v1',
            http=http,
            discoveryServiceUrl=DISCOVERY_DOC,
            static_discovery=False
        )

        #Creamos plantilla de formulario vacío
        NEW_FORM = {
            "info":{
                "title" : "Propuesta de clase",
            }
        }

        #Creamos cada pregunta por separado y despues las insertamos en el formulario
        first_question = {
            "requests": [{
                "createItem" : {
                    "item" : {
                        "title" : "Cuéntanos sobre ti",
                        "questionItem" : {
                            "question" : {
                                "required" : True,
                                "textQuestion" : {
                                "paragraph": True
                                }
                            }
                        },
                    },
                    
                "location": {
                        "index": 0
                    }
                },
            }]
        }


        second_question = {
            "requests": [{
                "createItem" : {
                    "item" : {
                        "title" : "Descripción de tu clase",
                        "questionItem" : {
                            "question" : {
                                "required" : True,
                                "textQuestion" : {
                                "paragraph": True
                                }
                            }
                        },
                    },
                    
                "location": {
                        "index": 1
                    }
                },
            }]
        }

        third_question = {
            "requests": [{
                "createItem" : {
                    "item" : {
                        "title" : "Cantidad de personas",
                        "questionItem" : {
                            "question" : {
                                "required" : True,
                                "choiceQuestion" : {
                                    "type": "RADIO",
                                    "options":[
                                        {
                                            "value": "[1-5]"
                                        },

                                        {
                                            "value": "[5-10]"
                                        },

                                        {
                                            "value": "[10-15]"
                                        },

                                        {
                                            "value": "[15-20]"
                                        },

                                        {
                                            "value": "[20-30]"
                                        },

                                        {
                                            "value": "[30-50]"
                                        },                       

                                    ],
                                    "shuffle": False
                                }
                            }
                        },
                    },
                    
                "location": {
                        "index": 2
                    }
                },
            }]

        }

        #Ahora inicializamos formulario vacío
        result = form_service.forms().create(body = NEW_FORM).execute()

        #Ahora metemos las preguntas
        question_setting = form_service.forms().batchUpdate(formId=result["formId"], body = first_question).execute()
        question_setting = form_service.forms().batchUpdate(formId=result["formId"], body = second_question).execute()
        question_setting = form_service.forms().batchUpdate(formId=result["formId"], body = third_question).execute()

        #Podemos obtener el formulario creado
        get_result = form_service.forms().get(formId = result["formId"]).execute()

        form_url = form_service.forms().get(formId = result["formId"]).execute()["responderUri"]

        st.session_state.form_link = form_url

        #Comprobamos si se creó
        print(json.dumps(get_result, indent=4))

    if st.session_state.show_link_formulario_propuestas:
        st.write(st.session_state.form_link)