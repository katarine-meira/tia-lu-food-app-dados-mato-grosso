from json_funcoes import carregar_json, salvar_json

data = carregar_json()

itemCadastrado = data["produtos"]
pedidosPendentes = data["pedidos_pendentes"]
filaPreparo = data["fila_preparo"]
filaRejeitados = data["fila_rejeitados"]
filaCancelados = data["fila_cancelados"]

contador_produto = data["contador_produto"]
contador_pedido = data["contador_pedido"]

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
    nome = input("Digite o nome do produto: ")
    descricao = input("Digite a descrição do produto: ")
    while True:
        try:
            preco = float(input("Digite o preço do produto (use '.' para decimais): "))
            break
        except ValueError:
            print("Digite o valor usando '.'(ponto)")
    while True:
        try:
            estoque = int(input("Digite a quantidade do estoque: "))
            break
        except ValueError:
            print("Digite um número válido!")
    codigo = f"PRO{contador_produto:04d}"
    contador_produto += 1
    item = {
        "nome": nome,
        "descricao": descricao,
        "codigo": codigo,
        "preco": preco,
        "estoque": estoque
    }
    itemCadastrado.append(item)
    data["contador_produto"] = contador_produto
    salvar_json(data)
    print("\nProduto cadastrado com sucesso!\n")

def atualizarItens():
    if not itemCadastrado: 
        print("\nO sistema ainda não possui um item cadastrado.")
        return
    print("\n=== ITENS CADASTRADOS ===")
    for i, item in enumerate(itemCadastrado):
        print(f"[{i}] {item['nome']} (R${item['preco']} - estoque: {item['estoque']})")
    while True:
        try:
            indice = int(input("\nDigite o número do item a atualizar: "))
            if 0 <= indice < len(itemCadastrado):
                break
            else:
                print("Item inválido!")
        except ValueError:
            print("Digite um número válido!")
    item = itemCadastrado[indice]
    nome_atual = input(f"Nome atual [{item['nome']}]: ") or item['nome']
    descricao_atual = input(f"Descrição atual [{item['descricao']}]: ") or item['descricao']
    preco_atual = input(f"Preço atual [{item['preco']}]:") or item['preco']
    estoque_atual = input(f"Estoque atual [{item['estoque']}]:") or item['estoque']
    item.update({
        "nome": nome_atual,
        "descricao": descricao_atual,
        "preco": float(preco_atual),
        "estoque": int(estoque_atual)
    })
    salvar_json(data)
    print("\nItens atualizados!")

def consultarItens():
    if itemCadastrado:
        print("\n===== Itens Disponíveis =====")
        itens_ordenados = bucket_sort(itemCadastrado, key=lambda x: int(x['codigo'][3:]))
        for i, item in enumerate(itens_ordenados):
            print(f"[{i}] {item['nome']} (R${item['preco']} - Descrição: {item['descricao']})")
    else:
        print("\nNenhum item cadastrado.")

def detalhesItens():
    if itemCadastrado:
        print("\n===== Detalhes do Item =====\n")
        for item in itemCadastrado:
            print(f"Nome: {item['nome']}")
            print(f"Descrição: {item['descricao']}")
            print(f"Código: {item['codigo']}")
            print(f"Preço: R$ {item['preco']:.2f}")
            print(f"Estoque: {item['estoque']}\n")
    else:
        print("\nNenhum item cadastrado.")

pedidosPendentes = []

def criarPedido():
    global contador_pedido
    if not itemCadastrado:
        print("\nNenhum produto no sistema.")
        return
    consultarItens()
    print(f"[{len(itemCadastrado)}] Sair")
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
        if indice == len(itemCadastrado):
            print("\nPedido cancelado.")
            return
        if 0 <= indice < len(itemCadastrado):
            if itemCadastrado[indice]['estoque'] > 0:
                itemCadastrado[indice]['estoque'] -= 1
                pedido = {
                    "nome": itemCadastrado[indice]['nome'],
                    "codigo": itemCadastrado[indice]['codigo'],
                    "preco": itemCadastrado[indice]['preco'],
                }
                pedido_usuario["produtos"].append(pedido)
                print("\nSua lista atual de pedidos:")
                for p in pedido_usuario["produtos"]:
                    print(f"- {p['nome']}")
                while True:
                    match pergunta("Adicionar mais produtos"):
                        case '1':
                            consultarItens()
                            break
                        case '0':
                            if pedido_usuario["produtos"]:
                                pedidosPendentes.append(pedido_usuario)
                                data["pedidos_pendentes"] = pedidosPendentes
                                salvar_json(data)
                                print("\nPedido enviado para aprovação!")
                            else:
                                print("\nNenhum produto adicionado, pedido cancelado.")
                            return 
                        case _:
                            print("\nOpção inválida")
            else:
                print(f"\n{itemCadastrado[indice]['nome']} está sem estoque.")
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

filaPreparo = []
filaRejeitados = []

def ProcessarPedidos():
    if pedidosPendentes:
        while pedidosPendentes:
            pedido = pedidosPendentes[0]
            print("\n===== Pedido pendente =====")
            print(f"Código do pedido - {pedido['id_pedido']} (Status: {pedido['status']})")
            for produto in pedido['produtos']:
                print(f"   - {produto['nome']} (id: {produto['codigo']})")
            print(f"\n===== Pedido {pedido['produtos'][0]['codigo']} =====")
            print("[1] Aceitar (pagamento)")
            print("[2] Rejeitar")
            print("[0] Sair")
            opcao = input("\n>>: ")

            if opcao == '1':
                valor_total = 0
                for produto in pedido['produtos']:
                    valor_total += produto['preco']
                valor_final_pago = valor_total
                cupom = input("Deseja utilizar o cupom de desconto do dia?[s ou n]: ").lower()
                if cupom == 's':
                    desconto = valor_total / 10
                    valor_final_pago = valor_total - desconto
                    print(f"\nValor total pago: {valor_final_pago:.2f}")
                else:
                    print(f"\nValor total pago: {valor_total:.2f}")
                    valor_final_pago = valor_total
                pedido['valor_final_pago'] = valor_final_pago
                pedido['status'] = "Aceito"
                linha = pedidosPendentes.pop(0)
                filaPreparo.append(linha)
                data["fila_preparo"] = filaPreparo
                salvar_json(data)
                print(f"\nPedido {pedido['id_pedido']} aceito!")
            elif opcao == '2':
                pedido['status'] = "Rejeitado"
                linha = pedidosPendentes.pop(0)
                filaRejeitados.append(linha)
                data["fila_rejeitados"] = filaRejeitados
                salvar_json(data)
                print("\nPedido cancelado!")
            elif opcao == '0':
                return
            else:
                print("\nOpção inválida")
    else:
        print("\nNenhum pedido novo no sistema.")

filaCancelados =[]

def atualizarStatusPedido():
    fluxoStatus = [
        'Em preparo',
        'Pedido pronto',
        'Aguardando o entregador',
        'Seu pedido saiu para entrega',
        'Pedido entregue'
    ]
    print("\nPEDIDOS EM PROCESSO: \n")
    for pedido in filaPreparo:
        print(f"ID do Pedido - {pedido['id_pedido']} (Status: {pedido['status']})")
        for produto in pedido['produtos']:
            print(f"   - {produto['nome']}")
        print("______________________________________________")
    if not filaPreparo:
        print("NENHUM PEDIDO A SER ATUALIZADO!")
        return
    numeroPedido = input(f"Nº ID do pedido que deseja atualizar: ")
    for pedido in filaPreparo:
        if pedido['id_pedido'] == numeroPedido:
            print(f"\nPedido encontrado!")
            print(f"id_pedido: {pedido['id_pedido']}")      
            if pedido['status'] in fluxoStatus:
                indice = fluxoStatus.index(pedido['status'])
                if indice < len(fluxoStatus) - 1:
                    pedido['status'] = fluxoStatus[indice + 1]
                else:
                    print("\nEste pedido já foi atualizado!")
                    return
            else:
                pedido['status'] = fluxoStatus[0]
            data["fila_preparo"] = filaPreparo
            salvar_json(data)
            print(f"Status do pedido {pedido['id_pedido']} atualizado para: {pedido['status']}")
            return
    print("\nPedido não encontrado!")

def cancelarPedido():
    global pedidosPendentes, filaPreparo, filaCancelados
    cancelaveis = []
    for nome_lista, lista_pedidos in [("Pendentes", pedidosPendentes), ("Fila de Preparo", filaPreparo)]:
        for pedido in lista_pedidos:
            status = pedido.get("status", "")
            if status in ("Aguardando Aprovação", "Aceito"):
                cancelaveis.append((nome_lista, pedido))
    if not cancelaveis:
        print("\nNão há pedidos canceláveis no momento.")
        return
    print("\n====== Pedidos Canceláveis ======")
    for i, (nome_lista, pedido) in enumerate(cancelaveis):
        nomes_produtos = ", ".join([produto['nome'] for produto in pedido['produtos']])
        print(f"[{i}] {nomes_produtos} | Status: {pedido['status']}")
    try: 
        escolha = int(input("\nDigite o número do pedido para cancelar: "))
        nome_lista, pedido = cancelaveis[escolha]
    except (ValueError, IndexError):
        print("Opção inválida.")
        return
    if pedido in pedidosPendentes:
        pedidosPendentes.remove(pedido)
    elif pedido in filaPreparo:
        filaPreparo.remove(pedido)
    pedido["status"] = "Cancelado"
    filaCancelados.append(pedido)
    data["fila_cancelados"] = filaCancelados
    salvar_json(data)
    print("\nPedido cancelado com sucesso!")

def exibirPedidos():
    print("\n========= PEDIDOS: ==========")
    if not (pedidosPendentes or filaPreparo or filaRejeitados or filaCancelados):
        print("Nenhum pedido encontrado.")
        return
    def mostrar_lista (nome, lista):
        if lista:
            print(f"\n ==== {nome} ====")
            pedidos_ordenados = bucket_sort(lista, key=lambda x: int(x['id_pedido'][3:]))
            for pedido in pedidos_ordenados:
                nome_produto = ", ".join([p['nome'] for p in pedido ['produtos']])
                total = pedido.get("valor_final_pago", "N/A")
                print(f"ID: {pedido['id_pedido']}  Produto: {nome_produto} | Status: {pedido['status']} | valor: {total}")
    mostrar_lista("Pendentes", pedidosPendentes)
    mostrar_lista("Em preparo", filaPreparo)
    mostrar_lista("Rejeitados", filaRejeitados)
    mostrar_lista("Cancelados", filaCancelados)

def filtroStatus():
    print("\n========= FILTRAR PEDIDO POR STATUS ==========")
    status = input("Digite o status que deseja filtrar: ").strip().lower()
    fila_pedido = pedidosPendentes + filaCancelados + filaPreparo + filaRejeitados
    filtrado = [p for p in fila_pedido if p['status'].lower() == status]
    if not filtrado:
        print("\nNenhum pedido encontrado.")
    else: 
        print(f"\nPedidos com status '{status}':")
        for pedido in filtrado:
            nome_produto = ", ".join([p['nome'] for p in pedido['produtos']])
            total = pedido.get("valor_final_pago", "N/A")
            print(f"ID: {pedido['id_pedido']} | Produtos: {nome_produto} | Valor total: {total}")

def relatorioVendas():
    totalFaturamento = 0
    for pedido in filaPreparo:
        if pedido['status'] in ("Aceito", "Em preparo", "Pedido pronto!", "Aguardando o entregador!", "Seu pedido saiu para entrega!", "Pedido entregue!"):
            totalFaturamento += pedido['valor_final_pago']
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
