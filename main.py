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
from utils.utils import gerar_relatorio_diario, preencher_documento, ExcecaoDocumentos

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

        Selecione uma das opções:
    """


if __name__ == "__main__":
    # lê dados antes de iniciar operações

    while True:
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
                laboratorio_cnpj=laboratorio_cnpj,
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
                        medicamento_bd = preencher_documento(
                            medicamento_id, "bd_medicamentos"
                        )
                        if medicamento_bd and "necessita_receita" in medicamento_bd:
                            medicamento = MedicamentosQuimioterapicos()
                        else:
                            medicamento = MedicamentosFitoterapicos()
                    except ExcecaoDocumentos:
                        print("Medicamento não localizado")
                        continue

                    try:
                        medicamento_retornado = medicamento.buscar_medicamento(
                            medicamento_id
                        )
                        if "mensagem" in medicamento_retornado:
                            print(medicamento_retornado["mensagem"])
                    except ExcecaoMedicamentos as error:
                        print(str(error))
                    else:
                        medicamento_localizado = True

                qtde_venda = float(input("informe a quantidade desejada: "))

                venda.cadastro_vendas(
                    medicamento=medicamento,
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
            while True:
                option_relatorio = input(menu_relatorios)
                print("\n")

                if option == "1":
                    cliente = Clientes()
                    print(cliente.relatorio_clientes())

                elif option == "2":
                    medicamento_fitoterapico = MedicamentosFitoterapicos()
                    medicamento_fitoterapico.lista_medicamentos()

                elif option == "3":
                    medicamento_quimioterapico = MedicamentosQuimioterapicos()
                    medicamento_quimioterapico.lista_medicamentos

                elif option == "4":
                    medicamentos = Medicamentos()
                    medicamentos.lista_todos_medicamentos()

                elif option == "5":
                    data_hoje = datetime.strftime(
                        datetime.now().replace(
                            hour=0, minute=0, second=0, microsecond=0
                        ),
                        "%d/%m/%Y %H:%M",
                    )
                    gerar_relatorio_diario(data_hoje)
