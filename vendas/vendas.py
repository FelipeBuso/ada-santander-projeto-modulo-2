from module.module import ler_arquivo, salvar_arquivo
from medicamentos.medicamentos import Medicamentos
from clientes.clientes import Clientes
from datetime import datetime

class Vendas:
    def __init__(self, produto: Medicamentos, cliente: Clientes):
        self._data_hora = datetime.now().strftime('%d/%m/%Y %H:%M')
        self._produto = produto
        self._cliente = cliente
        self._valor_total = None
    
    # get e set para data e hora
    def _get_data_hora(self) -> datetime:
        return self._data_hora
    
    def _set_data_hora(self, data_hora: datetime) -> None:
        self._data_hora = data_hora
    
    data_hora = property(_get_data_hora, _set_data_hora)
    
    # get e set para produto
    def _get_produto(self) -> str:
        return self._produto
    
    def _set_produto(self, produto: str) -> None:
        self._produto = produto
    
    produto = property(_get_produto, _set_produto)
    
    # get e set para cliente
    def _get_cliente(self) -> str:
        return self._cliente
    
    def _set_cliente(self, cliente: str) -> None:
        self._cliente = cliente
    
    cliente = property(_get_cliente, _set_cliente)

    # get e set para venda total
    def _get_valor_total(self) -> float:
        return self._valor_total

    def _set_valor_total(self, valor_total: float) -> None:
        self._valor_total = valor_total

    valor_total = property(_get_valor_total, _set_valor_total)