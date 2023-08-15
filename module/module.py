import json


def ler_arquivo(nome_arquivo="./banco_dados/db.json") -> None:
    try:
        with open(nome_arquivo, "r") as arquivo:
            return json.loads(arquivo.read())
    except Exception as error:
        print(str(error))
        return None


def salvar_arquivo(novo_arquivo: dict, nome_arquivo="./banco_dados/db.json") -> None:
    try:
        with open(nome_arquivo, "w") as arquivo:
            arquivo.write(json.dumps(novo_arquivo, ensure_ascii=False))
    except Exception as error:
        print(str(error))
    
    return None
