import streamlit as st
from consultas import *
from atualizar import *
from utils import *
from delete import *



def CRUD():
    tabelas_disponiveis = [
        "dependentes",
        "linguagem",
        "programador",
        "programador_linguagem",
        "startup"
    ]

    chaves_primarias = obter_chaves_primarias(tabelas_disponiveis)

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

    configuracoes = [
        "NOT NULL",
        "AUTO_INCREMENT"
    ]

    # Seção de criação de tabelas - CREATE
    st.header("Criação de Tabelas")
    col_ntabela, col_qtd_cols = st.columns([2, 0.5])  

    with col_ntabela:
        nome_da_tabela = st.text_input("Nome da tabela")
    with col_qtd_cols:
        qtd_colunas = st.number_input("Quantidade de colunas", min_value=1, step=1, format="%d")

    dic_cols = {}
    lista_colunas = [None] * qtd_colunas

    for col in range(qtd_colunas):
        nome = st.text_input(key=f"nome_{col}", label=f"Nome da {col + 1}° coluna")
        lista_colunas[col] = nome
        col_tipo, col_config_tipo = st.columns([1, 1])
        with col_tipo:
            tipo = st.selectbox(key=f"tipo_{col}", label=f"Tipo da {col + 1}° coluna", options=tipos_atributos)
        with col_config_tipo:
            if tipo in ['CHAR', 'VARCHAR']:
                qtd_char = st.number_input(key=f"qtd_vc_{col}", label=f"Quantidade de caracteres {tipo}", min_value=1, step=1)
                tipo += f"({qtd_char})"
            elif tipo in ['DECIMAL', 'FLOAT']:
                digitos, digitos_dps = st.columns([1, 1])
                with digitos:
                    total_digitos = st.number_input(key= f"total_digitos_{col}", label="Total de dígitos", min_value=1, step=1, format="%d")
                with digitos_dps:
                    digitos_posv = st.number_input(key= f"digitos_pos_virgula_{col}", label="Dígitos após a vírgula", min_value=1, step=1, format="%d")
                tipo += f"({total_digitos},{digitos_posv})"
            elif tipo == 'BIGINT':
                bigint_espec = st.selectbox(key=f"big_{col}", label="Tipo de BIGINT", options=["SIGNED", "UNSIGNED"])
                tipo += f" {bigint_espec}"
        config = st.multiselect(key=f"config_{col}", label=f"Configurações da {col + 1}° coluna", options=configuracoes)

        if len(config) > 0:
            if len(config) > 1:
                configs = " ".join(config)
                dic_cols[nome] = tipo + " " + configs
            else:
                dic_cols[nome] = tipo + " " + config[0]
        else:
            dic_cols[nome] = tipo

    dic_cols['keys'] = []

    st.header("Defina a chave primária")

    pk_composta = st.selectbox("A nova tabela possui chave primária composta?", ["Não", "Sim"])
    if pk_composta == 'Não':
        chave_primaria = st.selectbox("Selecione a chave primária", lista_colunas)
        dic_cols['keys'].append(f"PRIMARY KEY ({chave_primaria})")
    else:
        chave_primaria = st.multiselect("Selecione as colunas que devem compor a chave primária composta", lista_colunas)
        dic_cols['keys'].append(f"PRIMARY KEY ({', '.join(chave_primaria)})")

    st.header("Defina a chave estrangeira")

    fk_exists = st.selectbox("A nova tabela possui chave estrangeira?", ["Não", "Sim"])
    if fk_exists == "Sim":
        fk_composta = st.selectbox("A chave estrangeira deve ser composta?", ["Não", "Sim"])
        if fk_composta == 'Não':
            chave_estrangeira = st.selectbox("Selecione a coluna que deve ser chave estrangeira", lista_colunas)
            referencia_estrangeira = st.selectbox("Selecione sua referência", [f"FOREIGN KEY ({chave_estrangeira}) REFERENCES {tabela}({', '.join(pk)})" for tabela, pk in chaves_primarias.items()])
            on_delete = st.selectbox("Selecione o tipo de ON DELETE", ["Nenhum", "ON DELETE CASCADE", "ON DELETE RESTRICT"])
            if on_delete != "Nenhum":
                referencia_estrangeira += f" {on_delete}"
            dic_cols['keys'].append(referencia_estrangeira)
        else:
            chave_estrangeira = st.multiselect("Selecione as colunas que devem compor a chave estrangeira", lista_colunas)
            referencia_estrangeira = st.selectbox("Selecione sua referência", [f"FOREIGN KEY ({', '.join(chave_estrangeira)}) REFERENCES {tabela}({', '.join(pk)})" for tabela, pk in chaves_primarias.items()])
            on_delete = st.selectbox("Selecione o tipo de ON DELETE", ["Nenhum", "ON DELETE CASCADE", "ON DELETE RESTRICT"])
            if on_delete != "Nenhum":
                referencia_estrangeira += f" {on_delete}"
            dic_cols['keys'].append(referencia_estrangeira)

    if st.button("Criar tabela"):
        criar_tabela(nome_da_tabela, dic_cols)
        tabelas_disponiveis.append(nome_da_tabela)

    #Seção de adição de coluna - CREATE
    st.header("Adicionar Nova Coluna")
    configuracoes_uni = ['PRIMARY KEY', 'FOREIGN KEY', 'NOT NULL', 'AUTO_INCREMENT']
    tabela_uni = st.selectbox("Selecione a tebela a receber a nova coluna", tabelas_disponiveis)
    nome_uni = st.text_input("Nome da nova coluna")
    col_tipo_uni, col_config_tipo_uni = st.columns([1, 1])
    with col_tipo_uni:
        tipo_uni = st.selectbox("Tipo da coluna", tipos_atributos)
    with col_config_tipo_uni:
        if tipo_uni in ['CHAR', 'VARCHAR']:
            qtd_char_uni = st.number_input(label=f"Quantidade de caracteres {tipo_uni}", min_value=1, step=1)
            tipo_uni += f"({qtd_char_uni})"
        elif tipo_uni in ['DECIMAL', 'FLOAT']:
            digitos_uni, digitos_dps_uni = st.columns([1, 1])
            with digitos_uni:
                total_digitos_uni = st.number_input(label="Total de dígitos", min_value=1, step=1, format="%d")
            with digitos_dps_uni:
                digitos_posv_uni = st.number_input(label="Dígitos após a vírgula", min_value=1, step=1, format="%d")
            tipo_uni += f"({total_digitos_uni},{digitos_posv_uni})"
        elif tipo_uni == 'BIGINT':
            bigint_espec_uni = st.selectbox(label="Tipo de BIGINT", options=["SIGNED", "UNSIGNED"])
            tipo_uni += f" {bigint_espec_uni}"
    config_uni = st.multiselect(label=f"Configurações da nova coluna", options=configuracoes_uni)
    if 'FOREIGN KEY' in config_uni:
        refe_uni, ondelete_uni = st.columns([1, 1])
        with refe_uni:
            referencia_uni = st.selectbox(label=f"Referência da chave estrangeria {nome_uni}", 
                                    options=[f"FOREIGN KEY ({nome_uni}) REFERENCES {tabela}({', '.join(pk)})" for tabela, pk in chaves_primarias.items()])
        with ondelete_uni:
            on_delete_uni = st.selectbox(label=f"Tipo de ON DELETE", 
                                    options=["Nenhum", "ON DELETE CASCADE", "ON DELETE RESTRICT"])
            if on_delete_uni != 'Nenhum':
                referencia_uni += f" {on_delete_uni}"

        for indice_uni, con_uni in enumerate(config_uni):
            if con_uni == "FOREIGN KEY":
                config_uni.pop(indice_uni)
                config_uni.append(f"ADD {referencia_uni}")

    if st.button("Adicionar coluna"):
        if len(config) > 0:
            adicionar_coluna(tabela_uni, nome_uni, f"{tipo_uni} {config_uni[0]}")
        else:
            adicionar_coluna(tabela_uni, nome_uni, f"{tipo_uni}")
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

    # Seção de Exclusão de Registro - DELETE
    st.header("Excluir Registro")
    registros_para_excluir = listar_registros(tabela_selecionada)

    if registros_para_excluir:
        # Exibir os registros em um selectbox para o usuário escolher
        opcoes_registros_excluir = [str(registro) for registro in registros_para_excluir]
        registro_selecionado_para_excluir = st.selectbox("Escolha o registro para excluir:", opcoes_registros_excluir)

        # Obter o índice do registro selecionado
        indice_registro_excluir = opcoes_registros_excluir.index(registro_selecionado_para_excluir)
        registro_excluir = registros_para_excluir[indice_registro_excluir]

        # Botão para confirmar a exclusão
        if st.button("Excluir Registro"):
            # Construir a condição WHERE (usando a chave primária ou todos os campos para garantir unicidade)
            where_condicao_excluir = " AND ".join([f"{k} = %s" for k in registro_excluir.keys()])
            valores_where_excluir = tuple(registro_excluir.values())

            # Executar a exclusão
            resultado_exclusao = deletar_registro(
                tabela=tabela_selecionada,
                where_condicao=where_condicao_excluir,
                valores_where=valores_where_excluir
            )

            # Exibir a tabela atualizada
            if resultado_exclusao["status"] == "sucesso":
                st.success(resultado_exclusao["mensagem"])
                st.write("Tabela atualizada:")
                st.table(resultado_exclusao["tabela_atualizada"])
            else:
                st.error(resultado_exclusao["mensagem"])
    else:
        st.warning(f"Nenhum registro encontrado na tabela '{tabela_selecionada}'.")
# Executar a aplicação
CRUD()