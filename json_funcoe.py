import json
import os

def carregar_json(caminho_arquivo):
    # Se o arquivo não existir, cria com estrutura apropriada
    if not os.path.exists(caminho_arquivo):
        estrutura_inicial = []
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            json.dump(estrutura_inicial, f, indent=4, ensure_ascii=False)
        return estrutura_inicial

    # Se já existir, carrega
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        conteudo = json.load(f)
        return conteudo


def salvar_json(caminho_arquivo, dados):
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)