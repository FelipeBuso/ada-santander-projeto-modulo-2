from module.module import ler_arquivo
from typing import Dict


class ExcecaoDocumentos(Exception):
    def __init__(self, mensagem: str):
        self._erro = mensagem
        super().__init__(self._erro)


def preencher_cliente(id: str) -> Dict:
    bd_dados = ler_arquivo()
    bd_clientes = bd_dados["bd_clientes"]

    if id in bd_clientes and bd_clientes[id]:
        return bd_clientes[id]
    else:
        raise ExcecaoDocumentos("Cliente não localizado")


def preencher_laboratório(id: str) -> Dict:
    bd_dados = ler_arquivo()
    bd_laboratorios = bd_dados["bd_laboratorios"]

    if id in bd_laboratorios and bd_laboratorios[id]:
        return bd_laboratorios[id]
    else:
        raise ExcecaoDocumentos("Laboratorio não localizado")


def preencher_medicamento(id: str) -> Dict:
    bd_dados = ler_arquivo()
    bd_medicamentos = bd_dados["bd_medicamentos"]

    if id in bd_medicamentos and bd_medicamentos[id]:
        return bd_medicamentos[id]
    else:
        raise ExcecaoDocumentos("Medicamento não localizado")
