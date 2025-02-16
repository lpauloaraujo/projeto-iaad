import streamlit as st
from consultas import *
from atualizar import *
from utils import *



def CRUD():
    tabelas_disponiveis = [
        "dependentes",
        "linguagem",
        "programador",
        "programador_linguagem",
        "startup"
    ]

    # Filtros disponíveis para cada tabela
    filtros_por_tabela = {
        "dependentes": [
            ' ',
            'Filho ou Filha de um programador/programadora',
            'Esposa ou Marido de um programador/programadora',
            'filho ou filha com 10 anos ou mais'
        ],
        "programador": [
            ' ',
            'tem 30 anos ou mais',
            'tem menos de 30 anos',
            'Somente genero masculino',
            'Somente genero feminino'
        ],
        "linguagem": [
            ' '
        ],
        "programador_linguagem": [
            ' '
        ],
        "startup": [
            ' '
        ]
    }

    # Título da aplicação
    st.title("Consulta e Atualização de Tabela")

    # Selecionar tabela
    tabela_selecionada = st.selectbox(
        "Escolha uma tabela para consultar ou atualizar:",
        tabelas_disponiveis
    )

    #Seção de Criação de Tabelas - CREATE

    tipos_atributos = [
        "VARCHAR",
        "CHAR",
        "TEXT",
        "INT",
        "BIGINT",
        "DECIMAL",
        "NUMERIC",
        "FLOAT",
        "DOUBLE",
        "DATE",
        "DATETIME",
        "BOOLEAN"
    ]

    st.header("Criação de Tabelas")
    col_ntabela, col_qtd_cols = st.columns([2, 0.5])  

    with col_ntabela:
        nome_tabela = st.text_input("Nome da tabela")
    with col_qtd_cols:
        qtd_colunas = st.number_input("Quantidade de colunas", min_value=1, step=1, format="%d")

    dic_cols = {}
    for col in range(qtd_colunas):
        nome = st.text_input(key=f"nome_{col}", label=f"Nome da {col + 1}° coluna")
        tipo = st.selectbox(key=f"tipo_{col}", label=f"Tipo da {col + 1}° coluna", options=tipos_atributos)
        config = st.text_input(key=f"config_{col}", label=f"Configuração da {col + 1}° coluna (exp: NOT NULL, PRIMARY KEY, etc...)")
        dic_cols[nome] = [tipo, config]
    
    comando_colunas = adaptar_dic_colunas(dic_cols)

    print(nome_tabela, comando_colunas)

    # Seção de Atualização de Registro - UPDATE
    st.header("Atualizar Registro")
    registros = listar_registros(tabela_selecionada)

    if registros:
        # Exibir os registros em um selectbox para o usuário escolher
        opcoes_registros = [str(registro) for registro in registros]
        registro_selecionado_pra_atualizar = st.selectbox("Escolha o registro para alterar:", opcoes_registros)

        # Obter o índice do registro selecionado
        indice_registro = opcoes_registros.index(registro_selecionado_pra_atualizar)
        registro = registros[indice_registro]

        # Exibir as colunas da tabela para o usuário escolher qual alterar
        colunas = list(registro.keys())
        coluna_selecionada = st.selectbox("Escolha a coluna para alterar:", colunas)

        # Coletar o novo valor
        novo_valor = st.text_input(f"Novo valor para '{coluna_selecionada}':")

        # Botão para confirmar a alteração
        if st.button("Alterar Registro"):
            if novo_valor:
                # Construir a condição WHERE (usando a chave primária ou todos os campos para garantir unicidade)
                where_condicao = " AND ".join([f"{k} = %s" for k in registro.keys()])
                valores_where = tuple(registro.values())

                # Executar a alteração
                tabela_atualizada = alterar_registro(
                    tabela=tabela_selecionada,
                    coluna=coluna_selecionada,
                    novo_valor=novo_valor,
                    where_condicao=where_condicao,
                    valores_where =valores_where  
                )

                # Exibir a tabela atualizada
                if tabela_atualizada:
                    st.success("Registro alterado com sucesso!")
                    st.write("Tabela atualizada:")
                    st.table(tabela_atualizada)
            else:
                st.warning("Por favor, insira um novo valor.")
    else:
        st.warning(f"Nenhum registro encontrado na tabela '{tabela_selecionada}'.")

    # Seção de Consulta de Registros -- READ
    st.header("Consultar Registros")
    where_disponiveis = filtros_por_tabela.get(tabela_selecionada, [' '])
    where_selecionado = st.selectbox(
        "Escolha um filtro para a consulta:",
        where_disponiveis
    )

    colunas_tabela = obter_colunas_tabela(tabela_selecionada)

    if colunas_tabela:
        st.write("Selecione as colunas:")
        colunas_selecionadas = []
        for coluna in colunas_tabela:
            if st.checkbox(coluna, key=coluna):
                colunas_selecionadas.append(coluna)

        # Se nenhuma coluna for selecionada, seleciona todas por padrão
        if not colunas_selecionadas:
            colunas_selecionadas = "*"

    # Botão para consultar
    if st.button("Consultar"):
        if tabela_selecionada and colunas_tabela:
            # Executar a consulta
            resultados, colunas = consulta_colunas_tabela(
                tabela=tabela_selecionada,
                colunas=colunas_selecionadas,
                where=where_selecionado
            )

            # Exibir resultados
            if resultados:
                st.write("Resultados da consulta:")
                exibir_tabela((resultados, colunas))
            else:
                st.write("Nenhum resultado encontrado.")
        else:
            st.error("Selecione uma tabela e pelo menos uma coluna.")

# Executar a aplicação
CRUD()