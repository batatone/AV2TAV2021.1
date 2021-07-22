from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest
from unittest import mock
import requests

import App


class Tests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe")
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
        App.tabgen()

    def test_prontuario_cadastrado_i(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        driver.find_element_by_id("opaddcli").click()
        driver.find_element_by_id("cliaddnome").clear()
        driver.find_element_by_id("cliaddnome").send_keys("Carlos")
        driver.find_element_by_id("cliaddcpf").clear()
        driver.find_element_by_id("cliaddcpf").send_keys("12345678911")
        driver.find_element_by_id("templano2").click()
        driver.find_element_by_id("cliaddnomep").clear()
        driver.find_element_by_id("cliaddnomep").send_keys("Unimed")
        driver.find_element_by_id("cliaddtipop").clear()
        driver.find_element_by_id("cliaddtipop").send_keys("Teste")
        driver.find_element_by_id("cliaddultcon").clear()
        driver.find_element_by_id("cliaddultcon").send_keys("2021-07-31")
        driver.find_element_by_id("cliaddpront").clear()
        driver.find_element_by_id("cliaddpront").send_keys("1")
        driver.find_element_by_id("cliaddnasc").clear()
        driver.find_element_by_id("cliaddnasc").send_keys("2021-06-27")
        driver.find_element_by_id("dependente2").click()
        driver.find_element_by_id("subaddcli").click()
        self.assertEqual("Prontuário já cadastrado", driver.find_element_by_id("flashcliente").text)

    def test_cpf_cadastrado_i(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        driver.find_element_by_id("opaddcli").click()
        driver.find_element_by_id("cliaddnome").clear()
        driver.find_element_by_id("cliaddnome").send_keys("Carlos")
        driver.find_element_by_id("cliaddcpf").clear()
        driver.find_element_by_id("cliaddcpf").send_keys("12345678910")
        driver.find_element_by_id("templano2").click()
        driver.find_element_by_id("cliaddnomep").clear()
        driver.find_element_by_id("cliaddnomep").send_keys("Unimed")
        driver.find_element_by_id("cliaddtipop").clear()
        driver.find_element_by_id("cliaddtipop").send_keys("Teste")
        driver.find_element_by_id("cliaddultcon").clear()
        driver.find_element_by_id("cliaddultcon").send_keys("2021-07-31")
        driver.find_element_by_id("cliaddpront").clear()
        driver.find_element_by_id("cliaddpront").send_keys("8")
        driver.find_element_by_id("cliaddnasc").clear()
        driver.find_element_by_id("cliaddnasc").send_keys("2021-06-27")
        driver.find_element_by_id("dependente2").click()
        driver.find_element_by_id("subaddcli").click()
        self.assertEqual("CPF já cadastrado", driver.find_element_by_id("flashcliente").text)

    def test_busca_ok(self) :
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        driver.find_element_by_id("maglass").click()
        driver.find_element_by_id("CPF").clear()
        driver.find_element_by_id("CPF").send_keys("12345678910")
        driver.find_element_by_id("busca").click()
        self.assertEqual("12345678910", driver.find_element_by_id("pageclicpf").text)

    def test_cliente_page(self) :
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        cpf = driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='Ações'])[1]/following::td[2]").text
        driver.find_element_by_link_text("Carlos").click()
        self.assertEqual(cpf, driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Dependente'])[1]/following::td[2]").text)

    def test_dados_plano_invalidos_e(self) :
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        driver.find_element_by_id("opedcli1").click()
        driver.find_element_by_id("templano4").click()
        driver.find_element_by_id("cliednomep").clear()
        driver.find_element_by_id("cliednomep").send_keys("Particular")
        driver.find_element_by_id("cliedtipop").clear()
        driver.find_element_by_id("cliedtipop").send_keys("Pagar inteiro")
        driver.find_element_by_id("subedcli").click()
        self.assertEqual(u"Especiifique corretamente os dados do plano de saúde",
                         driver.find_element_by_id("flashcliente").text)

    def test_prontuario_invalido_e(self) :
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        driver.find_element_by_id("opedcli1").click()
        driver.find_element_by_id("cliedpront").clear()
        driver.find_element_by_id("cliedpront").send_keys("12346126612461614236614646236")
        driver.find_element_by_id("subedcli").click()
        self.assertEqual(u"Prontuário Inválido", driver.find_element_by_id("flashcliente").text)

    def test_cpf_grande_e(self) :
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        driver.find_element_by_id("opedcli1").click()
        driver.find_element_by_id("cliednome").click()
        driver.find_element_by_id("cliedcpf").click()
        driver.find_element_by_id("cliedcpf").clear()
        driver.find_element_by_id("cliedcpf").send_keys("1234567891011")
        driver.find_element_by_id("subedcli").click()
        self.assertEqual(u"CPF Inválido (Longo demais)", driver.find_element_by_id("flashcliente").text)

    def test_cpf_pequeno_e(self) :
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        driver.find_element_by_id("opedcli1").click()
        driver.find_element_by_id("cliednome").click()
        driver.find_element_by_id("cliedcpf").click()
        driver.find_element_by_id("cliedcpf").clear()
        driver.find_element_by_id("cliedcpf").send_keys("123456789")
        driver.find_element_by_id("subedcli").click()
        self.assertEqual(u"CPF Inválido (Curto demais)", driver.find_element_by_id("flashcliente").text)

    def test_multiplos_erros_e(self) :
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        driver.find_element_by_id("opedcli1").click()
        driver.find_element_by_id("cliedcpf").click()
        driver.find_element_by_id("cliedcpf").clear()
        driver.find_element_by_id("cliedcpf").send_keys("1234567891035351")
        driver.find_element_by_id("cliedpront").click()
        driver.find_element_by_id("cliedpront").clear()
        driver.find_element_by_id("cliedpront").send_keys("114613466356235717137134723571771")
        driver.find_element_by_id("subedcli").click()
        self.assertEqual(u"Múltiplos erros, envio cancelado", driver.find_element_by_id("flashcliente").text)

    def test_delete_cli(self) :
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        self.accept_next_alert = True
        driver.find_element_by_id("deletcli2").click()
        self.assertRegexpMatches(self.close_alert_and_get_its_text(), r"^Deseja mesmo deletar[\s\S]$")
        self.assertEqual("Cliente removido :(", driver.find_element_by_id("flashcliente").text)

    def test_edit_id_invalido(self) :
        driver = self.driver
        driver.get("http://127.0.0.1:5000/dentista")
        driver.find_element_by_id("opedorc1").click()
        driver.find_element_by_id("orcedident").clear()
        driver.find_element_by_id("orcedident").send_keys("14124123723572372382488268234")
        Select(driver.find_element_by_id("idpa")).select_by_visible_text("4")
        driver.find_element_by_id("subedorc").click()
        self.assertEqual("ID de Dentista Inválido", driver.find_element_by_id("flashorca").text)

    def test_delete_orc(self) :
        driver = self.driver
        driver.get("http://127.0.0.1:5000/dentista")
        self.accept_next_alert = True
        driver.find_element_by_id("delorc2").click()
        self.assertRegexpMatches(self.close_alert_and_get_its_text(), r"^Deseja mesmo deletar[\s\S]$")
        self.assertEqual(u"Orçamento removido :(", driver.find_element_by_id("flashorca").text)

    def mocked_requests_get(*args, **kwargs) :
        class MockResponse():
            def __init__(self, json_data, status_code) :
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        if args[0] == f"http://localhost:3002/api/planosaude?idped=1" :
            return MockResponse([{"idped":"3","status":"Negado","motivo":"Joguei a moeda pro alto e deu coroa","dataped":"2021-07-09","datares":"2021-07-09","id":"L019zssCdHIaoxLz"},
  {"idped":"2","status":"Aceito","motivo":"Joguei a moeda pro alto e deu cara","dataped":"2021-07-09","datares":"2021-07-09","id":"Mzaf75Y38VGpckYm"},
  {"idped":"4","status":"Negado","motivo":"Joguei a moeda pro alto e deu coroa","dataped":"2021-07-09","datares":"2021-07-09","id":"NTy6A4h19jWqylHJ"},
  {"idped":"5","status":"Aceito","motivo":"Joguei a moeda pro alto e deu cara","dataped":"2021-07-09","datares":"2021-07-09","id":"UFNQbRvhCp19h5tN"},
  {"idped":"1","status":"Negado","motivo":"Joguei a moeda pro alto e deu coroa","dataped":"2021-07-09","datares":"2021-07-09","id":"hPCS704pKQilJqt0"}], 200)
        elif args[0] == f"http://localhost:3002/api/planosaude?idped=2":
            return MockResponse([{"idped":"3","status":"Negado","motivo":"Joguei a moeda pro alto e deu coroa","dataped":"2021-07-09","datares":"2021-07-09","id":"L019zssCdHIaoxLz"},
  {"idped":"2","status":"Aceito","motivo":"Joguei a moeda pro alto e deu cara","dataped":"2021-07-09","datares":"2021-07-09","id":"Mzaf75Y38VGpckYm"},
  {"idped":"4","status":"Negado","motivo":"Joguei a moeda pro alto e deu coroa","dataped":"2021-07-09","datares":"2021-07-09","id":"NTy6A4h19jWqylHJ"},
  {"idped":"5","status":"Aceito","motivo":"Joguei a moeda pro alto e deu cara","dataped":"2021-07-09","datares":"2021-07-09","id":"UFNQbRvhCp19h5tN"},
  {"idped":"1","status":"Negado","motivo":"Joguei a moeda pro alto e deu coroa","dataped":"2021-07-09","datares":"2021-07-09","id":"hPCS704pKQilJqt0"}], 200)
        elif args[0] == f"http://localhost:3002/api/planosaude?idped=3":
            return MockResponse([{"idped":"3","status":"Negado","motivo":"Joguei a moeda pro alto e deu coroa","dataped":"2021-07-09","datares":"2021-07-09","id":"L019zssCdHIaoxLz"},
  {"idped":"2","status":"Aceito","motivo":"Joguei a moeda pro alto e deu cara","dataped":"2021-07-09","datares":"2021-07-09","id":"Mzaf75Y38VGpckYm"},
  {"idped":"4","status":"Negado","motivo":"Joguei a moeda pro alto e deu coroa","dataped":"2021-07-09","datares":"2021-07-09","id":"NTy6A4h19jWqylHJ"},
  {"idped":"5","status":"Aceito","motivo":"Joguei a moeda pro alto e deu cara","dataped":"2021-07-09","datares":"2021-07-09","id":"UFNQbRvhCp19h5tN"},
  {"idped":"1","status":"Negado","motivo":"Joguei a moeda pro alto e deu coroa","dataped":"2021-07-09","datares":"2021-07-09","id":"hPCS704pKQilJqt0"}], 200)
        elif args[0] == f"http://localhost:3002/api/planosaude?idped=4":
            return MockResponse([{"idped":"3","status":"Negado","motivo":"Joguei a moeda pro alto e deu coroa","dataped":"2021-07-09","datares":"2021-07-09","id":"L019zssCdHIaoxLz"},
  {"idped":"2","status":"Aceito","motivo":"Joguei a moeda pro alto e deu cara","dataped":"2021-07-09","datares":"2021-07-09","id":"Mzaf75Y38VGpckYm"},
  {"idped":"4","status":"Negado","motivo":"Joguei a moeda pro alto e deu coroa","dataped":"2021-07-09","datares":"2021-07-09","id":"NTy6A4h19jWqylHJ"},
  {"idped":"5","status":"Aceito","motivo":"Joguei a moeda pro alto e deu cara","dataped":"2021-07-09","datares":"2021-07-09","id":"UFNQbRvhCp19h5tN"},
  {"idped":"1","status":"Negado","motivo":"Joguei a moeda pro alto e deu coroa","dataped":"2021-07-09","datares":"2021-07-09","id":"hPCS704pKQilJqt0"}], 200)
        elif args[0] == f"http://localhost:3002/api/planosaude?idped=5":
            return MockResponse([{"idped":"3","status":"Negado","motivo":"Joguei a moeda pro alto e deu coroa","dataped":"2021-07-09","datares":"2021-07-09","id":"L019zssCdHIaoxLz"},
  {"idped":"2","status":"Aceito","motivo":"Joguei a moeda pro alto e deu cara","dataped":"2021-07-09","datares":"2021-07-09","id":"Mzaf75Y38VGpckYm"},
  {"idped":"4","status":"Negado","motivo":"Joguei a moeda pro alto e deu coroa","dataped":"2021-07-09","datares":"2021-07-09","id":"NTy6A4h19jWqylHJ"},
  {"idped":"5","status":"Aceito","motivo":"Joguei a moeda pro alto e deu cara","dataped":"2021-07-09","datares":"2021-07-09","id":"UFNQbRvhCp19h5tN"},
  {"idped":"1","status":"Negado","motivo":"Joguei a moeda pro alto e deu coroa","dataped":"2021-07-09","datares":"2021-07-09","id":"hPCS704pKQilJqt0"}], 200)
        elif args[0] == f"http://localhost:3002/api/planosaude":
            return MockResponse([{"idped" : "3", "status" : "Negado", "motivo" : "Joguei a moeda pro alto e deu coroa",
                                  "dataped" : "2021-07-09", "datares" : "2021-07-09", "id" : "L019zssCdHIaoxLz"},
                                 {"idped" : "2", "status" : "Aceito", "motivo" : "Joguei a moeda pro alto e deu cara",
                                  "dataped" : "2021-07-09", "datares" : "2021-07-09", "id" : "Mzaf75Y38VGpckYm"},
                                 {"idped" : "4", "status" : "Negado", "motivo" : "Joguei a moeda pro alto e deu coroa",
                                  "dataped" : "2021-07-09", "datares" : "2021-07-09", "id" : "NTy6A4h19jWqylHJ"},
                                 {"idped" : "5", "status" : "Aceito", "motivo" : "Joguei a moeda pro alto e deu cara",
                                  "dataped" : "2021-07-09", "datares" : "2021-07-09", "id" : "UFNQbRvhCp19h5tN"},
                                 {"idped" : "1", "status" : "Negado", "motivo" : "Joguei a moeda pro alto e deu coroa",
                                  "dataped" : "2021-07-09", "datares" : "2021-07-09", "id" : "hPCS704pKQilJqt0"}], 200)

        return MockResponse(None, 404)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_api_busca_ok(self, mock_get):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/dentista")
        driver.find_element_by_id("x").clear()
        driver.find_element_by_id("x").send_keys("1")
        driver.find_element_by_id("send").click()
        self.assertEqual("Pedido 1", driver.find_element_by_id("pedidosolo").text)
        self.assertEqual("1", driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Data da Resposta'])[1]/following::td[1]").text)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_api_todos_ok(self, mock_get) :
        driver = self.driver
        driver.get("http://127.0.0.1:5000/dentista")
        driver.find_element_by_id("getall").click()
        self.assertEqual("todos", driver.find_element_by_id("allofthem").text)

    def test_dados_plano_invalidos_i(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        driver.find_element_by_id("opaddcli").click()
        driver.find_element_by_id("cliaddnome").clear()
        driver.find_element_by_id("cliaddnome").send_keys("Carlos")
        driver.find_element_by_id("cliaddcpf").clear()
        driver.find_element_by_id("cliaddcpf").send_keys("12345678911")
        driver.find_element_by_id("templano2").click()
        driver.find_element_by_id("cliaddnomep").clear()
        driver.find_element_by_id("cliaddnomep").send_keys("Particular")
        driver.find_element_by_id("cliaddtipop").clear()
        driver.find_element_by_id("cliaddtipop").send_keys("Teste")
        driver.find_element_by_id("cliaddultcon").clear()
        driver.find_element_by_id("cliaddultcon").send_keys("2021-07-31")
        driver.find_element_by_id("cliaddpront").clear()
        driver.find_element_by_id("cliaddpront").send_keys("6")
        driver.find_element_by_id("cliaddnasc").clear()
        driver.find_element_by_id("cliaddnasc").send_keys("2021-06-27")
        driver.find_element_by_id("dependente2").click()
        driver.find_element_by_id("subaddcli").click()
        self.assertEqual("Especiifique corretamente os dados do plano de saúde",
                         driver.find_element_by_id("flashcliente").text)

    def test_multiplos_erros_i(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        driver.find_element_by_id("opaddcli").click()
        driver.find_element_by_id("cliaddnome").clear()
        driver.find_element_by_id("cliaddnome").send_keys("Carlos")
        driver.find_element_by_id("cliaddcpf").clear()
        driver.find_element_by_id("cliaddcpf").send_keys("1234567891011")
        driver.find_element_by_id("templano2").click()
        driver.find_element_by_id("cliaddnomep").clear()
        driver.find_element_by_id("cliaddnomep").send_keys("Unimed")
        driver.find_element_by_id("cliaddtipop").clear()
        driver.find_element_by_id("cliaddtipop").send_keys("Teste")
        driver.find_element_by_id("cliaddultcon").clear()
        driver.find_element_by_id("cliaddultcon").send_keys("2021-07-31")
        driver.find_element_by_id("cliaddpront").clear()
        driver.find_element_by_id("cliaddpront").send_keys("-1")
        driver.find_element_by_id("cliaddnasc").clear()
        driver.find_element_by_id("cliaddnasc").send_keys("2021-06-27")
        driver.find_element_by_id("dependente2").click()
        driver.find_element_by_id("subaddcli").click()
        self.assertEqual("Múltiplos erros, envio cancelado", driver.find_element_by_id("flashcliente").text)

    def test_prontuario_invalido_i(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        driver.find_element_by_id("opaddcli").click()
        driver.find_element_by_id("cliaddnome").clear()
        driver.find_element_by_id("cliaddnome").send_keys("Carlos")
        driver.find_element_by_id("cliaddcpf").clear()
        driver.find_element_by_id("cliaddcpf").send_keys("12345678911")
        driver.find_element_by_id("templano2").click()
        driver.find_element_by_id("cliaddnomep").clear()
        driver.find_element_by_id("cliaddnomep").send_keys("Unimed")
        driver.find_element_by_id("cliaddtipop").clear()
        driver.find_element_by_id("cliaddtipop").send_keys("Teste")
        driver.find_element_by_id("cliaddultcon").clear()
        driver.find_element_by_id("cliaddultcon").send_keys("2021-07-31")
        driver.find_element_by_id("cliaddpront").clear()
        driver.find_element_by_id("cliaddpront").send_keys("-1")
        driver.find_element_by_id("cliaddnasc").clear()
        driver.find_element_by_id("cliaddnasc").send_keys("2021-06-27")
        driver.find_element_by_id("dependente2").click()
        driver.find_element_by_id("subaddcli").click()
        self.assertEqual("Prontuário Inválido", driver.find_element_by_id("flashcliente").text)

    def test_cpf_pequeno_i(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        driver.find_element_by_id("opaddcli").click()
        driver.find_element_by_id("cliaddnome").clear()
        driver.find_element_by_id("cliaddnome").send_keys("Carlos")
        driver.find_element_by_id("cliaddcpf").clear()
        driver.find_element_by_id("cliaddcpf").send_keys("1234")
        driver.find_element_by_id("templano2").click()
        driver.find_element_by_id("cliaddnomep").clear()
        driver.find_element_by_id("cliaddnomep").send_keys("Unimed")
        driver.find_element_by_id("cliaddtipop").clear()
        driver.find_element_by_id("cliaddtipop").send_keys("Teste")
        driver.find_element_by_id("cliaddultcon").clear()
        driver.find_element_by_id("cliaddultcon").send_keys("2021-07-31")
        driver.find_element_by_id("cliaddpront").clear()
        driver.find_element_by_id("cliaddpront").send_keys("3")
        driver.find_element_by_id("cliaddnasc").clear()
        driver.find_element_by_id("cliaddnasc").send_keys("2021-06-27")
        driver.find_element_by_id("dependente2").click()
        driver.find_element_by_id("subaddcli").click()
        self.assertEqual("CPF Inválido (Curto demais)", driver.find_element_by_id("flashcliente").text)

    def test_cpf_grande_i(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        driver.find_element_by_id("opaddcli").click()
        driver.find_element_by_id("cliaddnome").clear()
        driver.find_element_by_id("cliaddnome").send_keys("Carlos")
        driver.find_element_by_id("cliaddcpf").clear()
        driver.find_element_by_id("cliaddcpf").send_keys("1234567891011")
        driver.find_element_by_id("templano2").click()
        driver.find_element_by_id("cliaddnomep").clear()
        driver.find_element_by_id("cliaddnomep").send_keys("Unimed")
        driver.find_element_by_id("cliaddtipop").clear()
        driver.find_element_by_id("cliaddtipop").send_keys("Teste")
        driver.find_element_by_id("cliaddultcon").clear()
        driver.find_element_by_id("cliaddultcon").send_keys("2021-07-31")
        driver.find_element_by_id("cliaddpront").clear()
        driver.find_element_by_id("cliaddpront").send_keys("3")
        driver.find_element_by_id("cliaddnasc").clear()
        driver.find_element_by_id("cliaddnasc").send_keys("2021-06-27")
        driver.find_element_by_id("dependente2").click()
        driver.find_element_by_id("subaddcli").click()
        self.assertEqual("CPF Inválido (Longo demais)", driver.find_element_by_id("flashcliente").text)

    def test_insert_id_invalido_orc(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/dentista")
        driver.find_element_by_id("opaddorc").click()
        driver.find_element_by_id("idpb").click()
        Select(driver.find_element_by_id("idpb")).select_by_visible_text("4")
        driver.find_element_by_id("orcadddenprot").clear()
        driver.find_element_by_id("orcadddenprot").send_keys("aaa")
        driver.find_element_by_id("orcadddescproc").clear()
        driver.find_element_by_id("orcadddescproc").send_keys("23523456")
        driver.find_element_by_id("orcaddident").clear()
        driver.find_element_by_id("orcaddident").send_keys("14124121124")
        driver.find_element_by_id("orcadddataval").clear()
        driver.find_element_by_id("orcadddataval").send_keys("2021-07-30")
        driver.find_element_by_id("orcaddass").clear()
        driver.find_element_by_id("orcaddass").send_keys("Doutor Den Tista")
        driver.find_element_by_id("subaddorc").click()
        self.assertEqual("ID de Dentista Inválido", driver.find_element_by_id("flashorca").text)

    def test_api_busca_invalida(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/dentista")
        driver.find_element_by_id("x").click()
        driver.find_element_by_id("send").click()
        self.assertEqual(u"Entrada Inválida", driver.find_element_by_id("flashorca").text)

    def test_api_busca_sem_resposta(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/dentista")
        driver.find_element_by_id("x").clear()
        driver.find_element_by_id("x").send_keys("1495674569071465901756193478634958731465913847614646362357235725272357")
        driver.find_element_by_id("send").click()
        self.assertEqual(u"Não há resposta para este pedido ainda", driver.find_element_by_id("flashorca").text)

    def test_not_found(self) :
        result = requests.get("http://127.0.0.1:5000/naotem")

        expected_status_code = 404
        self.assertEqual(result.status_code, expected_status_code,
                         "Expected status code = '{}', but got '{}'".format(expected_status_code, result.status_code))

    def test_not_found(self) :
        result = requests.get("http://127.0.0.1:5000/cpage/12345/")

        expected_status_code = 500
        self.assertEqual(result.status_code, expected_status_code,
                         "Expected status code = '{}', but got '{}'".format(expected_status_code, result.status_code))

    def test_not_found(self) :
        result = requests.get("http://127.0.0.1:5000/insert")

        expected_status_code = 405
        self.assertEqual(result.status_code, expected_status_code,
                         "Expected status code = '{}', but got '{}'".format(expected_status_code, result.status_code))



    def test_foi_ok(self) :
        result = requests.get("http://127.0.0.1:5000/")

        expected_status_code = 200
        self.assertEqual(result.status_code, expected_status_code,
                         "Expected status code = '{}', but got '{}'".format(expected_status_code, result.status_code))


    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
