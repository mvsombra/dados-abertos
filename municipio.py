from unicodedata import normalize as normal


class Municipio:
    def __init__(self, i, nome, meso, micro):
        self.id = i
        self.nome = nome
        self.mesorregiao = meso
        self.microrregiao = micro

    def __str__(self):
        return self.nome

    @property
    def nome_tratado(self):
        nome = self.nome.lower().replace(' ', '-')
        return normal('NFKD', nome).encode('ASCII', 'ignore').decode('ASCII')
