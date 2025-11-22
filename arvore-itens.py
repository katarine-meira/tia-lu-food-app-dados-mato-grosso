from json_funcoe import carregar_json, salvar_json

CAMINHO_JSON_ITENS = "dados_itens.json"


class NoAVL:
    def __init__(self, cod_item, valor):
        self.chave = cod_item
        self.valor = valor
        self.esquerda = None
        self.direita = None
        self.altura = 1


class ArvoreAVL:
    def __init__(self):
        self.raiz = None
        self.carregar_itens()

    def altura(self, no):
        if no is None:
            return 0
        return no.altura

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

    def inserir(self, raiz, cod_item, valor):
        if raiz is None:
            return NoAVL(cod_item, valor)

        if cod_item < raiz.chave:
            raiz.esquerda = self.inserir(raiz.esquerda, cod_item, valor)
        elif cod_item > raiz.chave:
            raiz.direita = self.inserir(raiz.direita, cod_item, valor)
        else:
            raiz.valor = valor
            return raiz

        raiz.altura = 1 + max(self.altura(raiz.esquerda), self.altura(raiz.direita))
        bal = self.balanceamento(raiz)

        if bal > 1 and cod_item < raiz.esquerda.chave:
            return self.rotacao_direita(raiz)
        if bal < -1 and cod_item > raiz.direita.chave:
            return self.rotacao_esquerda(raiz)
        if bal > 1 and cod_item > raiz.esquerda.chave:
            raiz.esquerda = self.rotacao_esquerda(raiz.esquerda)
            return self.rotacao_direita(raiz)
        if bal < -1 and cod_item < raiz.direita.chave:
            raiz.direita = self.rotacao_direita(raiz.direita)
            return self.rotacao_esquerda(raiz)

        return raiz

    def adicionar_item(self, cod_item, valor):
        self.raiz = self.inserir(self.raiz, cod_item, valor)
        self.salvar_itens()

    def buscar(self, raiz, cod_item):
        if raiz is None:
            return None
        if cod_item == raiz.chave:
            return raiz.valor
        if cod_item < raiz.chave:
            return self.buscar(raiz.esquerda, cod_item)
        return self.buscar(raiz.direita, cod_item)

    