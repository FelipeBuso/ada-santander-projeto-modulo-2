from module.module import ler_arquivo, salvar_arquivo


class ExcessaoLaboratorios(Exception):
    def __init__(self, mensagem: str):
        self._erro = mensagem
        super().__init__(self._erro)


class Laboratorios:
    def __init__(self):
        self._cnpj = None
        self._nome = None
        self._endereco = None
        self._telefone = None
        self._cidade = None
        self._estado = None

    def _get_cnpj(self) -> str:
        return self._cnpj

    def _set_cnpj(self, cnpj: str) -> None:
        self._cnpj = cnpj

    nome = property(_get_cnpj, _set_cnpj)

    def _get_nome(self) -> str:
        return self._nome

    def _set_nome(self, nome: str) -> None:
        self._nome = nome

    nome = property(_get_nome, _set_nome)

    def _get_endereco(self) -> str:
        return self._endereco

    def _set_endereco(self, endereco: str) -> None:
        self._endereco = endereco

    endereco = property(_get_endereco, _set_endereco)

    def _get_telefone(self) -> str:
        return self._telefone

    def _set_telefone(self, telefone: str) -> None:
        self._telefone = telefone

    telefone = property(_get_telefone, _set_telefone)

    def _get_cidade(self) -> str:
        return self._cidade

    def _set_cidade(self, cidade: str) -> None:
        self._cidade = cidade

    cidade = property(_get_cidade, _set_cidade)

    def _get_estado(self) -> str:
        return self._estado

    def _set_estado(self, estado: str) -> None:
        self._estado = estado

    estado = property(_get_estado, _set_estado)

    def buscar_laboratorio(self, cnpj: str) -> dict:
        bd = ler_arquivo()
        bd_laboratorios = bd["bd_laboratorios"]
        if cnpj in bd_laboratorios and bd_laboratorios[cnpj]:
            laboratorio = bd_laboratorios[cnpj]
            self.cnpj = cnpj
            self.nome = laboratorio["nome"]
            self.endereco = laboratorio["endereco"]
            self.cidade = laboratorio["cidade"]
            self.estado = laboratorio["estado"]

            return {"cnpj": cnpj, **laboratorio}
        else:
            return "Laboratório não localizado"

    def cadastrar_laboratorio(
        self,
        cnpj: str,
        nome: str,
        endereco: str,
        telefone: str,
        cidade: str,
        estado: str,
    ) -> None:
        bd = ler_arquivo()
        bd_laboratorios = bd["bd_laboratorios"]
        if cnpj in bd_laboratorios:
            raise ExcessaoLaboratorios("laboratório já cadastrado")
        else:
            bd_laboratorios[cnpj] = {
                "nome": nome,
                "endereco": endereco,
                "telefone": telefone,
                "cidade": cidade,
                "estado": estado,
            }
            bd["bd_laboratorios"] = bd_laboratorios
            salvar_arquivo(bd)
            self.buscar_laboratorio(cnpj)
            return "Laboratorio cadastrado com sucesso"
