'''
Obs: Há um jeito bem mais facil de fazer esse mesmo projeto usando a lib Camelot, porém achei meio inviavel já
que para utiliza-la o usuario deve baixar duas dependencias a parte e ainda importar a lib aqui no terminal.

Projeto feito com as libs Tabula, Pandas, Numpy, Zipfile e Os

Obs2: se quiser as três tabelas em unico csv, então só sera necessário importar a lib tabula

Ex só com tabula: 
    import tabula

    URL_PDF = 'https://www.gov.br/ans/pt-br/arquivos/assuntos/prestadores/padrao-para-troca-de-informacao-de-saude-suplementar-tiss/padrao-tiss/padrao-tiss_componente-organizacional_202111.pdf'
    tabula.convert_into(URL_PDF, 'Quadros.csv', 'csv', pages='114-120')

Como não queria as 3 tabelas juntas optei por adicionar outras libs.

Abra o terminal e digite:
    pip install tabula
    pip install pandas
    pip install numpy
    pip install zipfile
    pip install os

Se estiver em ambiente Linux:
    pip3 install tabula  
    pip3 install pandas
    pip3 install numpy
    pip3 install zipfile
    pip3 install os  
'''

from zipfile import ZipFile
import numpy as np
import pandas as pd
import tabula
import os

#Verifica se o arquivo já existe na pasta 
def verifica_arquivo_existente():
    print('Verificando se arquivo já existe ...')

    if os.path.isfile('./Teste_{John_Santos_Felix_de_Santana}.zip'):
        print('Arquivo encontrado\nVerifique a pasta raiz do projeto')
        return True
    else:
        print('Arquivo não encontrado\n\nIniciando a extração\n')
        print('Isso pode levar alguns segundos ...')
        return False    

#Extrai os quadros do pdf e transforma eles em .csv
def extrai_quadros():
    URL_PDF = 'https://www.gov.br/ans/pt-br/arquivos/assuntos/prestadores/padrao-para-troca-de-informacao-de-saude-suplementar-tiss/padrao-tiss/padrao-tiss_componente-organizacional_202111.pdf'
    lista_quadros = tabula.read_pdf(URL_PDF, pages='114-120')

    #Define opção maxima de display como nula, para evitar truncamento de dados 
    pd.set_option('display.max_colwidth', None)

    df_quadro30 = pd.DataFrame(lista_quadros[0])
    df_quadro30.to_csv('Quadro_30.csv', index=False)

    array_quadro31 = np.array(dtype=list, object=[lista_quadros[1:7]])
    df_quadro31 = pd.DataFrame(array_quadro31)
    df_quadro31.to_csv('Quadro_31.csv', index=False)

    df_quadro32 = pd.DataFrame(lista_quadros[7])
    df_quadro32.to_csv('Quadro_32.csv', index=False)

    cria_zip()

#Pega os .csv extraidos e compacta todos em um arquivo .zip
def cria_zip():
    with ZipFile('./Teste_{John_Santos_Felix_de_Santana}.zip', 'w') as myzip:
        myzip.write('Quadro_30.csv')
        myzip.write('Quadro_31.csv')
        myzip.write('Quadro_32.csv')
    
    os.remove('Quadro_30.csv')
    os.remove('Quadro_31.csv')
    os.remove('Quadro_32.csv')

    print('Arquivo criado com sucesso')

#Inicio do Programa
def main():
    if verifica_arquivo_existente() == True:
        print('Obrigado por usar o programa')
    else:
        extrai_quadros()

#Define começo do programa 
if __name__ == '__main__':
    main()