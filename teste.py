def escolhaMenu():
    escolhaDoMenu = """
    ============= ESCOLHA O MENU ===============
    
    [1] \tMenu de Itens
    [0] \tSair
    
    => """
    
    return input(escolhaDoMenu)

def menuItens():
    menu = """
    ================== MENU ITENS ==================
    
    [1] \tRegistrar Item 
    [0] \tSair

    => """
    return input(menu)


produtos = []
def registro():
    produto = {}
    nome = input("Digite seu nome: ")
    numero = input("Digite seu numero: ")
    produto["nome"] = nome
    produto["numero"] = numero
    produtos.append(produto)

    
     
while True:
    match escolhaMenu():
        case '1':
            while True:
                match menuItens():
                    case '1':
                        registro()
                        print(produtos)
                    case '0':
                        break
                    case _:
                        print("Opção inválida")
        case '0':
            break
        case _:
            print("Opção inválida")