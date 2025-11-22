class NoAVL:
    def __init__(self, cod_item, valor):
        self.chave = cod_item
        self.valor = valor
        self.esquerda = None
        self.direita = None
        self.altura = 1

class ArvoreAVL:
    def altura(self, no):
        if no is None:
            return 0
        else:
            return no.height
    
    def balanceamento(self, no):
        if no is None:
            return 0 
        else:
            return self.altura(no.esquerda) - self.altura(no.direita)
        
    def rotacao_direita(self, Y):
        X = Y.esquerda
        T2 = X.direita

        X.direita = Y
        Y.esquerda = T2

        Y.altura = 1 + max(self.altura(Y.esquerda), self.altura(Y.direita)) #o max é pra pegar o maior desses dois
        X.altura = 1 + max(self.altura(X.esquerda), self.altura(X.direita))

        return X

    def rotacao_esquerda(self, X):
        Y = X.direita
        T2 = X.esquerda

        Y.esquerda = X
        X.direita = T2

        X.altura = 1 + max(self.altura(X.esquerda), self.altura(X.direita))
        Y.altura = 1 + max(self.altura(Y.esquerda), self.altura(Y.direita))

        return Y
    def inserir(self, raiz, cod_item, valor):
        if raiz is None:
            return NoAVL(cod_item, valor)
        
        if cod_item < raiz.cod:
            raiz.esquerda = self.inserir(raiz.esquerda, cod_item, valor)
        
        elif cod_item > raiz.cod:
            raiz.direita = self.inserir(raiz.direita, cod_item, valor)
        
        else:
            return raiz
        
    #pra atualizar altura e o balaceamento

        raiz.altura = 1 + max(self.altura(raiz.esquerda), self.altura(raiz.direita))

        balanceamento = self.balanceamento(raiz)

        #casos pra desbalancear se pesar em algum lado 
        if balanceamento > 1 and cod_item < raiz.esquerda.id:
            return self.rotacao_direita(raiz)

        if balanceamento < -1 and cod_item > raiz.direita.id:
            return self.rotacao_esquerda(raiz)

        if balanceamento > 1 and cod_item > raiz.esquerda.id:
            raiz.esquerda = self.rotacao_esquerda(raiz.esquerda)
            return self.rotacao_direita(raiz)

        if balanceamento < -1 and cod_item < raiz.direita.id:
            raiz.direita = self.rotacao_direita(raiz.direita)
            return self.rotacao_esquerda(raiz)
        
        return raiz
    
    