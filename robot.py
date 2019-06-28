from crawler import Lics_Tudo_Transparente as ltt
from control_functions import Controler


def main():
    control = Controler()
    dba = control.create_dba()
    dba.delete_licitacoes()
    crawler = ltt()
    crawler.crawl()
    dba.delete_licitacoes(invalidas=True)


if(__name__ == '__main__'):
    main()
