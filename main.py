from clientes.clientes import Clientes, ExcecaoClientes
from datetime import datetime
from laboratorios.laboratorios import Laboratorios, ExcessaoLaboratorios
from medicamentos.medicamentos import (
    Medicamentos,
    MedicamentosFitoterapicos,
    MedicamentosQuimioterapicos,
    ExcecaoMedicamentos,
)
from vendas.vendas import Vendas
from unidecode import unidecode
from utils.utils import gerar_relatorio_diario, ExcecaoDocumentos

menu = """
        ========================================================
                            SEJA BEM-VINDO(A)!"                 
        ========================================================
        MENU DE OPÇÕES

        1-Cadastrar laboratório
        2-Cadastrar medicamento fitoterápico
        3-Cadastrar medicamento quimioterápico
        4-Cadastrar cliente
        5-Cadastrar venda
        6-Relatórios
        7-Sair

        Selecione uma das opções:
    """
menu_relatorios = """
        ========================================================
                        Selecione o relatório                 
        ========================================================
        MENU DE OPÇÕES

        1-Clientes
        2-Medicamento fitoterápico
        3-Medicamento quimioterápico
        4-Medicamentos geral
        5-Estatíscas dos atendimentos
        6-Sair

        Selecione uma das opções:
    """


if __name__ == "__main__":
    # lê dados antes de iniciar operações

    cond_init = True
    while cond_init:
        option = input(menu)
        print("\n")

        if option == "1":
            laboratorio = Laboratorios()
            cnpj = input("Informe o CNPJ do laboratório: ")
            nome = input("Informe o nome do laboratório: ")
            endereco = input("Informe o endereço do laboratório: ")
            telefone = input("Informe o telefone do laboratório: ")
            cidade = input("Informe a cidade do laboratório: ")
            estado = input("Informe o estado do laboratório: ")
            laboratorio.cadastrar_laboratorio(
                cnpj=cnpj,
                nome=nome,
                endereco=endereco,
                telefone=telefone,
                cidade=cidade,
                estado=estado,
            )

        elif option == "2":
            medicamento_fitoterapico = MedicamentosFitoterapicos()
            nome = input("Informe o nome do medicamento fitoterápico: ")
            principio_ativo = input(
                "Informe o nome do princípio ativo do medicamento fitoterápico: "
            )

            laboratorio_localizado = False
            while not laboratorio_localizado:
                laboratorio_cnpj = input("Informe o CNPJ do laboratório: ")
                try:
                    laboratorio = Laboratorios()
                    laboratorio.buscar_laboratorio(laboratorio_cnpj)
                except ExcessaoLaboratorios as error:
                    print(str(error))
                else:
                    laboratorio_localizado = True

            descricao = input("Informe a descrição do medicamento fitoterápico: ")
            preco = float(input("Informe o preço do medicamento fitoterápico: "))
            quantidade_estoque = float(
                input("Informe a quantidade de medicamento fitoterápico: ")
            )
            medicamento_fitoterapico.cadastrar_medicamento(
                nome=nome,
                principio_ativo=principio_ativo,
                laboratorio=laboratorio,
                descricao=descricao,
                preco=preco,
                quantidade_estoque=quantidade_estoque,
            )

        elif option == "3":
            medicamento_quimioterapico = MedicamentosQuimioterapicos()
            nome = input("Informe o nome do medicamento: ")
            principio_ativo = input("Informe o nome do medicamento: ")
            laboratorio_localizado = False
            while not laboratorio_localizado:
                laboratorio_cnpj = input("Informe o CNPJ do laboratório: ")
                try:
                    laboratorio = Laboratorios()
                    laboratorio.buscar_laboratorio(laboratorio_cnpj)
                except ExcessaoLaboratorios as error:
                    print(str(error))
                else:
                    laboratorio_localizado = True

            descricao = input("Informe a descirção do medicamento: ")
            preco = float(input("Informe o valor do medicamento: "))
            verifica_necessita_receita = True
            necessita_receita = ""
            while verifica_necessita_receita:
                necessita_receita = input(
                    "Informe se o medicamento é controlado (S/N): "
                )
                if unidecode(necessita_receita.lower()) in ["s", "sim", "n", "nao"]:
                    verifica_necessita_receita = False
            quantidade_estoque = float(input("Informe o estoque do medicamento: "))
            necessita_receita = necessita_receita.lower() in ["s", "sim"]
            medicamento_quimioterapico.cadastrar_medicamento(
                nome=nome,
                principio_ativo=principio_ativo,
                laboratorio=laboratorio,
                descricao=descricao,
                preco=preco,
                necessita_receita=necessita_receita,
                quantidade_estoque=quantidade_estoque,
            )

        elif option == "4":
            cliente = Clientes()
            nome = input("Informe o nome do cliente: ")
            cpf = input("Informe o cpf do cliente (sem números): ")
            data_nascimento = input("Informe a data de nascimento do cliente: ")
            cliente.cadastrar_cliente(
                nome=nome, cpf=cpf, data_nascimento=data_nascimento
            )

        elif option == "5":
            cliente_localizado = False
            while not cliente_localizado:
                cliente_cpf = input("Informe o CPF do cliente: ")
                try:
                    cliente = Clientes()
                    cliente.buscar_cliente(cliente_cpf)
                except ExcecaoClientes as error:
                    print(str(error))
                else:
                    cliente_localizado = True

            venda = Vendas(cliente=cliente)
            cadastrar_venda = True
            while cadastrar_venda:
                medicamento_localizado = False
                while not medicamento_localizado:
                    medicamento_id = input("Informe o ID do medicamento: ")
                    try:
                        medicamento_pesquisado = Medicamentos()
                        medicamento_classe_correta = (
                            medicamento_pesquisado.retorna_classe(medicamento_id)
                        )
                    except ExcecaoDocumentos as error:
                        print(str(error))
                        continue

                    try:
                        medicamento_retornado = (
                            medicamento_classe_correta.buscar_medicamento(
                                medicamento_id
                            )
                        )
                        if "mensagem" in medicamento_retornado:
                            print(medicamento_retornado["mensagem"])
                    except ExcecaoMedicamentos as error:
                        print(str(error))
                    else:
                        medicamento_localizado = True

                qtde_venda = float(input("informe a quantidade desejada: "))

                venda.cadastro_vendas(
                    medicamento=medicamento_classe_correta,
                    qnt_venda=qtde_venda,
                )
                verifica_nova_venda = True
                while verifica_nova_venda:
                    cadastrar_nova_venda = input("Inserir mais produto? (S/N): ")
                    if unidecode(cadastrar_nova_venda.lower()) in [
                        "s",
                        "sim",
                        "n",
                        "nao",
                    ]:
                        if unidecode(cadastrar_nova_venda.lower()) in ["n", "nao"]:
                            cadastrar_venda = False
                        verifica_nova_venda = False

            venda.encerra_venda()

        elif option == "6":
            condicao = True
            while condicao:
                option_relatorio = input(menu_relatorios)
                print("\n")

                if option_relatorio == "1":
                    cliente = Clientes()
                    clientes = cliente.relatorio_clientes()
                    print(
                        f"{'cpf':15} {'nome':30} {'Data de nascimento':12}", end="\n\n"
                    )
                    for cliente in clientes:
                        print(
                            f"{cliente['cpf']:15} {cliente['nome']:30} {cliente['data_nascimento']:12}",
                            end="\n",
                        )

                elif option_relatorio == "2":
                    medicamento_fitoterapico = MedicamentosFitoterapicos()
                    medicamentos_fitoterapicos = (
                        medicamento_fitoterapico.lista_medicamentos()
                    )
                    print(
                        f'{"ID":4} {"Nome":30} {"Laboratório":10} {"Preço":6} {"Estoque":6}',
                        end="\n",
                    )
                    for medicamento in medicamentos_fitoterapicos:
                        print(
                            f'{medicamento["id"]:4} {medicamento["nome"]:30} {medicamento["laboratorio"]:10} {medicamento["preco"]:6} {medicamento["quantidade_estoque"]:6}',
                            end="\n",
                        )

                elif option_relatorio == "3":
                    medicamento_quimioterapico = MedicamentosQuimioterapicos()
                    medicamento_quimioterapico.lista_medicamentos
                    medicamentos_quimioterapicos = (
                        medicamento_quimioterapico.lista_medicamentos()
                    )
                    print(
                        f'{"ID":4} {"Nome":30} {"Necessita Receita":25} {"Laboratório":10} {"Preço":6} {"Estoque":6}',
                        end="\n",
                    )
                    for medicamento in medicamentos_quimioterapicos:
                        print(
                            f'{medicamento["id"]:4} {medicamento["nome"]:30} { "Sim" if medicamento["necessita_receita"] else "Não":30} {medicamento["laboratorio"]:10} {medicamento["preco"]:6} {medicamento["quantidade_estoque"]:6}',
                            end="\n",
                        )

                elif option_relatorio == "4":
                    medicamentos = Medicamentos()
                    todos_medicamentos = medicamentos.lista_todos_medicamentos()

                    def aplica_receita(medicamento: dict) -> str:
                        if (
                            "necessita_receita" in medicamento
                            and medicamento["necessita_receita"]
                        ):
                            return "Sim"
                        if (
                            "necessita_receita" in medicamento
                            and not medicamento["necessita_receita"]
                        ):
                            return "Não"
                        else:
                            return "Não se aplica"

                    print(
                        f'{"ID":4} {"Tipo":15} {"Nome":30} {"Necessita Receita":25} {"Laboratório":10} {"Preço":6} {"Estoque":6}',
                        end="\n",
                    )

                    for medicamento in todos_medicamentos:
                        print(
                            f'{medicamento["id"]:4} {"Quimioterápico" if "necessita_receita" in medicamento else "Fitoterápico":15} {medicamento["nome"]:30} {aplica_receita(medicamento):25} {medicamento["laboratorio"]:10} {medicamento["preco"]:6} {medicamento["quantidade_estoque"]:6}',
                            end="\n",
                        )

                elif option_relatorio == "5":
                    data_escolhida = input("Digite data do relatorio pretendido: ")
                    try:
                        estatisticas = gerar_relatorio_diario(data_escolhida)
                        print("Métricas do dia\n\n")
                        print(
                            f'Remédio mais vendido (unidades): {estatisticas["remedio_mais_vendido"]["nome"]}'
                        )
                        print(
                            f'Quantidade vendida: {estatisticas["remedio_mais_vendido"]["qtde_vendida"]}'
                        )
                        print(
                            f'Valor vendido: {round(estatisticas["remedio_mais_vendido"]["total_vendido"],2)}'
                        )
                        print(
                            f'Total de clientes atendidos: {estatisticas["clientes_atendidos"]}'
                        )
                        print(
                            f'Totais de remédios Quimioterápicos - Unidades: {estatisticas["vendas_quimioterapicos"]["qtde_vendida"]} - Valor: {round(estatisticas["vendas_quimioterapicos"]["total_vendido"],2)}'
                        )
                        print(
                            f'Totais de remédios Fitoterápicos - Unidades: {estatisticas["vendas_fitoterapicos"]["qtde_vendida"]} - Valor: {round(estatisticas["vendas_fitoterapicos"]["total_vendido"], 2)}'
                        )

                    except ExcecaoDocumentos as e:
                        print(str(e))
                        continue

                elif option_relatorio == "6":
                    condicao = False
        elif option == "7":
            data_hoje = datetime.strftime(
                datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
                "%d/%m/%Y %H:%M",
            )
            try:
                estatisticas = gerar_relatorio_diario(data_hoje)
                print("Métricas do dia\n\n")
                print(
                    f'Remédio mais vendido (unidades): {estatisticas["remedio_mais_vendido"]["nome"]}'
                )
                print(
                    f'Quantidade vendida: {estatisticas["remedio_mais_vendido"]["qtde_vendida"]}'
                )
                print(
                    f'Valor vendido: {round(estatisticas["remedio_mais_vendido"]["total_vendido"],2)}'
                )
                print(
                    f'Total de clientes atendidos: {estatisticas["clientes_atendidos"]}'
                )
                print(
                    f'Totais de remédios Quimioterápicos - Unidades: {estatisticas["vendas_quimioterapicos"]["qtde_vendida"]} - Valor: {round(estatisticas["vendas_quimioterapicos"]["total_vendido"],2)}'
                )
                print(
                    f'Totais de remédios Fitoterápicos - Unidades: {estatisticas["vendas_fitoterapicos"]["qtde_vendida"]} - Valor: {round(estatisticas["vendas_fitoterapicos"]["total_vendido"], 2)}'
                )

            except ExcecaoDocumentos as e:
                print(str(e))
                continue
            cond_init = False
