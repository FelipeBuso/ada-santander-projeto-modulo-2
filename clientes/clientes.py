from module.module import ler_arquivo, salvar_arquivo
from datetime import datetime, date
import re
from typing import List, Dict


class ExcecaoClientes(Exception):
    def __init__(self, mensagem: str):
        self._erro = mensagem
        super().__init__(self._erro)


class Clientes:
    """
    Classe que representa um cliente
    ...

    Atributos
    ---
    cpf: str
        CPF do cliente com 11 dígitos
    nome: str
        Nome completo do cliente
    data de nascimento: str
        Data de nascimento no formato dd/mm/yyyy
    ativo: bool

    Métodos
    ---
    buscar_cliente:
        Retorna os dados do cliente para a instância
    cadastrar_cliente:
        Cadastra o cliente no banco de dados
    excluir_cliente:
        Altera a chave ativo no banco de dados
    relatorio_clientes:
        retorna um lista de clientes
    """

    def __init__(self):
        self._nome = None
        self._cpf = None
        self._data_nascimento = None
        self._ativo = True

    def valida_cpf(self, cpf):
        """
        Valida se o cpf é contem somente números e preenche com 0 à esquerda
        """
        cpf = re.sub(r"[!@#$%^&*-. ]", "", str(cpf)).zfill(11)
        if not cpf.isdigit() or len(cpf) > 11:
            raise ValueError("CPF inválido")
        return cpf

    def _get_nome(self) -> str:
        return self._nome

    def _set_nome(self, nome: str) -> None:
        self._nome = nome

    nome = property(_get_nome, _set_nome)

    def _get_cpf(self) -> str:
        return self._cpf

    def _set_cpf(self, cpf: str) -> None:
        self._cpf = self.valida_cpf(cpf)

    cpf = property(_get_cpf, _set_cpf)

    def _get_data_nascimento(self) -> str:
        return self._data_nascimento

    def _set_data_nascimento(self, data_nascimento: str) -> None:
        self._data_nascimento = data_nascimento

    data_nascimento = property(_get_data_nascimento, _set_data_nascimento)

    def _get_ativo(self) -> bool:
        return self._ativo

    def _set_ativo(self, ativo: bool) -> None:
        self._ativo = ativo

    ativo = property(_get_ativo, _set_ativo)

    def buscar_cliente(self, cpf: str) -> Dict[str, str]:
        """
        Busca um cliente no banco de dados pelo CPF

        Caso não exista, lança um exceção do tipo "ExcecaoClientes"
        """
        dados_bd = ler_arquivo()
        if (
            cpf in dados_bd["bd_clientes"]
            and dados_bd["bd_clientes"][cpf]
            and dados_bd["bd_clientes"][cpf]["ativo"]
        ):
            dict_cliente = dados_bd["bd_clientes"][cpf]
            self.nome = dict_cliente["nome"]
            self.cpf = cpf
            self.data_nascimento = dict_cliente["data_nascimento"]
            self.ativo = dict_cliente["ativo"]
            return {"cpf": self.cpf, **dict_cliente}
        else:
            raise ExcecaoClientes("Cliente não localizado.")

    def cadastrar_cliente(self, nome: str, cpf: str, data_nascimento: str) -> str:
        """
        Cadastra o cliente no banco de dados.

        Caso o cpf já exista no banco de dados, lança um exceção do tipo "ExcecaoClientes"
        """
        dados_bd = ler_arquivo()
        cpf = self.valida_cpf(cpf)
        if (
            cpf in dados_bd["bd_clientes"]
            and dados_bd["bd_clientes"][cpf]
            and dados_bd["bd_clientes"][cpf]["ativo"]
        ):
            raise ExcecaoClientes("Cliente já cadastrado")
        elif (
            cpf in dados_bd["bd_clientes"] and not dados_bd["bd_clientes"][cpf]["ativo"]
        ):
            dados_bd["bd_clientes"][cpf]["ativo"] = True
            salvar_arquivo(dados_bd)
            return "Cliente reativado"
        else:
            dados_bd["bd_clientes"][cpf] = {
                "nome": nome,
                "data_nascimento": data_nascimento,
                "ativo": self.ativo,
            }
            salvar_arquivo(dados_bd)
            self.buscar_cliente(cpf)
            return "Cliente cadastrado com sucesso"

    def excluir_cliente(self, cpf: str) -> str:
        """
        Localiza o cpf no banco de dados e atualiza a chave "ativo" para false

        Caso cliente já esteja inativo ou não seja localizado, lança uma exceção
        do tipo "ExcecaoClientes"
        """
        dados_bd = ler_arquivo()
        cpf = self.valida_cpf(cpf)
        if cpf not in dados_bd["bd_clientes"]:
            raise ExcecaoClientes("Cliente não localizado")
        elif (
            cpf in dados_bd["bd_clientes"]
            and dados_bd["bd_clientes"][cpf]
            and not dados_bd["bd_clientes"][cpf]["ativo"]
        ):
            raise ExcecaoClientes("Cliente já está inativo")
        elif (
            cpf in dados_bd["bd_clientes"]
            and dados_bd["bd_clientes"][cpf]
            and dados_bd["bd_clientes"][cpf]["ativo"]
        ):
            dados_bd["bd_clientes"][cpf]["ativo"] = False
            salvar_arquivo(dados_bd)
            return "Cliente excluido"
        else:
            raise ExcecaoClientes("Erro desconhecido (excluir_cliente)")

    def relatorio_clientes(self) -> List[Dict[str, str]]:
        """
        Retorna lista de clientes, em ordem crescente, pela chave nome.
        """
        dados_bd = ler_arquivo()
        clientes = [
            {"cpf": key, **value} for key, value in dados_bd["bd_clientes"].items()
        ]
        funcao_sort = lambda x: x["nome"]
        clientes.sort(key=funcao_sort)
        return clientes
