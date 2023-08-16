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

    def _get_id(self) -> int:
        return self._id

    def _set_id(self, id: str) -> None:
        self._id = id

    id = property(_get_id, _set_id)

    def _get_nome(self) -> str:
        return self._nome

    def _set_nome(self, nome: str) -> None:
        self._nome = nome

    nome = property(_get_nome, _set_nome)

    def _get_principio_ativo(self) -> str:
        return self.__principio_ativo

    def _set_principio_ativo(self, principio_ativo: str) -> None:
        self._principio_ativo = principio_ativo

    principio_ativo = property(_get_principio_ativo, _set_principio_ativo)

    def _get_laboratorio(self) -> str:
        return self._laboratorio

    def _set_laboratorio(self, laboratorio: str) -> None:
        self._laboratorio = laboratorio

    laboratorio = property(_get_laboratorio, _set_laboratorio)

    def _get_descricao(self) -> str:
        return self._descricao

    def _set_descricao(self, descricao: str) -> None:
        self._descricao = descricao

    descricao = property(_get_descricao, _set_descricao)

    def _get_preco(self) -> float:
        return self._preco

    def _set_preco(self, preco: float) -> None:
        self._preco = preco

    preco = property(_get_preco, _set_preco)

    def _get_quantidade_estoque(self) -> float:
        return self._quantidade_estoque

    def _set_quantidade_estoque(self, quantidade_estoque: float) -> None:
        self._quantidade_estoque = quantidade_estoque

    quantidade_estoque = property(_get_quantidade_estoque, _set_quantidade_estoque)

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
            self.id = id
            self.nome = dados_medicamentos[id]["nome"]
            self.principio_ativo = dados_medicamentos[id]["principio_ativo"]
            self.laboratorio = dados_medicamentos[id]["laboratorio"]
            self.descricao = dados_medicamentos[id]["descricao"]
            self.preco = dados_medicamentos[id]["preco"]
            self.quantidade_estoque = dados_medicamentos[id]["quantidade_estoque"]
            response = {
                "necessita_receita": False,
                "medicamento": dados_medicamentos[id],
            }
        else:
            raise ExcecaoMedicamentos("Medicamento não localizado")

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

    def pesquisa_medicamento_descricao(self, descricao: str) -> List[Dict[str, str]]:
        dados_bd = ler_arquivo()
        dados_medicamentos = dados_bd["bd_medicamentos"]
        medicamentos_localizados = list()
        for id, medicamento in dados_medicamentos.items():
            if descricao.lower() in medicamento["descricao"].lower():
                medicamentos_localizados.append({"id": id, **medicamento})
        if len(medicamentos_localizados) > 0:
            return medicamentos_localizados
        else:
            raise ExcecaoMedicamentos("Medicamento não localizado")

    def lista_todos_medicamentos(self) -> List[Dict[str, str]]:
        dados_bd = ler_arquivo()
        dados_medicamentos = dados_bd["bd_medicamentos"]
        lista_medicamentos = [
            {"id": id, **medicamento} for id, medicamento in dados_medicamentos.items()
        ]
        if len(lista_medicamentos) > 0:
            funcao_sort = lambda x: x["nome"]
            lista_medicamentos.sort(key=funcao_sort)
            return lista_medicamentos
        else:
            raise ExcecaoMedicamentos("Nenhum medicamento localizado")


class MedicamentosQuimioterapicos(Medicamentos):
    def __init__(self) -> None:
        self._necessita_receita = None
        super().__init__()

    def _get_necessita_receita(self) -> bool:
        return self._necessita_receita

    def _set_necessita_receita(self, necessita_receita: bool) -> None:
        self._necessita_receita = necessita_receita

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

    def buscar_medicamento(self, id: str) -> Dict:
        dados_bd = ler_arquivo()
        dados_medicamentos = dados_bd["bd_medicamentos"]
        if id in dados_medicamentos and dados_medicamentos[id]:
            self.id = id
            self.nome = dados_medicamentos[id]["nome"]
            self.principio_ativo = dados_medicamentos[id]["principio_ativo"]
            self.laboratorio = dados_medicamentos[id]["laboratorio"]
            self.descricao = dados_medicamentos[id]["descricao"]
            self.preco = dados_medicamentos[id]["preco"]
            self.quantidade_estoque = dados_medicamentos[id]["quantidade_estoque"]
            self.necessita_receita = dados_medicamentos[id]["necessita_receita"]
            response = {
                "necessita_receita": dados_medicamentos[id]["necessita_receita"],
                "medicamento": dados_medicamentos[id],
            }
            if dados_medicamentos[id]["necessita_receita"]:
                response[
                    "mensagem"
                ] = f'o medicamento {dados_medicamentos[id]["nome"]} é controlado. Verificou a receita com o cliente?'
            return response
        else:
            raise ExcecaoMedicamentos("Medicamento não localizado")

    def lista_medicamentos(self) -> List[Dict[str, str]]:
        dados_bd = ler_arquivo()
        dados_medicamentos = dados_bd["bd_medicamentos"]
        lista_medicamentos_quimioterapicos = [
            {"id": id, **medicamento}
            for id, medicamento in dados_medicamentos.items()
            if "necessita_receita" in medicamento
        ]
        if len(lista_medicamentos_quimioterapicos) > 0:
            return lista_medicamentos_quimioterapicos
        else:
            raise ExcecaoMedicamentos("Nenhum medicamento localizado")


class MedicamentosFitoterapicos(Medicamentos):
    def __init__(self) -> None:
        super().__init__()

    def lista_medicamentos(self) -> List[Dict[str, str]]:
        dados_bd = ler_arquivo()
        dados_medicamentos = dados_bd["bd_medicamentos"]
        lista_medicamentos_fitoterapicos = [
            {"id": id, **medicamento}
            for id, medicamento in dados_medicamentos.items()
            if not "necessita_receita" in medicamento
        ]
        if len(lista_medicamentos_fitoterapicos) > 0:
            return lista_medicamentos_fitoterapicos
        else:
            raise ExcecaoMedicamentos("Nenhum medicamento localizado")
