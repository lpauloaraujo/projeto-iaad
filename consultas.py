import mysql.connector
from db_config import db_config  


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
        elif where == 'Startups sem programadores (LEFT JOIN EXCLUSIVO)':
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
        elif where == 'Programadores sem startups (LEFT JOIN EXCLUSIVO)':
                query = """
                SELECT 
                    nome_programador 
                FROM 
                    startups2va.programador 
                NATURAL LEFT JOIN 
                    startups2va.startup 
                WHERE 
                    id_startup IS NULL 
                ORDER BY 
                    nome_programador;
                """
        
        elif where == 'programadores e suas linguagens (NATURAL JOIN)':
               query = """
               SELECT 
                    p.nome_programador, 
                    l.nome_linguagem 
                FROM 
                    startups2va.programador p 
                NATURAL JOIN 
                    startups2va.programador_linguagem pl 
                NATURAL JOIN 
                    startups2va.linguagem l 
                ORDER BY 
                    p.nome_programador;
                """
        
        elif where == 'linguagens que não estão associadas a nenhum programador (LEFT JOIN EXCLUSIVO)':
               query = """
                SELECT 
                    l.nome_linguagem 
                FROM 
                    startups2va.linguagem l 
                NATURAL LEFT JOIN 
                    startups2va.programador_linguagem pl 
                WHERE 
                    pl.id_programador IS NULL 
                ORDER BY 
                    l.nome_linguagem;
                """
        elif where == 'Listar programadores, suas startups e as linguagens que conhecem (NATURAL JOIN)':
               query = """
               SELECT 
                    p.nome_programador, 
                    s.nome_startup, 
                    l.nome_linguagem 
                FROM 
                    startups2va.programador p 
                NATURAL JOIN 
                    startups2va.startup s 
                NATURAL JOIN 
                    startups2va.programador_linguagem pl 
                NATURAL JOIN 
                    startups2va.linguagem l 
                ORDER BY 
                    p.nome_programador;
                """
        elif where == 'Listar todos os nomes de programadores e dependentes (UNION)':
               query = """
               SELECT 
                    nome_programador AS nome 
                FROM 
                    startups2va.programador
                UNION
                SELECT 
                    nome_dependente AS nome 
                FROM 
                    startups2va.dependentes;
                """
        elif where == 'Listar todos os programadores e seus respectivos dependentes (LEFT JOIN)':
               query = """
               SELECT 
                    p.nome_programador, 
                    d.nome_dependente,
                    d.parentesco
                FROM 
                    startups2va.dependentes d 
                NATURAL LEFT JOIN 
                    startups2va.programador p 
                ORDER BY 
                    d.nome_dependente;
                """
        else:
                query = f"SELECT {colunas_str} FROM {tabela}"

        # Executar a consulta
        cursor.execute(query)

        # Obter resultados
        results = cursor.fetchall()
        column_names = [i[0] for i in cursor.description]  # Nomes das colunas

        return (results, column_names)


