import unittest
import requests
import json

class BusquedaTests(unittest.TestCase):
    valid_input = None
    invalid_input = None

    @classmethod
    def setUpClass(cls):
        cls.base_url = "http://127.0.0.1:8000/Busqueda"
        cls.valid_input = "Un taller de pintura para niños"
        cls.invalid_input = ""

    @classmethod
    def tearDownClass(cls):
        del cls.valid_input
        del cls.invalid_input

    def test_busqueda_normal_input(self):

        response = requests.post(url=self.base_url, data=json.dumps({"descripcion" : self.valid_input}))
        response = response.content
        response = json.loads(response)
        self.assertRegex(response["Tema"]["descripcion"],"[ñ*Ñ*á*é*í*ó*ú*Á*É*Í*Ó*Ú*\\*\,*\.*w*\s*]*")
        self.assertEqual("5",response["Duracion"],)
        self.assertEqual(5,response["Cupos"])
        self.assertEqual("NULL",response["Modalidad"])
        self.assertEqual("NULL",response["Fecha"])
        self.assertEqual("NULL",response["Hora"])
        self.assertEqual("NULL",response["Nombre"])
        self.assertEqual("NULL",response["Recinto"])

    def test_busqueda_empty_input(self):

        response = requests.post(url=self.base_url,data=json.dumps({"descripcion" : self.invalid_input}))
        self.assertEqual(400,int(response.content))

if __name__ == '__main__':
    unittest.main()