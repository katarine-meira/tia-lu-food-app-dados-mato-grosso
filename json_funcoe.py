import json
import os

def carregar_json(caminho_arquivo):
    # Se o arquivo não existir, cria com estrutura apropriada
    if not os.path.exists(caminho_arquivo):
        # Para dados_pedidos.json - DEVE SER DICIONÁRIO
        if "dados_pedidos" in caminho_arquivo:
            estrutura_inicial = {
                "produtos": [],
                "pedidos_pendentes": [],
                "fila_preparo": [],
                "fila_rejeitados": [],
                "fila_cancelados": [],
                "contador_produto": 1,
                "contador_pedido": 1
            }
        else:
            # Para outros arquivos (árvores) - PODE SER LISTA
            estrutura_inicial = []
        
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            json.dump(estrutura_inicial, f, indent=4, ensure_ascii=False)
        return estrutura_inicial

    # Se já existir, carrega
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        conteudo = json.load(f)
        
        # Se for dados_pedidos e estiver vazio ou lista, corrige
        if "dados_pedidos" in caminho_arquivo and (not conteudo or isinstance(conteudo, list)):
            conteudo = {
                "produtos": [],
                "pedidos_pendentes": [],
                "fila_preparo": [],
                "fila_rejeitados": [],
                "fila_cancelados": [],
                "contador_produto": 1,
                "contador_pedido": 1
            }
            # Salva a correção
            with open(caminho_arquivo, "w", encoding="utf-8") as fw:
                json.dump(conteudo, fw, indent=4, ensure_ascii=False)
        
        return conteudo


def salvar_json(caminho_arquivo, dados):
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)