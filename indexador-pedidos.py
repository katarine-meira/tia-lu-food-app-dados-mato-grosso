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

    def altura(self, no):
        return 0 if no is None else no.altura

    def fatorBalanceamento(self, no):
        if no is None:
            return 0
        return self.altura(no.esquerda) - self.altura(no.direita)

    def rotaDireita(self, y):
        x = y.esquerda
        T2 = x.direita
        x.direita = y
        y.esquerda = T2
        y.altura = 1 + max(self.altura(y.esquerda), self.altura(y.direita))
        x.altura = 1 + max(self.altura(x.esquerda), self.altura(x.direita))
        return x

    def rotaEsquerda(self, x):
        y = x.direita
        T2 = y.esquerda
        y.esquerda = x
        x.direita = T2
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
        balance = self.fatorBalanceamento(raiz)

        if balance > 1 and id_pedido < raiz.esquerda.id:
            return self.rotaDireita(raiz)
        if balance < -1 and id_pedido > raiz.direita.id:
            return self.rotaEsquerda(raiz)
        if balance > 1 and id_pedido > raiz.esquerda.id:
            raiz.esquerda = self.rotaEsquerda(raiz.esquerda)
            return self.rotaDireita(raiz)
        if balance < -1 and id_pedido < raiz.direita.id:
            raiz.direita = self.rotaDireita(raiz.direita)
            return self.rotaEsquerda(raiz)

        return raiz

    def adicionarPedido(self, id_pedido, dados_pedido):
        self.raiz = self.inserir(self.raiz, id_pedido, dados_pedido)

    def buscar(self, raiz, id_pedido):
        if raiz is None:
            return None
        if id_pedido == raiz.id:
            return raiz.dados
        if id_pedido < raiz.id:
            return self.buscar(raiz.esquerda, id_pedido)
        return self.buscar(raiz.direita, id_pedido)

    def inordem(self, raiz):
        if raiz is not None:
            self.inordem(raiz.esquerda)
            print(raiz.id, raiz.dados)
            self.inordem(raiz.direita)
