import unittest
import requests
import json
import re

class RespuestaTests(unittest.TestCase):
    valid_input = None
    invalid_input = None

    @classmethod
    def setUpClass(cls):
        cls.base_url = "http://127.0.0.1:8000/Respuesta"
        cls.valid_input = {
            "tema": "taller de música clásica",
            "modalidad": "Presencial"
        } #Aqui poner un input que se considere normal
        cls.invalid_input = {
            "tema": "",
            "modalidad": "Presencial"
        } #Aqui poner un input que se considere malo

    @classmethod
    def tearDownClass(cls):
        del cls.valid_input
        del cls.invalid_input

    def test_respuesta_normal_input(self):

        response = requests.post(url=self.base_url, data=json.dumps(self.valid_input))
        links = response.json()
        for item in links["link_talleristas"]: #capaz me fui un pokito a la cresta ns XD
            self.assertIn("Nombre", item)
            self.assertRegex(item["Nombre"],r'[\w\s,ÁÉÍÓÚáéíóúÑñ]+')

            self.assertIn("Modalidad", item)
            self.assertTrue(item["Modalidad"]=='Presencial' or item["Modalidad"]=='Online' or item["Modalidad"]=='Presencial, Online' or item["Modalidad"]=='Online, Presencial')

            self.assertIn("Precio", item)
            self.assertRegex(item["Precio"],r'^\$\d+(.\d{3})*$')

            self.assertIn("Tema", item)
            self.assertRegex(item["Tema"],r'[\w\s,ÁÉÍÓÚáéíóúÑñ]+')

            self.assertIn("Enlace", item)
            self.assertTrue(re.fullmatch(r"((https://)?www\.)?superprof\.cl/.*", item["Enlace"]) or re.fullmatch(r"((https://)?www\.)?tusclasesparticulares\.cl/.*", item["Enlace"])) #ns si jugárnosla tanto XD

            self.assertIn("Fuente", item)
            self.assertTrue(item["Fuente"]=='superprof' or item["Fuente"]=='tusclasesparticulares')


    def test_respuesta_empty_input(self): 

        response = requests.post(url=self.base_url,data=json.dumps(self.invalid_input))
        self.assertEqual(400,int(response.content)) #Confirmar si response es lo que debe ser con metodos assert (estan en el sv de discord)

#Esto debe ir para poder ejecutar los tests
if __name__ == '__main__':
    unittest.main()
