from arvore_itens import ArvoreAVL
from arvore_pedidos import ArvorePedido

arvoreItens = ArvoreAVL()
arvorePedidos = ArvorePedido()

# Calcula contador de produtos
contador_produto = 0
itens = arvoreItens.listar_em_ordem()
if itens:
    contador_produto = max(int(no['valor']['codigo'][3:]) for no in itens) + 1

# Calcula contador de pedidos
contador_pedido = 0
pedidos = arvorePedidos.listar_em_ordem()
if pedidos:
    contador_pedido = max(int(no['dados']['id_pedido'][3:]) for no in pedidos) + 1


def get_pedidos():
    return arvorePedidos.listar_em_ordem()

def get_pedidos_por_status(status):
    pedidos = arvorePedidos.listar_em_ordem()
    return [
        p["dados"]
        for p in pedidos
        if p["dados"].get("status") == status
    ]

def bucket_sort(arr, key=lambda x: x):
    if len(arr) <= 1:
        return arr
    min_val = min(arr, key=key)
    max_val = max(arr, key=key)
    bucket_count = len(arr)
    buckets = [[] for _ in range(bucket_count)]
    for item in arr:
        index = int((key(item) - key(min_val)) / (key(max_val) - key(min_val)) * (bucket_count - 1))
        buckets[index].append(item)
    for i in range(bucket_count):
        buckets[i] = sorted(buckets[i], key=key)
    sorted_arr = []
    for bucket in buckets:
        sorted_arr.extend(bucket)
    return sorted_arr

def sair():
    escolhaSair = """
    ============= DESEJA SAIR? ===============
    
    [1] Não
    [0] Sair
    => """
    return input(escolhaSair)

def pergunta(val):
    opcao = f"""
    ============= ESCOLHA ===============
    
    [1] {val}
    [0] Sair
    => """
    return input(opcao)

def escolhaMenu():
    escolhaDoMenu = """
    ============= ESCOLHA O MENU ===============
    
    [1] Menu de Itens
    [2] Menu de Pedidos
    [0] Sair
    => """
    return input(escolhaDoMenu)

def menuItens():
    menu = """
    ================== MENU ITENS ==================
    
    [1] Cadastrar Item 
    [2] Atualizar Item
    [3] Consultar Itens
    [4] Detalhes do Item
    [0] Sair
    => """
    return input(menu)

def menuConsultas():
    menu = """
    ================== MENU CONSULTAS ==================
    
    [1] Exibir Pedidos 
    [2] Filtro por Status
    [3] Relatório de Vendas
    [0] Sair
    => """
    return input(menu)

def menuPedidos():
    menu = """
    ================= MENU PEDIDOS =================
    
    [1] Criar Pedido 
    [2] Processar Pedidos Pendentes
    [3] Atualizar Status de Pedido
    [4] Cancelar Pedido
    [5] Consultas
    [0] Sair
    => """
    return input(menu)

clientes = []

def cadastroCliente():
    cliente = {}
    nome = input("Digite seu nome de usuário: ")
    cliente["nome"] = nome
    clientes.append(cliente)
    print(f"Bem-vindo {nome}!")

def criarCliente():
    if clientes:
        while True:
            print("\nEscolha o usuário\n")
            for i, cliente in enumerate(clientes):
                print(f"[{i}] - {cliente['nome']}")
            print(f"[{len(clientes)}] - Criar novo cliente")
            try:
                opcao = int(input("\n>>: "))
                if 0 <= opcao < len(clientes):
                    print(f"Bem-vindo {clientes[opcao]['nome']}!")
                    break
                elif opcao == len(clientes):
                    cadastroCliente()
                    break
                else:
                    print("Opção inválida!")
            except ValueError:
                print("Digite um número válido!")
                continue
    else:
        while True:
            print("\nAinda não existem clientes cadastrados.")
            menu = pergunta("Criar cliente")
            match menu:
                case '1':
                    cadastroCliente()
                    return
                case '0':
                    menuPedidos()
                case _:
                    print("\tOpção inválida")

def cadastrarItem():
    global contador_produto

    print("\n===== CADASTRAR ITEM =====\n")

    nome = input("Digite o nome do produto: ")
    descricao = input("Digite a descrição do produto: ")

    while True:
        try:
            preco = float(input("Digite o preço do produto (use '.' para decimais): "))
            break
        except ValueError:
            print("Valor inválido. Tente novamente!")

    while True:
        try:
            estoque = int(input("Digite a quantidade no estoque: "))
            break
        except ValueError:
            print("Valor inválido. Tente novamente!")

    # Gera o código do produto
    codigo = f"PRO{contador_produto:04d}"
    contador_produto += 1

    # Item que será salvo
    item = {
        "nome": nome,
        "descricao": descricao,
        "codigo": codigo,
        "preco": preco,
        "estoque": estoque
    }

    # Adiciona o item na AVL
    arvoreItens.adicionar_item(codigo, item)
    print("\nProduto cadastrado com sucesso!\n")


def atualizarItens():
    itens = arvoreItens.listar_em_ordem()
    if not itens:
        print("\nO sistema ainda não possui um item cadastrado.")
        return

    print("\n=== ITENS CADASTRADOS ===")
    for i, item in enumerate(itens):
        print(f"[{i}] {item['valor']['nome']} (R${item['valor']['preco']} - estoque: {item['valor']['estoque']})")

    while True:
        try:
            indice = int(input("\nDigite o número do item a atualizar: "))
            if 0 <= indice < len(itens):
                break
            else:
                print("Item inválido!")
        except ValueError:
            print("Digite um número válido!")

    item = itens[indice]['valor']  # pegamos o valor do nó
    nome_atual = input(f"Nome atual [{item['nome']}]: ") or item['nome']
    descricao_atual = input(f"Descrição atual [{item['descricao']}]: ") or item['descricao']
    preco_atual = input(f"Preço atual [{item['preco']}]: ") or item['preco']
    estoque_atual = input(f"Estoque atual [{item['estoque']}]: ") or item['estoque']

    item.update({
        "nome": nome_atual,
        "descricao": descricao_atual,
        "preco": float(preco_atual),
        "estoque": int(estoque_atual)
    })

    # Atualiza na AVL
    arvoreItens.adicionar_item(itens[indice]['cod_item'], item)
    print("\nItens atualizados!")

def consultarItens():
    itens = arvoreItens.listar_em_ordem()

    if not itens:
        print("\nNenhum item cadastrado.")
        return

    print("\n===== ITENS DISPONÍVEIS =====")

    for i, item in enumerate(itens):
        valor = item["valor"]
        print(f"[{i}] {valor['nome']} (R${valor['preco']} - Descrição: {valor['descricao']})")

def detalhesItens():
    itens = arvoreItens.listar_em_ordem()

    if itens:
        print("\n===== Detalhes do Item =====\n")
        for no in itens:
            item = no['valor']
            print(f"Nome: {item['nome']}")
            print(f"Descrição: {item['descricao']}")
            print(f"Código: {item['codigo']}")
            print(f"Preço: R$ {item['preco']:.2f}")
            print(f"Estoque: {item['estoque']}\n")
    else:
        print("\nNenhum item cadastrado.")

def criarPedido():
    global contador_pedido
    itens = arvoreItens.listar_em_ordem()  # Pega todos os itens da AVL

    if not itens:
        print("\nNenhum produto no sistema.")
        return

    print("\n===== ITENS DISPONÍVEIS =====")
    for i, no in enumerate(itens):
        item = no['valor']
        print(f"[{i}] {item['nome']} (R${item['preco']} - estoque: {item['estoque']})")
    print(f"[{len(itens)}] Sair")

    pedido_usuario = {
        "id_pedido": f"PED{contador_pedido:04d}",
        "produtos": [],
        "status": "Aguardando Aprovação"
    }
    contador_pedido += 1

    while True:
        try:
            indice = int(input("\nDigite o número do produto que deseja: "))
        except ValueError:
            print("Digite um número válido.")
            continue

        if indice == len(itens):
            print("\nPedido cancelado.")
            return

        if 0 <= indice < len(itens):
            item = itens[indice]['valor']
            if item['estoque'] > 0:
                item['estoque'] -= 1  # Atualiza estoque direto na AVL
                arvoreItens.adicionar_item(item['codigo'], item)

                pedido = {
                    "nome": item['nome'],
                    "codigo": item['codigo'],
                    "preco": item['preco'],
                }
                pedido_usuario["produtos"].append(pedido)

                print("\nSua lista atual de pedidos:")
                for p in pedido_usuario["produtos"]:
                    print(f"- {p['nome']}")

                while True:
                    match pergunta("Adicionar mais produtos"):
                        case '1':
                            # Mostra os itens novamente
                            itens = arvoreItens.listar_em_ordem()
                            print("\n===== ITENS DISPONÍVEIS =====")
                            for i, no in enumerate(itens):
                                item_temp = no['valor']
                                print(f"[{i}] {item_temp['nome']} (R${item_temp['preco']} - estoque: {item_temp['estoque']})")
                            print(f"[{len(itens)}] Sair")
                            break
                        case '0':
                            if pedido_usuario["produtos"]:
                                arvorePedidos.adicionar_pedido(
                                    pedido_usuario["id_pedido"],
                                    pedido_usuario
                                )
                                print("\nPedido enviado para aprovação!")
                            else:
                                print("\nNenhum produto adicionado, pedido cancelado.")
                            return
                        case _:
                            print("\nOpção inválida")
            else:
                print(f"\n{item['nome']} está sem estoque.")
                while True:
                    match sair():
                        case '1':
                            break
                        case '0':
                            print("\nPedido cancelado.")
                            return
                        case _:
                            print("Opção inválida.")
        else:
            print("\nÍndice inválido.")

def ProcessarPedidos():
    # Carrega todos os pedidos da AVL
    pedidos = arvorePedidos.listar_em_ordem()

    # Filtra apenas os que estão "Aguardando Aprovação"
    pedidos_pendentes = [p["dados"] for p in pedidos if p["dados"].get("status") == "Aguardando Aprovação"]

    if not pedidos_pendentes:
        print("\nNenhum pedido novo no sistema.")
        return

    while pedidos_pendentes:
        pedido = pedidos_pendentes[0]
        print("\n===== Pedido pendente =====")
        print(f"Código do pedido - {pedido['id_pedido']} (Status: {pedido['status']})")
        for produto in pedido['produtos']:
            print(f"   - {produto['nome']} (id: {produto['codigo']})")
        print(f"\n===== Pedido {pedido['id_pedido']} =====")
        print("[1] Aceitar (pagamento)")
        print("[2] Rejeitar")
        print("[0] Sair")
        opcao = input("\n>>: ")

        if opcao == '1':
            valor_total = sum(produto['preco'] for produto in pedido['produtos'])
            valor_final_pago = valor_total
            cupom = input("Deseja utilizar o cupom de desconto do dia? [s ou n]: ").lower()
            if cupom == 's':
                desconto = valor_total / 10
                valor_final_pago = valor_total - desconto
            pedido['valor_final_pago'] = valor_final_pago
            pedido['status'] = "Aceito"
            
            # Atualiza estoque somente quando pedido é aceito
            # for produto_pedido in pedido['produtos']:
            #     codigo = produto_pedido['codigo']
            #     no_item = arvoreItens.buscar(codigo)  # Buscar nó na AVL
            #     if no_item:
            #         no_item['valor']['estoque'] -= 1
            #         arvoreItens.adicionar_item(codigo, no_item['valor'])

            # Atualiza na AVL
            arvorePedidos.adicionar_pedido(pedido['id_pedido'], pedido)

            print(f"\nPedido {pedido['id_pedido']} aceito! Valor final: R$ {valor_final_pago:.2f}")

        elif opcao == '2':
            pedido['status'] = "Rejeitado"

            # Atualiza na AVL
            arvorePedidos.adicionar_pedido(pedido['id_pedido'], pedido)

            print(f"\nPedido {pedido['id_pedido']} rejeitado!")

        elif opcao == '0':
            return
        else:
            print("\nOpção inválida")

        # Remove o pedido processado da lista temporária
        pedidos_pendentes.pop(0)

filaCancelados =[]

def atualizarStatusPedido():
    fluxoStatus = [
        'Em preparo',
        'Pedido pronto',
        'Aguardando o entregador',
        'Seu pedido saiu para entrega',
        'Pedido entregue'
    ]

    # Carrega todos os pedidos da AVL
    pedidos = arvorePedidos.listar_em_ordem()
    
    # Filtra apenas pedidos em andamento (status que podemos atualizar)
    pedidos_em_processo = [
        item["dados"] for item in pedidos 
        if item["dados"].get("status") in fluxoStatus or item["dados"].get("status") == "Aceito"
    ]

    if not pedidos_em_processo:
        print("\nNENHUM PEDIDO A SER ATUALIZADO!")
        return

    print("\nPEDIDOS EM PROCESSO: \n")
    for pedido in pedidos_em_processo:
        print(f"ID do Pedido - {pedido['id_pedido']} (Status: {pedido['status']})")
        for produto in pedido['produtos']:
            print(f"   - {produto['nome']}")
        print("______________________________________________")

    numeroPedido = input("Nº ID do pedido que deseja atualizar: ")

    for pedido in pedidos_em_processo:
        if pedido['id_pedido'] == numeroPedido:
            print(f"\nPedido encontrado! ID: {pedido['id_pedido']}")      

            status_atual = pedido.get('status', '')
            if status_atual in fluxoStatus:
                indice = fluxoStatus.index(status_atual)
                if indice < len(fluxoStatus) - 1:
                    pedido['status'] = fluxoStatus[indice + 1]
                else:
                    print("\nEste pedido já foi atualizado!")
                    return
            else:
                # Caso esteja em "Aceito" ou outro status inicial
                pedido['status'] = fluxoStatus[0]

            # Atualiza na AVL
            arvorePedidos.adicionar_pedido(pedido['id_pedido'], pedido)

            print(f"Status do pedido {pedido['id_pedido']} atualizado para: {pedido['status']}")
            return

    print("\nPedido não encontrado!")

def cancelarPedido():
    # Carrega todos os pedidos da AVL
    pedidos = arvorePedidos.listar_em_ordem()

    # Filtra apenas os pedidos canceláveis
    cancelaveis = [
        pedido["dados"] 
        for pedido in pedidos 
        if pedido["dados"].get("status") in ("Aguardando Aprovação", "Aceito")
    ]

    if not cancelaveis:
        print("\nNão há pedidos canceláveis no momento.")
        return

    print("\n====== Pedidos Canceláveis ======")
    for i, pedido in enumerate(cancelaveis):
        nomes_produtos = ", ".join([produto['nome'] for produto in pedido['produtos']])
        print(f"[{i}] {nomes_produtos} | Status: {pedido['status']}")

    try:
        escolha = int(input("\nDigite o número do pedido para cancelar: "))
        pedido = cancelaveis[escolha]
    except (ValueError, IndexError):
        print("Opção inválida.")
        return

    # Atualiza o status para "Cancelado" e salva na AVL
    pedido["status"] = "Cancelado"

    for produto in pedido["produtos"]:
        codigo = produto["codigo"]
        no_item = arvoreItens.buscar(codigo)
        if no_item:
            no_item["valor"]["estoque"] += 1  # devolve 1 unidade ao estoque
            arvoreItens.adicionar_item(codigo, no_item["valor"])  # atualiza AVL

    arvorePedidos.adicionar_pedido(pedido["id_pedido"], pedido)

    print("\nPedido cancelado com sucesso!")

def exibirPedidos():
    print("\n========= PEDIDOS ==========")

    # carregar todos os pedidos ordenados da AVL
    pedidos = arvorePedidos.listar_em_ordem()

    if not pedidos:
        print("Nenhum pedido encontrado.")
        return

    # organizar por grupos
    grupos = {
        "Aguardando Aprovação": [],
        "Aceito": [],
        "Em preparo": [],
        "Pedido pronto": [],
        "Aguardando o entregador": [],
        "Seu pedido saiu para entrega": [],
        "Pedido entregue": [],
        "Rejeitado": [],
        "Cancelado": []
    }

    # separar pedidos conforme o status
    for item in pedidos:
        pedido = item["dados"]  # pois AVL salva {"id_pedido": x, "dados": {...}}

        status = pedido.get("status", "Desconhecido")

        # cria grupo se necessário
        if status not in grupos:
            grupos[status] = []

        grupos[status].append(pedido)

    # exibir cada grupo
    for nome, lista in grupos.items():
        if lista:  # só exibe se tiver pedidos
            print(f"\n===== {nome.upper()} =====")
            for pedido in lista:
                nomes = ", ".join([p["nome"] for p in pedido["produtos"]])
                valor = pedido.get("valor_final_pago", "N/A")
                if valor == "N/A":
                    produtos = pedido.get("produtos")
                    valor = 0;
                    for item in produtos:
                        valor += item.get("preco")
                print(f"ID: {pedido['id_pedido']} | Produtos: {nomes} | Status: {pedido['status']} | Valor: {valor}")

def filtroStatus():
    print("\n========= FILTRAR PEDIDO POR STATUS ==========")
    status_desejado = input("Digite o status que deseja filtrar: ").strip().lower()

    # Pega todos os pedidos da AVL em ordem
    pedidos = arvorePedidos.listar_em_ordem()
    
    # Filtra pelo status
    filtrado = [
        p["dados"] 
        for p in pedidos 
        if p["dados"].get("status", "").lower() == status_desejado
    ]

    if not filtrado:
        print("\nNenhum pedido encontrado.")
        return

    print(f"\nPedidos com status '{status_desejado}':")
    for pedido in filtrado:
        nomes_produtos = ", ".join([produto["nome"] for produto in pedido["produtos"]])
        valor = pedido.get("valor_final_pago", "N/A")
        print(f"ID: {pedido['id_pedido']} | Produtos: {nomes_produtos} | Valor total: {valor}")

def relatorioVendas():
    totalFaturamento = 0

    # Carrega todos os pedidos da AVL
    pedidos = arvorePedidos.listar_em_ordem()

    # Considera apenas pedidos que estão em status de venda/entrega
    status_validos = (
        "Aceito",
        "Em preparo",
        "Pedido pronto",
        "Aguardando o entregador",
        "Seu pedido saiu para entrega",
        "Pedido entregue"
    )

    for item in pedidos:
        pedido = item["dados"]
        if pedido.get("status") in status_validos:
            totalFaturamento += pedido.get("valor_final_pago", 0)

    print("\n===== RELATÓRIO DE FATURAMENTO =====")
    print(f"\nFaturamento total: R$ {totalFaturamento:.2f}")

while True:
    match escolhaMenu():
        case '1':
            while True:
                match menuItens():
                    case '1':
                        cadastrarItem()
                    case '2':
                        atualizarItens()
                    case '3':
                        consultarItens()
                    case '4':
                        detalhesItens()
                    case '0':
                        break
                    case _:
                        print("Opção inválida")
        case '2':
            while True:
                match menuPedidos():
                    case '1':
                        criarCliente()
                        criarPedido()
                    case '2':
                        criarCliente()
                        ProcessarPedidos()
                    case '3':
                        criarCliente()
                        atualizarStatusPedido()
                    case '4':
                        criarCliente()
                        cancelarPedido()
                    case '5':
                        criarCliente()
                        while True:
                            match menuConsultas():
                                case '1':
                                    exibirPedidos()
                                case '2':
                                    filtroStatus()
                                case'3':
                                    relatorioVendas()
                                case '0':
                                    break
                                case _:
                                    print("Opção inválida")
                    case '0':
                        break
                    case _:
                        print("Opção inválida")
        case '0':
            break
        case _:
            print("Opção inválida")
