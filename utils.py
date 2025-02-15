import streamlit as st
import mysql.connector
from db_config import db_config

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