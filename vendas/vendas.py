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

    def alerta_quimioterapicos(self._produto, necessita_receita):
        if necessita_receita:
            print(f"Por favor verifique a receita do cliente para o medicamento {self._produto._get_nome()}")

    def desconto_idoso(self):
        data_nascimento_cliente = self._cliente.data_nascimento
        idade = (datetime.now() - datetime.strptime(data_nascimento_cliente, "%d/%m/%Y")).days // 365

        if idade > 65:
            self.valor_total *= 0.8

    def desconto_geral(self):
        valor_minimo = 150.00
        if self.valor_total > valor_minimo:
            self.valor_total *= 0.85

    def melhor_desconto(self):
        desconto_idoso_aplicado = self.valor_total.desconto_idoso()
        desconto_geral_aplicado = self.valor_total.desconto_geral()
        if desconto_idoso_aplicado < desconto_geral_aplicado:
            self.valor_total = desconto_idoso_aplicado
        else:
            self.valor_total = desconto_geral_aplicado
