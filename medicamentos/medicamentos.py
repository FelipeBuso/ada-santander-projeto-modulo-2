from module.module import ler_arquivo, salvar_arquivo
from laboratorios.laboratorios import Laboratorios
from typing import Dict, List


class ExcecaoMedicamentos(Exception):
    def __init__(self, mensagem: str):
        self._erro = mensagem
        super().__init__(self._erro)


class Medicamentos:
    def __init__(self) -> None:
        self._id = None
        self._nome = None
        self._principio_ativo = None
        self._laboratorio = None
        self._descricao = None
        self._preco = None
        self._quantidade_estoque = None

    @property
    def id(self) -> int:
        return self._id

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def principio_ativo(self) -> str:
        return self.__principio_ativo

    @property
    def laboratorio(self) -> str:
        return self._laboratorio

    @property
    def descricao(self) -> str:
        return self._descricao

    @property
    def preco(self) -> float:
        return self._preco

    @property
    def quantidade_estoque(self) -> float:
        return self._quantidade_estoque

    def cadastrar_medicamento(
        self,
        nome: str,
        principio_ativo: str,
        laboratorio: Laboratorios,
        descricao: str,
        preco: float,
        quantidade_estoque: float = 0,
    ):
        dados_bd = ler_arquivo()
        id_medicamento = str(len(dados_bd["bd_medicamentos"]) + 1)
        if dados_bd["bd_medicamentos"]:
            for _, medicamento in dados_bd["bd_medicamentos"].items():
                if medicamento["nome"] == nome:
                    raise ExcecaoMedicamentos("Medicamento já cadastrato")

        novo_medicamento = {
            "nome": nome,
            "principio_ativo": principio_ativo,
            "laboratorio": laboratorio.cnpj,
            "descricao": descricao,
            "preco": preco,
            "quantidade_estoque": quantidade_estoque,
        }
        dados_bd["bd_medicamentos"][id_medicamento] = novo_medicamento
        salvar_arquivo(dados_bd)
        return "Medicamento cadastrado com sucesso"

    def buscar_medicamento(self, id: str) -> Dict:
        dados_bd = ler_arquivo()
        dados_medicamentos = dados_bd["bd_medicamentos"]
        if id in dados_medicamentos and dados_medicamentos[id]:
            return dados_medicamentos[id]
        else:
            raise ExcecaoMedicamentos("medicamento não localizado")

    def pesquisa_medicamento_nome(self, nome: str) -> List[Dict[str, str]]:
        dados_bd = ler_arquivo()
        dados_medicamentos = dados_bd["bd_medicamentos"]
        medicamentos_localizados = list()
        for id, medicamento in dados_medicamentos.items():
            if nome.lower() in medicamento["nome"].lower():
                medicamentos_localizados.append({"id": id, **medicamento})
        if len(medicamentos_localizados) > 0:
            return medicamentos_localizados
        else:
            raise ExcecaoMedicamentos("Medicamento não localizado")

    def pesquisa_medicamento_laboratorio(
        self, laboratorio: Laboratorios
    ) -> List[Dict[str, str]]:
        dados_bd = ler_arquivo()
        dados_medicamentos = dados_bd["bd_medicamentos"]
        medicamentos_localizados = list()
        for id, medicamento in dados_medicamentos.items():
            if laboratorio.cnpj == medicamento["laboratorio"]:
                medicamentos_localizados.append({"id": id, **medicamento})
        if len(medicamentos_localizados) > 0:
            return medicamentos_localizados
        else:
            raise ExcecaoMedicamentos("Medicamento não localizado")


class MedicamentosQuimioterapicos(Medicamentos):
    def __init__(self) -> None:
        self._necessita_receita = None
        super().__init__()

    @property
    def necessita_receita(self) -> bool:
        return self._necessita_receita

    def cadastrar_medicamento(
        self,
        nome: str,
        principio_ativo: str,
        laboratorio: Laboratorios,
        descricao: str,
        preco: float,
        necessita_receita: bool,
        quantidade_estoque: float = 0,
    ):
        dados_bd = ler_arquivo()
        id_medicamento = str(len(dados_bd["bd_medicamentos"]) + 1)
        if dados_bd["bd_medicamentos"]:
            for _, medicamento in dados_bd["bd_medicamentos"].items():
                if medicamento["nome"] == nome:
                    raise ExcecaoMedicamentos("Medicamento já cadastrato")

        novo_medicamento = {
            "nome": nome,
            "principio_ativo": principio_ativo,
            "laboratorio": laboratorio.cnpj,
            "descricao": descricao,
            "preco": preco,
            "quantidade_estoque": quantidade_estoque,
            "necessita_receita": necessita_receita,
        }
        dados_bd["bd_medicamentos"][id_medicamento] = novo_medicamento
        salvar_arquivo(dados_bd)
        return "Medicamento cadastrado com sucesso"


class MedicamentosFitoterapicos(Medicamentos):
    def __init__(self) -> None:
        super().__init__()
