import json
import os

def carregar_json(caminho_arquivo):
    # Se ainda não tiver ele vai gerar um arq vazio
    if not os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)
        return []

    # Se ja tiver vai carregar
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_json(caminho_arquivo, dados):
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)