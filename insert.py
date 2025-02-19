import mysql.connector
import streamlit as st
from consultas import *
from utils import *

def validar_tipo_dado(valor, tipo_coluna):
    """
    Verifica se o valor é compatível com o tipo de dados da coluna.
    :param valor: Valor a ser validado.
    :param tipo_coluna: Tipo de dados da coluna (ex: 'INT', 'VARCHAR(255)', 'DATE').
    :return: True se o valor for compatível, False caso contrário.
    """
    tipo_coluna = tipo_coluna.upper()

    if valor is None:
        return True  # Permitir valores None (NULL no banco)

    try:
        if "INT" in tipo_coluna:
            int(valor)
        elif "VARCHAR" in tipo_coluna or "TEXT" in tipo_coluna:
            str(valor)
        elif "DATE" in tipo_coluna or "DATETIME" in tipo_coluna:
            # Aqui você pode validar com regex ou parsing de data
            from datetime import datetime
            datetime.strptime(valor, "%Y-%m-%d")  # Assume formato 'YYYY-MM-DD'
        elif "FLOAT" in tipo_coluna or "DOUBLE" in tipo_coluna:
            float(valor)
        elif "BOOLEAN" in tipo_coluna:
            if not isinstance(valor, (bool, int)):  # Aceita 0/1 como booleano
                return False
        else:
            return False
    except (ValueError, TypeError):
        return False

    return True

def inserir_registro(tabela, colunas, valores):
    """
    Insere um novo registro em uma tabela, verificando os tipos de dados.
    Retorna a tabela atualizada após a inserção.
    :param tabela: Nome da tabela.
    :param colunas: Lista de nomes das colunas.
    :param valores: Lista de valores correspondentes às colunas.
    :return: Lista de dicionários representando a tabela atualizada ou mensagem de erro.
    """
    try:
        with mysql.connector.connect(**db_config) as cnx:
            with cnx.cursor(dictionary=True) as cursor:
                # Buscar os tipos das colunas da tabela
                cursor.execute(f"SHOW COLUMNS FROM {tabela}")
                tipos_colunas = {coluna["Field"]: coluna["Type"] for coluna in cursor.fetchall()}

                # Validar tipos de dados antes da inserção
                for coluna, valor in zip(colunas, valores):
                    if coluna in tipos_colunas and not validar_tipo_dado(valor, tipos_colunas[coluna]):
                        return {"erro": f"Valor '{valor}' incompatível com '{tipos_colunas[coluna]}' da coluna '{coluna}'."}

                # Montar e executar a query de inserção
                colunas_str = ", ".join(colunas)
                placeholders = ", ".join(["%s"] * len(valores))
                query = f"INSERT INTO {tabela} ({colunas_str}) VALUES ({placeholders})"
                cursor.execute(query, valores)
                cnx.commit()

                if cursor.rowcount > 0:
                    st.success(f"Registro inserido com sucesso: {cursor.rowcount} linha(s) afetada(s).")
                else:
                    return {"aviso": "Nenhum registro foi inserido. Verifique os dados fornecidos."}

                # Consultar a tabela atualizada
                cursor.execute(f"SELECT * FROM {tabela}")
                return cursor.fetchall()

    except mysql.connector.IntegrityError as err:
        return {"erro": f"Erro de integridade: {err}"}
    except mysql.connector.ProgrammingError as err:
        return {"erro": f"Erro de sintaxe ou estrutura: {err}"}
    except mysql.connector.InterfaceError as err:
        return {"erro": f"Erro de conexão com o banco: {err}"}
    except mysql.connector.Error as err:
        return {"erro": f"Erro geral do MySQL: {err}"}
