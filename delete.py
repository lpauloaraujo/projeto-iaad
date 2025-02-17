from consultas import *
from utils import *
import mysql.connector

def deletar_registro(tabela, atributo=None, valor=None, where_condicao=None, valores_where=None):
    """
    Deleta um ou mais registros de uma tabela com base em uma condição WHERE ou em um atributo específico.
    Retorna a tabela atualizada após a exclusão.

    :param tabela: Nome da tabela (string segura).
    :param atributo: Nome da coluna onde será feita a comparação (opcional).
    :param valor: Valor que será comparado na coluna do atributo (opcional).
    :param where_condicao: Condição WHERE com placeholders (%s), se necessário.
    :param valores_where: Tupla com valores correspondentes aos placeholders na condição WHERE.
    :return: Dicionário com status e lista de registros atualizados.
    """
    
    try:
        with mysql.connector.connect(**db_config) as cnx:
            with cnx.cursor(dictionary=True) as cursor:
                
                # Buscar os atributos (colunas) da tabela dinamicamente
                cursor.execute(f"SHOW COLUMNS FROM {tabela}")
                colunas_disponiveis = {coluna["Field"] for coluna in cursor.fetchall()}

                # Caso o usuário passe um atributo para deletar registros com um valor específico
                if atributo and valor is not None:
                    if atributo not in colunas_disponiveis:
                        return {"status": "erro", "mensagem": f"Atributo '{atributo}' não existe na tabela '{tabela}'."}
                    
                    query = f"DELETE FROM {tabela} WHERE {atributo} = %s"
                    valores_where = (valor,)
                
                # Caso o usuário passe uma condição WHERE personalizada
                elif where_condicao and valores_where:
                    query = f"DELETE FROM {tabela} WHERE {where_condicao}"
                
                else:
                    return {"status": "erro", "mensagem": "É necessário fornecer um atributo/valor ou uma condição WHERE válida."}

                # Executar a query de exclusão
                cursor.execute(query, valores_where)
                cnx.commit()

                linhas_afetadas = cursor.rowcount
                if linhas_afetadas > 0:
                    mensagem = f"{linhas_afetadas} registro(s) deletado(s) com sucesso."
                else:
                    mensagem = "Nenhum registro deletado. Verifique a condição WHERE."

                # Buscar a tabela atualizada
                cursor.execute(f"SELECT * FROM {tabela}")
                tabela_atualizada = cursor.fetchall()
                
                return {
                    "status": "sucesso",
                    "mensagem": mensagem,
                    "tabela_atualizada": tabela_atualizada
                }

    except mysql.connector.Error as err:
        return {"status": "erro", "mensagem": f"Erro no banco de dados: {err}"}
    except Exception as e:
        return {"status": "erro", "mensagem": f"Erro inesperado: {e}"}
