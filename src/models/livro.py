class Livro():
    def __init__(self, nome):
        self.nome_livro = nome
        self.paginas = {}
        self.pagina_atual = 1
        self.numero_de_paginas = 0

    def adicionar_conteudo(self, lista):
        pagina = 1
        count = 0
        for conteudo in lista:
            if pagina not in self.paginas:
                self.paginas[pagina] = []
            self.paginas[pagina].append(conteudo)
            count += 1
            if count == 9:
                count = 0
                pagina += 1
        self.numero_de_paginas = len(self.paginas.keys())

    @property
    def proxima_pagina(self):
        if self.numero_de_paginas != self.pagina_atual:
            self.pagina_atual += 1

    @property
    def pagina_anterior(self):
        if self.pagina_atual != 1:
            self.pagina_atual -= 1
            
    @property
    def numero_itens(self):
        try:
            numero_de_itens = len(self.paginas[self.pagina_atual])
        except:
            numero_de_itens = 0
        return numero_de_itens

    @property
    def itens_pagina(self):
        return self.paginas[self.pagina_atual]
