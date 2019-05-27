class Licitacao:
    def __init__(self, i, mun, ed, obj, mod, org, dt, sts):
        self.id = i
        self.edital = ed
        self.municipio = mun
        self.objeto = obj
        self.modalidade = mod
        self.orgao = org
        self.data_abertura = dt
        self.status = sts

    def __str__(self):
        return '{} - {}'.format(self.edital, self.objeto)
