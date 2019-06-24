import requests
from bs4 import BeautifulSoup as bs

municipios = ['eusebio', 'maranguape', 'novaolinda', 'parambu', 'pedrabranca',
              'salitre']
base_url = "https://{}.tudotransparente.com.br/api/licitacoes/xml/{}"
for m in municipios:
    for ano in ['2019', '2018', '2017']:
        temp_url = base_url.format(m, ano)
        page = requests.get(temp_url)
        soup = bs(page.content, 'lxml')
        lics = soup.findAll('licitacoes')
        for lic in lics:
            print('Número: {}'.format(lic.numero.text))
            print('Data: {}'.format(lic.data.text))
            print('Objeto: {}'.format(lic.objeto.text))
            print('Modalidade: {}'.format(lic.modalidade.text))
            print('Tipo: {}'.format(lic.tipo.text))
            print('------------')
