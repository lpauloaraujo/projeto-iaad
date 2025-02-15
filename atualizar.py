from consultas import *
from utils import *
import mysql.connector


def alterar_registro(tabela, coluna, novo_valor, where_condicao, valores_where):
    """
    Altera um registro em uma coluna de uma tabela, verificando se o novo valor é do mesmo domínio (tipo de dados).
    Retorna a tabela atualizada após a alteração.

    :param tabela: Nome da tabela.
    :param coluna: Nome da coluna a ser atualizada.
    :param novo_valor: Novo valor para a coluna.
    :param where_condicao: Condição WHERE para identificar o registro.
    :param valores_where: Valores correspondentes aos placeholders na condição WHERE.
    :return: Lista de dicionários representando a tabela atualizada.
    """
    try:
        # Conectar ao banco de dados
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor(dictionary=True)

        # Montar a query de atualização
        query = f"UPDATE {tabela} SET {coluna} = %s WHERE {where_condicao}"
        
        # Executar a query de atualização
        # Passar o novo valor e os valores da cláusula WHERE como parâmetros
        cursor.execute(query, (novo_valor, *valores_where))

        # Confirmar a transação
        cnx.commit()

        # Verificar se alguma linha foi afetada
        if cursor.rowcount > 0:
            st.success(f"Registro(s) alterado(s) com sucesso: {cursor.rowcount} linha(s) afetada(s).")
        else:
            st.warning("Nenhum registro foi alterado. Verifique a condição WHERE.")

        # Consultar a tabela atualizada
        cursor.execute(f"SELECT * FROM {tabela}")
        tabela_atualizada = cursor.fetchall()

        return tabela_atualizada

    except mysql.connector.Error as err:
        st.error(f"Erro ao alterar registro: {err}")
        return []
    finally:
        # Fechar a conexão
        if cnx.is_connected():
            cursor.close()
            cnx.close()

def validar_tipo_dado(valor, tipo_coluna):
    """
    Verifica se o valor é compatível com o tipo de dados da coluna.

    :param valor: Valor a ser validado.
    :param tipo_coluna: Tipo de dados da coluna (ex: 'INT', 'VARCHAR(255)', 'DATE').
    :return: True se o valor for compatível, False caso contrário.
    """
    tipo_coluna = tipo_coluna.upper()

    if "INT" in tipo_coluna:
        return isinstance(valor, int)
    elif "VARCHAR" in tipo_coluna or "TEXT" in tipo_coluna:
        return isinstance(valor, str)
    elif "DATE" in tipo_coluna or "DATETIME" in tipo_coluna:
        return isinstance(valor, str)  # Assume que datas são passadas como strings no formato correto
    elif "FLOAT" in tipo_coluna or "DOUBLE" in tipo_coluna:
        return isinstance(valor, float)
    elif "BOOLEAN" in tipo_coluna:
        return isinstance(valor, bool)
    else:
        print(f"Tipo de coluna '{tipo_coluna}' não suportado para validação.")
        return False