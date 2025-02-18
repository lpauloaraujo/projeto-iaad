import streamlit as st
import mysql.connector
from db_config import db_config
from collections import defaultdict

def obter_chaves_primarias(tabelas_existentes):
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()
    placeholders = ', '.join(['%s'] * len(tabelas_existentes))
    query = f"""
    SELECT TABLE_NAME, COLUMN_NAME
    FROM information_schema.KEY_COLUMN_USAGE
    WHERE TABLE_SCHEMA = %s
    AND TABLE_NAME IN ({placeholders})
    AND CONSTRAINT_NAME = 'PRIMARY';
    """
    cursor.execute(query, ('startups2va', *tabelas_existentes))
    primary_keys = cursor.fetchall()
    primary_keys_dict = defaultdict(list)
    for table, column in primary_keys:
        primary_keys_dict[table].append(column)
    return primary_keys_dict

def exibir_tabela(tupla):
    results, column_names = tupla
    st.write("Resultados da consulta:")
    # Criar o cabeçalho da tabela com os nomes das colunas em vermelho
    header = "<tr>" + "".join([f'<th style="color: red;">{col}</th>' for col in column_names]) + "</tr>"
    
    # Criar as linhas da tabela com os dados
    rows = ""
    for row in results:
        rows += "<tr>" + "".join([f"<td>{cell}</td>" for cell in row]) + "</tr>"
    
    # Montar a tabela completa em HTML
    table_html = f"""
    <table>
        {header}
        {rows}
    </table>
    """
    
    # Exibir a tabela usando st.markdown com HTML
    st.markdown(table_html, unsafe_allow_html=True)

def obter_colunas_tabela(tabela):
    
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()

    # Consulta para obter as colunas da tabela
    cursor.execute(f"SHOW COLUMNS FROM {tabela};")
    colunas = [row[0] for row in cursor.fetchall()]

    return colunas


def listar_registros(tabela):
    """
    Lista todos os registros de uma tabela.
    """
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {tabela}")
        registros = cursor.fetchall()
        return registros
    except mysql.connector.Error as err:
        st.error(f"Erro ao listar registros: {err}")
        return []
    finally:
        if cnx.is_connected():
            cursor.close()
            cnx.close()




#Funções do CREATE
def criar_tabela(nome_tabela, colunas):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        cols = adaptar_dic_colunas(colunas)
        cursor.execute(f"CREATE TABLE {nome_tabela} {cols}")
        st.success(f'Tabela "{nome_tabela}" criada com sucesso.')
    except mysql.connector.Error as err:
        st.error(f"Erro ao criar tabela: {err}")
    finally:
        if cnx.is_connected():
            cursor.close()
            cnx.close()

def adaptar_dic_colunas(dic_colunas):
    colunas = '('
    for key, value in dic_colunas.items():
        if key == 'keys':
            if len(dic_colunas['keys']) == 0:
                colunas = colunas[:len(colunas) - 2]
                colunas += ');'
                return colunas
            else:
                for i, ref in enumerate(dic_colunas['keys']):
                    if i == len(dic_colunas['keys']) - 1:
                        colunas += f"{ref});"
                        return colunas
                    colunas += f"{ref}, "
        colunas += f"{key} {value}, "
    return colunas

def adicionar_coluna(tabela, nome, configs):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        cursor.execute(f"ALTER TABLE {tabela} ADD COLUMN {nome} {configs};")
        st.success(f'Coluna "{nome}" adicionada a tabela "{tabela}" com sucesso.')
    except mysql.connector.Error as err:
        st.error(f"Erro ao adicionar coluna: {err}")
    finally:
        if cnx.is_connected():
            cursor.close()
            cnx.close()

import mysql.connector

def get_table_names():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        cursor.close()
        conn.close()
        return tables
    except mysql.connector.Error as err:
        print(f"Erro: {err}")
        return []




