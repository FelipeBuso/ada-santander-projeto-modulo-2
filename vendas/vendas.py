from module.module import ler_arquivo, salvar_arquivo
from medicamentos.medicamentos import Medicamentos
from clientes.clientes import Clientes
from datetime import datetime
from functools import reduce


class ExcecaoVendas(Exception):
    def __init__(self, mensagem: str):
        self._erro = mensagem
        super().__init__(self._erro)


class Vendas:
    """
    Representação de uma venda

    Atributos
    ---
    data_hora: datetime
        Hora do incício do atendimento
    produtos: list
        Lista de produtos vendidos
    cpf_cliente: str
        CPF do cliente que está efetuando a compra
    idade_cliente: int
        Idade calculada do cliente com base na data de nascimento
    valor_total: float
        Soma das vendas de produtos

    Métodos
    ---
    cadastro_vendas:
        Insere nova venda de produto.
    encerra_venda:
        Finaliza o atendimento
    """

    def __init__(self, cliente: Clientes):
        self._data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
        self._produtos = []
        self.cpf_cliente = cliente.cpf
        self._idade_cliente = (
            datetime.now() - datetime.strptime(cliente.data_nascimento, "%d/%m/%Y")
        ).days / 365
        self._valor_total = None

    # get e set para data e hora
    def _get_data_hora(self) -> datetime:
        return self._data_hora

    def _set_data_hora(self, data_hora: datetime) -> None:
        self._data_hora = data_hora

    data_hora = property(_get_data_hora, _set_data_hora)

    # get e set para produto
    def _get_produtos(self) -> list:
        return self._produtos

    def _set_produtos(self, produto: str) -> None:
        self._produtos.append(produto)

    produtos = property(_get_produtos, _set_produtos)

    # get e set para cpf do cliente
    def _get_cpf_cliente(self) -> str:
        return self.cpf_cliente

    def _set_cpf_cliente(self, cpf_cliente: str) -> None:
        self.cpf_cliente = cpf_cliente

    cliente = property(_get_cpf_cliente, _set_cpf_cliente)

    # get e set para idade do cliente
    def _get_idade_cliente(self) -> int:
        return self._idade_cliente

    def _set_idade_cliente(self, idade_cliente) -> None:
        self._idade_cliente = idade_cliente

    idade_cliente = property(_get_idade_cliente, _set_idade_cliente)

    # get e set para venda total
    def _get_valor_total(self) -> float:
        return self._valor_total

    def _set_valor_total(self, valor_total: float) -> None:
        self._valor_total = valor_total

    valor_total = property(_get_valor_total, _set_valor_total)

    def cadastro_vendas(self, medicamento: Medicamentos, qnt_venda: int) -> None:
        # busca dados
        dados_bd = ler_arquivo()

        # utiliza id medicamento
        id_medicamento = medicamento.id

        # verifica qnt estoque
        if (
            qnt_venda
            > dados_bd["bd_medicamentos"][id_medicamento]["quantidade_estoque"]
        ):
            raise ExcecaoVendas("Estoque insuficiente.")

        # caso não haja exceção, adicione venda do produto
        venda_produto = {
            "id_produto": medicamento.id,
            "qtde_venda": qnt_venda,
            "sub_total": round(qnt_venda * medicamento.preco, 2),
        }

        # adiciona na lista produtos
        self.produtos = venda_produto
        dados_bd["bd_medicamentos"][id_medicamento]["quantidade_estoque"] -= qnt_venda
        salvar_arquivo(dados_bd)

    def encerra_venda(self):
        dados_bd = ler_arquivo()

        # busca medicamentos
        bd_medicamentos = dados_bd["bd_medicamentos"]
        dados_bd["bd_medicamentos"] = bd_medicamentos

        # verifica quantidade de vendas existentes
        qnt_vendas = "1"
        if "bd_vendas" in dados_bd:
            qnt_vendas = str(len(dados_bd["bd_vendas"]) + 1)
        elif "bd_vendas" not in dados_bd:
            dados_bd["bd_vendas"] = {qnt_vendas: {}}  # adiciona número da venda

        # adiciona venda com dados de produto e cliente
        obj_venda = {
            "data_hora": self.data_hora,
            "produtos_vendidos": self._produtos,
            "cliente": self.cpf_cliente,
            "valor_total": round(
                reduce(lambda soma, valor: soma + valor["sub_total"], self.produtos, 0),
                2,
            ),
        }

        # verifica desconto na venda
        if self.idade_cliente > 65:
            obj_venda["valor_total"] = round(obj_venda["valor_total"] * 0.8, 2)

        elif obj_venda["valor_total"] > 150:
            obj_venda["valor_total"] = round(obj_venda["valor_total"] * 0.9, 2)

        # adiciona venda no arquivo json
        dados_bd["bd_vendas"][qnt_vendas] = obj_venda
        salvar_arquivo(dados_bd)
