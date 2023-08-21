from module.module import ler_arquivo
from typing import Dict


class ExcecaoDocumentos(Exception):
    def __init__(self, mensagem: str):
        self._erro = mensagem
        super().__init__(self._erro)


# Lẽ o arquivo db.json, filtra a coleção e retorna o documento pelo id.
def preencher_documento(id: str, collection: str) -> Dict:
    bd_dados = ler_arquivo()
    bd_collection = bd_dados[collection]

    if id in bd_collection and bd_collection[id]:
        return bd_collection[id]
    else:
        raise ExcecaoDocumentos("Documento não localizado")


# Filtra as informações de vendas do banco de dados e rotorna um dicionario com as informações do relatório
def gerar_relatorio_diario(data_inicial: str) -> Dict:
    """
    Retorna um relatório de estatísticas de atendimento a partir da data informada até o fechamento
    """
    bd_dados = ler_arquivo()
    bd_vendas = bd_dados["bd_vendas"]
    clientes_atendidos = list()
    relatorio_vendas = dict()

    # filtra as vendas pela data parâmetro
    vendas_filtradas = [
        venda for venda in bd_vendas.values() if venda["data_hora"] >= data_inicial
    ]
    if len(vendas_filtradas) == 0:
        raise ExcecaoDocumentos("Não houve vendas nesta data")

    dicionario_vendas = {
        "produto_geral": {},
        "produto_quimioterapico": {"qtde_vendida": 0, "total_vendido": 0},
        "produto_fitoterapico": {"qtde_vendida": 0, "total_vendido": 0},
    }

    # Percorre os itens vendidos para cálculo de quantidade e valores
    for item in vendas_filtradas:
        clientes_atendidos.append(item["cliente"])
        for item_medicamento in item["produtos_vendidos"]:
            id = item_medicamento["id_produto"]
            medicamento = preencher_documento(id=id, collection="bd_medicamentos")
            # verifica se o produto já existe no dicionario e atualiza ou incrementa os valores
            if id in dicionario_vendas["produto_geral"]:
                dicionario_vendas["produto_geral"][id][
                    "qtde_vendida"
                ] += item_medicamento["qtde_venda"]
                dicionario_vendas["produto_geral"][id][
                    "total_venda"
                ] += item_medicamento["sub_total"]
            else:
                dicionario_vendas["produto_geral"][id] = {
                    "qtde_vendida": item_medicamento["qtde_venda"],
                    "total_venda": item_medicamento["sub_total"],
                }
            # Incrementa a quantidade e valores por tipo de medicmaneto
            if "necessita_receita" in medicamento:
                dicionario_vendas["produto_quimioterapico"][
                    "qtde_vendida"
                ] += item_medicamento["qtde_venda"]
                dicionario_vendas["produto_quimioterapico"][
                    "total_vendido"
                ] += item_medicamento["sub_total"]
            else:
                dicionario_vendas["produto_fitoterapico"][
                    "qtde_vendida"
                ] += item_medicamento["qtde_venda"]
                dicionario_vendas["produto_fitoterapico"][
                    "total_vendido"
                ] += item_medicamento["sub_total"]

    # Retorna o produto com maior número de unidades vendidas
    maior_qtde_venda = max(
        [venda for venda in dicionario_vendas["produto_geral"].items()],
        key=lambda x: x[1]["qtde_vendida"],
    )
    medicamento_maior_venda = preencher_documento(
        id=maior_qtde_venda[0], collection="bd_medicamentos"
    )

    relatorio_vendas["remedio_mais_vendido"] = {
        "nome": medicamento_maior_venda["nome"],
        "qtde_vendida": maior_qtde_venda[1]["qtde_vendida"],
        "total_vendido": round(maior_qtde_venda[1]["total_venda"], 2),
    }
    relatorio_vendas["clientes_atendidos"] = len(set(clientes_atendidos))
    relatorio_vendas["vendas_quimioterapicos"] = dicionario_vendas[
        "produto_quimioterapico"
    ]
    relatorio_vendas["vendas_fitoterapicos"] = dicionario_vendas["produto_fitoterapico"]

    return relatorio_vendas
