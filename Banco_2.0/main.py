import mysql.connector
import download_dados

def baixa_dados():
    download_dados.main()

def cria_tables(cursor):
    cont_tables = 0
    cont_name_tables = 0
    year = 2020

    while cont_tables < 8:
        if cont_name_tables == 4:
            cont_tables = 0
            year += 1

        cursor.execute(f'''
            CREATE TABLE T{cont_name_tables+1}{year}(	
                data varchar(12),
                reg_ans varchar(11),
                cod_conta varchar(11),
                descricao tinytext,
                vl_saldo varchar(30)
            ) DEFAULT CHARSET = utf8
        ''')
        cont_name_tables += 1
        cont_tables += 1
    
    cursor.execute(f'''
        CREATE TABLE referencia(
            reg_ans varchar(11),
            cnpj varchar(30),
            razao_social tinytext,
            nome_fantasia varchar(20),
            modalidade varchar(30),
            logradouro tinytext,
            numero_end varchar(20),	
            complemento varchar(40),
            bairro	tinytext,
            cidade varchar(50),
            uf varchar(4),
            cep varchar(11),
            ddd varchar(4),
            telefone varchar(20),
            fax varchar(20),
            email varchar(50),
            representante varchar(50),
            cargo_reprensentante varchar(30),
            data varchar(12)
        ) DEFAULT CHARSET = utf8
    ''')

def relaciona_tables(cursor):
    cont_tables = 0
    cont_name_tables = 0
    year = 2020

    cursor.execute('''
        ALTER TABLE referencia
        MODIFY cnpj varchar(30) PRIMARY KEY
    ''')

    while cont_tables < 8:
        if cont_tables == 4:
            cont_name_tables = 0
            year += 1
        
        cursor.execute(f'''
            ALTER TABLE T{cont_name_tables+1}{year}
            ADD FOREING KEY (reg_ans) REFERENCES referencia(cnpj)
            ADD FOREING KEY (descricao) REFERENCES referencia(cnpj)
        ''')
        
        cont_name_tables += 1
        cont_tables +=1

def coloca_dados(cursor):
    cont_tables = 0
    cont_name_tables = 0
    year = 2020

    while cont_tables < 7:
        if cont_tables == 4:
            cont_name_tables = 0
            year += 1
        
        cursor.execute(f'''
            LOAD DATA INFILE './{cont_name_tables+1}T{year}.csv' INTO TABLE T{cont_name_tables+1}{year}
            FIELDS TERMINATED BY ';'
            LINES TERMINATED BY '\n'
            IGNORE 1 ROWS
        ''')
    
    cursor.execute(f'''
        LOAD DATA INFILE './relatorio.csv' INTO TABLE referencia
        FIELDS TERMINATED BY ';'
        LINES TERMINATED BY '\n'
        IGNORE 3 ROWS
    ''')
        
def consulta_trimestre(cursor):
    cursor.execute(f'''
        SELECT reg_ans.3T2021 descricao.3T2021, cnpj.Relatorio_cadop 
        FROM 3T2021, Relatorio_cadop
        WHERE Relatorio_cadop.cnpj = 3T2021.reg_ans AND descricao IN ('"EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR"'); 
    ''')

def cosulta_ano(cursor):
    cont_tables = 0
    cont_name_tables = 0
    year = 2020

    while cont_tables < 7:
        if cont_tables == 4:
            year += 1
            cont_name_tables = 0

        cursor.execute(f'''
            SELECT reg_ans.{cont_name_tables+1}T{year}, descricao.1T2020, cnpj.Relatorio_cadop 
            FROM 1T2020, Relatorio_cadop
            WHERE Relatorio_cadop.cnpj = 1T2020.reg_ans AND descricao IN ('"EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR"')
        ''')

        cont_tables += 1
        cont_name_tables += 2

def main():
    
    #Faz a conecção com o mysql
    banco = mysql.connector.connect(
        host='localhost',
        user='root',
        password=''
    )

    #define a variavel com cmd do sql
    cursor = banco.cursor()

    #usa o comando execute para executar blocos de comandos dentro do banco
    cursor.execute('''
        CREATE DATABASE python_banco				
        DEFAULT CHARACTER SET utf8
    ''')

    cursor.execute('USE python_banco')

    cria_tables(cursor)
    relaciona_tables(cursor)
    baixa_dados()
    coloca_dados(cursor)
          
if __name__ == '__main__':
    main()