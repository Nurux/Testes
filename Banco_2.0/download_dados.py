import os
from bs4 import BeautifulSoup
from zipfile import ZipFile
import requests

def baixa_dados_lastyear(link_1):
    cont = 1
    cont2 = 3

    dados_lastyear = requests.get(link_1)

    dados_download = BeautifulSoup(dados_lastyear.content, 'html.parser')

    print('Baixando dados do ultimo ano ...')
    while cont < 4:
        lastyear_download = dados_download.find_all('a')[-cont].get('href')
        print(lastyear_download)
        
        link_download = link_1 + lastyear_download
        tables_dados = requests.get(link_download)
        
        with open (f'{cont2}T2021.zip', 'wb') as arquivo:
            arquivo.write(tables_dados.content)

        cont += 1
        cont2 -= 1

def baixa_dados_penultimateyear(link_2):
    cont = 1
    cont2 = 3

    last_year = requests.get(link_2)

    list_download = BeautifulSoup(last_year.content, 'html.parser')

    while cont < 5:
        d1 = list_download.find_all('a')[-cont].get('href')
        print(d1)
        t1 = link_2 + d1
        dl1 = requests.get(t1)
        
        with open (f'{cont2+1}T2020.zip', 'wb') as arquivo:
            arquivo.write(dl1.content)

        cont += 1
        cont2 -= 1

def baixa_relatorio():

    site = requests.get('http://www.ans.gov.br/externo/site_novo/informacoes_avaliacoes_oper/lista_cadop.asp')
    
    with open('relatorio.csv', 'wb') as arquivo:
        arquivo.write(site.content)

def descompacta_dados():
    cont = 0
    cont2 = 0
    years = 2020

    while cont < 7:
        if cont == 4:
            cont2 = 0
            years += 1

        
        with ZipFile(f'{cont2+1}T{years}.zip', 'r') as myzip:
            myzip.extractall() 
            
        os.remove(f'{cont2+1}T{years}.zip')
        cont +=1
        cont2 += 1            

def main():
    site = requests.get('http://ftp.dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/')

    obj_site = BeautifulSoup(site.content, 'html.parser')

    link_1 = obj_site.find_all('a')[-2].get('href')
    link_2 = obj_site.find_all('a')[-3].get('href')

    url = 'http://ftp.dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/'

    link_1 = url + link_1
    link_2 = url + link_2

    baixa_dados_lastyear(link_1)
    baixa_dados_penultimateyear(link_2)
    descompacta_dados()
    baixa_relatorio()
    
if __name__ == '__main__':
    main()