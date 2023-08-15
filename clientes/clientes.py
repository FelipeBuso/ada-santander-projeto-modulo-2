from module.module import ler_arquivo, salvar_arquivo
from datetime import datetime, date
import re


bd = ler_arquivo()


class ExcecaoClientes(Exception):
    def __init__(self, mensagem: str):
        self._erro = mensagem
        super().__init__(self._erro)


class Clientes:
    def __init__(self):
        self._nome = None
        self._cpf = None
        self._data_nascimento = None

    def valida_cpf(self, cpf):
        cpf = re.sub(r"[!@#$%^&*-. ]", "", str(cpf)).zfill(11)
        if not cpf.isdigit() or len(cpf) > 11:
            raise ValueError("CPF inválido")
        return cpf

    def _get_nome(self) -> str:
        return self._nome

    def _set_nome(self, nome: str) -> None:
        self._nome = nome

    nome = property(_get_nome, _set_nome)

    def _get_cpf(self):
        return self._cpf

    def _set_cpf(self, cpf: str) -> None:
        self._cpf = self.valida_cpf(cpf)

    cpf = property(_get_cpf, _set_cpf)

    def _get_data_nascimento(self):
        return datetime.strftime(self._data_nascimento, "%d/%m/%Y")

    def _set_data_nascimento(self, data_nascimento: date) -> None:
        self._data_nascimento = data_nascimento

    data_nascimento = property(_get_data_nascimento, _set_data_nascimento)

    def buscar_cliente(self, cpf: str) -> dict[str,str]:
        if cpf in bd["bd_clientes"] and bd["bd_clientes"][cpf]:
            cliente = bd["bd_clientes"][cpf]
            self.nome = cliente["nome"]
            self.cpf = cpf
            self.data_nascimento = cliente["data_nascimento"]
            return {"cpf": cpf, **cliente}
        else:
            raise ExcecaoClientes("Cliente não localizado.")

    def cadastrar_cliente(self, nome: str, cpf: str, data_nascimento: str) -> str:
        print(bd)
        cpf = self.valida_cpf(cpf)
        if cpf in bd["bd_clientes"]:
            raise ExcecaoClientes("Cliente já cadastrado")
        else:
            bd["bd_clientes"][cpf] = {
                "nome": nome,
                "data_nascimento": data_nascimento,
            }
            salvar_arquivo(bd)
            self.buscar_cliente(cpf)
            return "Cliente cadastrado com sucesso"

    def relatorio_clientes(self) -> list[dict[str,str]]:
        clientes = [{"cpf": key, **value} for key, value in bd["bd_clientes"].items()]
        funcao_sort = lambda x: x["nome"]
        clientes.sort(key=funcao_sort)
        return clientes
