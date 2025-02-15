import mysql.connector
from db_config import db_config  


def startups_sem_programadores():

    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()

    # Executar uma consulta
    query = """
    SELECT 
        nome_startup 
    FROM 
        startups2va.startup 
    NATURAL LEFT JOIN 
        startups2va.programador 
    WHERE 
        id_programador IS NULL 
    ORDER BY 
        nome_startup;
"""
    cursor.execute(query)

    results = cursor.fetchall()
    # Obter os nomes das colunas
    column_names = [i[0] for i in cursor.description]

    return (results, column_names)

def consulta_colunas_tabela(tabela, colunas="*", where=None):
    
        # Conectar ao banco de dados
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

        # Montar a consulta SQL
        if isinstance(colunas, list):
            colunas_str = ", ".join(colunas)  # Converte a lista de colunas em uma string
        else:
            colunas_str = colunas  # Usa "*" ou a string fornecida diretamente

        query = f"SELECT {colunas_str} FROM {tabela}"

        # Adicionar cláusula WHERE se fornecida
        if where == 'tem 30 anos ou mais':
                query += " WHERE TIMESTAMPDIFF(YEAR, data_nascimento, CURDATE()) >= 30"
        elif where == 'tem menos de 30 anos':
                query += " WHERE TIMESTAMPDIFF(YEAR, data_nascimento, CURDATE()) < 30"
        elif where == 'Filho ou Filha de um programador/programadora':
                query += " WHERE parentesco = 'Filho' OR parentesco = 'Filha'"
        elif where == 'Esposa ou Marido de um programador/programadora':
                query += " WHERE parentesco IS NULL OR parentesco NOT IN ('Filho', 'Filha')"
        elif where == 'filho ou filha com 10 anos ou mais':
                query += " WHERE (parentesco = 'Filho' or parentesco = 'Filha') AND TIMESTAMPDIFF(YEAR, data_dependete, CURDATE()) >= 10"
        elif where == 'Somente genero masculino':
                query += " WHERE genero_programador = 'M'"
        elif where == 'Somente genero feminino':
                query += " WHERE genero_programador = 'F'"        
        else:
                query = f"SELECT {colunas_str} FROM {tabela}"

        # Executar a consulta
        cursor.execute(query)

        # Obter resultados
        results = cursor.fetchall()
        column_names = [i[0] for i in cursor.description]  # Nomes das colunas

        return (results, column_names)






    
