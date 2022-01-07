from bs4 import BeautifulSoup
from pathlib import Path
import os
import requests


def busca_link(site_TISS):
    page = BeautifulSoup(site_TISS.content, 'html.parser')
    link_pdf = page.find('a', attrs={'data-tippreview-enabled': 'true'}).get('href')

    baixa_pdf(link_pdf)

def baixa_pdf(link_pdf):
    page = requests.get(link_pdf)
    page_pdf = BeautifulSoup(page.content, 'html.parser')

    componente_organizacional = page_pdf.find('a', attrs={'target': '_blank'}).get('href')

    pdf = requests.get(componente_organizacional)

    arquivo = Path('Comportamento_Organizacional.pdf')
    arquivo.write_bytes(pdf.content)

def verifica_status_http(site_TISS):
    print('Verificando disponibilidade do site ...')

    if site_TISS.status_code == 200:
        print('Acesso permitido\nIniciando download do pdf ...')
        return True
    else:
        print('Ocorreu um erro ao se comunicar ao site')
        return False

def verifica_arquivo_existente():
    print('Verificando se o arquivo existe em seu computador ...')

    if os.path.isfile('./Comportamento_Organizacional.pdf'):
        print('Arquivo encontrado\nPor favor verifique a pasta do programa')
        return True
    
    return False

def main():
    arquivo = verifica_arquivo_existente()

    if arquivo == True:
        print('Obrigado por me usar')
    else:
        site_TISS = requests.get('https://www.gov.br/ans/pt-br/assuntos/prestadores/padrao-para-troca-de-informacao-de-saude-suplementar-2013-tiss')

        status_code = verifica_status_http(site_TISS)

        if status_code == True: 
            busca_link(site_TISS)

if __name__ == "__main__":
    main()