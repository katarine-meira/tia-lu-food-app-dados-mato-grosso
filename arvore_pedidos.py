from json_funcoe import carregar_json, salvar_json

CAMINHO_JSON_PEDIDOS = "arvore_pedidos_index.json"


class NoAVL:
    def __init__(self, id_pedido, dados_pedido):
        self.id = id_pedido
        self.dados = dados_pedido
        self.esquerda = None
        self.direita = None
        self.altura = 1


class ArvorePedido:
    def __init__(self):
        self.raiz = None
        self.carregar_pedidos()

    def altura(self, no):
        return 0 if no is None else no.altura

    def balanceamento(self, no):
        if no is None:
            return 0
        return self.altura(no.esquerda) - self.altura(no.direita)

    def rotacao_direita(self, y):
        x = y.esquerda
        t2 = x.direita
        x.direita = y
        y.esquerda = t2
        y.altura = 1 + max(self.altura(y.esquerda), self.altura(y.direita))
        x.altura = 1 + max(self.altura(x.esquerda), self.altura(x.direita))
        return x

    def rotacao_esquerda(self, x):
        y = x.direita
        t2 = y.esquerda
        y.esquerda = x
        x.direita = t2
        x.altura = 1 + max(self.altura(x.esquerda), self.altura(x.direita))
        y.altura = 1 + max(self.altura(y.esquerda), self.altura(y.direita))
        return y

    def inserir(self, raiz, id_pedido, dados_pedido):
        if raiz is None:
            return NoAVL(id_pedido, dados_pedido)

        if id_pedido < raiz.id:
            raiz.esquerda = self.inserir(raiz.esquerda, id_pedido, dados_pedido)
        elif id_pedido > raiz.id:
            raiz.direita = self.inserir(raiz.direita, id_pedido, dados_pedido)
        else:
            raiz.dados = dados_pedido
            return raiz

        raiz.altura = 1 + max(self.altura(raiz.esquerda), self.altura(raiz.direita))
        bal = self.balanceamento(raiz)

        if bal > 1 and id_pedido < raiz.esquerda.id:
            return self.rotacao_direita(raiz)
        if bal < -1 and id_pedido > raiz.direita.id:
            return self.rotacao_esquerda(raiz)
        if bal > 1 and id_pedido > raiz.esquerda.id:
            raiz.esquerda = self.rotacao_esquerda(raiz.esquerda)
            return self.rotacao_direita(raiz)
        if bal < -1 and id_pedido < raiz.direita.id:
            raiz.direita = self.rotacao_direita(raiz.direita)
            return self.rotacao_esquerda(raiz)

        return raiz
    
    def adicionar_pedido(self, id_pedido, dados_pedido):
        self.raiz = self.inserir(self.raiz, id_pedido, dados_pedido)
        self.salvar_pedidos()

    def buscar(self, raiz, id_pedido):
        if raiz is None:
            return None
        if id_pedido == raiz.id:
            return raiz.dados
        if id_pedido < raiz.id:
            return self.buscar(raiz.esquerda, id_pedido)
        return self.buscar(raiz.direita, id_pedido)

    def carregar_pedidos(self):
        dados = carregar_json(CAMINHO_JSON_PEDIDOS)
        
        if not isinstance(dados, list):
            dados = []
        
        self.raiz = None
        for pedido in dados:
            self.raiz = self.inserir(self.raiz, pedido["id_pedido"], pedido["dados"])

    def salvar_pedidos(self):
        dados = []
        self._inordem_json(self.raiz, dados)
        salvar_json(CAMINHO_JSON_PEDIDOS, dados)

    def _inordem_json(self, no, lista):
        if no is not None:
            self._inordem_json(no.esquerda, lista)
            lista.append({"id_pedido": no.id, "dados": no.dados})
            self._inordem_json(no.direita, lista)

  