
import streamlit as st
import pandas as pd
import os
import re # Usado para a busca de tecnologias

# --- Configuração da Página ---
# Define o título da aba do navegador e o layout da página
st.set_page_config(
    page_title="Ecossistema de Inovação MG",
    layout="wide"
)

# --- Carregamento dos Dados ---
# Dicionário que mapeia os nomes das seções aos seus respectivos arquivos CSV
ARQUIVOS_CSV = {
    "Executores": '../reports/classificacao_final_revisada.csv',
    "Base de Conhecimento e P&D": '../reports/base_conhecimento_pd.csv',
    "Demais Organizações": '../reports/demais_organizacoes.csv'
}

# Função com cache para carregar os dados, evitando recarregamentos desnecessários
@st.cache_data
def carregar_dados(caminho_do_arquivo):
    """Carrega um arquivo CSV a partir de um caminho, com tratamento de erro."""
    if not os.path.exists(caminho_do_arquivo):
        # Mostra um erro se o arquivo não for encontrado
        return None
    return pd.read_csv(caminho_do_arquivo)

# Carrega todos os dataframes definidos no dicionário ARQUIVOS_CSV
dataframes = {nome: carregar_dados(caminho) for nome, caminho in ARQUIVOS_CSV.items()}

# --- Barra Lateral (Sidebar) ---
st.sidebar.title("Navegação")
st.sidebar.markdown("Selecione uma visualização:")

# Menu principal para navegar entre as diferentes páginas do dashboard
paginas_principais = ["Visão Geral e Ficha Detalhada", "Busca Avançada", "Base de Conhecimento e P&D", "Visualização em Tabela"]
pagina_selecionada = st.sidebar.radio("Menu Principal:", paginas_principais)

# --- Corpo Principal do Dashboard ---
st.title("Mapeamento do Ecossistema de Inovação de Minas Gerais")

# ===== PÁGINA 1: VISÃO GERAL E FICHA DETALHADA (EXECUTORES) =====
if pagina_selecionada == "Visão Geral e Ficha Detalhada":
    st.header("Análise de Startups, EBTs e Médias/Grandes Empresas")
    
    df_executores = dataframes.get("Executores")
    
    if df_executores is not None:
        # --- VISUALIZAÇÕES AGREGADAS ---
        st.subheader("Panorama Geral")
        total_orgs = len(df_executores)
        total_cidades = df_executores['cidade_sede'].nunique()
        total_missoes = df_executores['missoes_finais'].nunique()
        
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Organizações Mapeadas", total_orgs)
        kpi2.metric("Cidades com Organizações", total_cidades)
        kpi3.metric("Combinações de Missões", total_missoes)
        st.divider()

        st.subheader("Distribuições e Tendências")
        col_graf1, col_graf2 = st.columns(2)
        
        with col_graf1:
            st.markdown("**Top 10 Cidades por Nº de Organizações**")
            cidades_contagem = df_executores['cidade_sede'].value_counts().nlargest(10).sort_values(ascending=True)
            st.bar_chart(cidades_contagem, horizontal=True)

        with col_graf2:
            st.markdown("**Distribuição por Fase do Negócio**")
            fase_contagem = df_executores['fase_negocio'].value_counts()
            st.bar_chart(fase_contagem)
        st.divider()

        # --- FICHA DETALHADA DA ORGANIZAÇÃO ---
        st.header("Ficha Detalhada da Organização")
        
        lista_orgs = sorted(df_executores['nome_organizacao'].unique())
        org_nome_selecionado = st.selectbox(
            "Selecione uma organização para ver os detalhes:",
            lista_orgs
        )
        
        org_dados = df_executores[df_executores['nome_organizacao'] == org_nome_selecionado].iloc[0]

        def mostrar_info(titulo, valor):
            if pd.notna(valor) and str(valor).strip() not in ["", " ", "não possui", "nan"]:
                st.markdown(f"**{titulo}:** {valor}")

        def mostrar_link(titulo, url):
            if pd.notna(url) and str(url).strip():
                st.markdown(f"**{titulo}:** [{url}]({url})")

        # Layout do Card
        st.divider()
        col1, col2 = st.columns([1, 4])
        with col1:
            if pd.notna(org_dados.get('logo_url')):
                st.image(org_dados['logo_url'], width=150)
        with col2:
            st.subheader(org_dados['nome_organizacao'])
            if pd.notna(org_dados.get('cidade_sede')):
                st.caption(f"📍 {org_dados['cidade_sede']} - {org_dados['uf_sede']}")
        
        st.markdown("**Missões Estratégicas:**")
        if pd.notna(org_dados.get('missoes_finais')):
            missoes = [m.strip() for m in str(org_dados['missoes_finais']).split(',')]
            cols = st.columns(len(missoes) if missoes else 1)
            for i, missao in enumerate(missoes):
                if missao: cols[i].button(missao, use_container_width=True, key=f"exec_missao_{i}")

        st.divider()

        tab_sobre, tab_negocio, tab_contato = st.tabs(["Sobre a Organização", "Negócio e Investimento", "Contato e Links"])
        with tab_sobre:
            st.subheader("Sobre a Organização")
            mostrar_info("Descrição", org_dados.get('descricao_organizacao'))
            mostrar_info("Tecnologias Disruptivas", org_dados.get('tecnologias_disruptivas'))
            mostrar_info("Áreas de Expertise", org_dados.get('areas_expertise_x'))
            mostrar_info("Categoria", org_dados.get('categoria_organizacao'))
            mostrar_info("Tipo", org_dados.get('tipo_organizacao_y'))

        with tab_negocio:
            st.subheader("Negócio e Investimento")
            mostrar_info("Fase do Negócio", org_dados.get('fase_negocio'))
            mostrar_info("Modelo de Negócio", org_dados.get('modelo_negocio'))
            mostrar_info("Segmento de Atuação", org_dados.get('segmento_atuacao'))
            mostrar_info("Segmentação de Clientes", org_dados.get('segmentacao_clientes'))
            mostrar_info("Número de Funcionários", org_dados.get('numero_funcionarios'))
            st.divider()
            mostrar_info("Busca Investimento?", org_dados.get('busca_investimento'))
            mostrar_info("Fase de Investimento já Captada", org_dados.get('fase_investimento_captada'))
            mostrar_info("Tese de Investimento", org_dados.get('tese_investimento'))

        with tab_contato:
            st.subheader("Contato e Links")
            mostrar_link("Website", org_dados.get('site_organizacao'))
            mostrar_link("LinkedIn", org_dados.get('linkedin_url'))
            mostrar_info("Email para Contato", org_dados.get('email_contato'))
    else:
        st.warning("Dados dos Executores não puderam ser carregados. Verifique o caminho do arquivo.")

# ===== PÁGINA 2: BUSCA AVANÇADA =====
elif pagina_selecionada == "Busca Avançada":
    st.header("Busca Avançada de Organizações")
    st.markdown("Use os filtros abaixo para encontrar organizações com perfis específicos.")
    
    df_busca = dataframes.get("Executores")
    
    if df_busca is not None:
        techs = df_busca['tecnologias_disruptivas'].dropna().str.split(',').explode().str.strip().unique()
        categorias = df_busca['categoria_organizacao'].dropna().unique()
        segmentos = df_busca['segmento_atuacao'].dropna().unique()

        col1, col2, col3 = st.columns(3)
        with col1:
            techs_selecionadas = st.multiselect("Tecnologias Disruptivas:", sorted(techs))
        with col2:
            categorias_selecionadas = st.multiselect("Categoria da Organização:", sorted(categorias))
        with col3:
            segmentos_selecionados = st.multiselect("Segmento de Atuação:", sorted(segmentos))

        df_filtrado = df_busca.copy()

        if techs_selecionadas:
            regex_techs = '|'.join([re.escape(t) for t in techs_selecionadas])
            df_filtrado = df_filtrado[df_filtrado['tecnologias_disruptivas'].str.contains(regex_techs, na=False)]
        
        if categorias_selecionadas:
            df_filtrado = df_filtrado[df_filtrado['categoria_organizacao'].isin(categorias_selecionadas)]

        if segmentos_selecionados:
            df_filtrado = df_filtrado[df_filtrado['segmento_atuacao'].isin(segmentos_selecionados)]

        st.divider()
        st.subheader("Resultados da Busca")

        if not df_filtrado.empty:
            st.success(f"**{len(df_filtrado)}** organizações encontradas com os critérios selecionados.")
            colunas_para_exibir = [
                'nome_organizacao', 'cidade_sede', 'missoes_finais', 
                'tecnologias_disruptivas', 'categoria_organizacao', 'segmento_atuacao'
            ]
            st.dataframe(df_filtrado[colunas_para_exibir])
        else:
            st.warning("Nenhuma organização encontrada com os critérios selecionados. Tente uma busca mais ampla.")
    else:
        st.warning("Dados dos Executores não puderam ser carregados para a busca.")

# ===== PÁGINA 3: BASE DE CONHECIMENTO E P&D =====
# ===== PÁGINA 3: BASE DE CONHECIMENTO E P&D (COM FILTRO) =====
elif pagina_selecionada == "Base de Conhecimento e P&D":
    st.header("Análise da Base de Conhecimento e P&D")
    
    df_pesquisa = dataframes.get("Base de Conhecimento e P&D")
    
    if df_pesquisa is not None:
        
        # --- NOVO FILTRO POR TIPO DE ORGANIZAÇÃO ---
        st.subheader("Filtros")
        
        # Prepara as opções para o filtro, removendo valores nulos e pegando os únicos
        if 'tipo_organizacao_y' in df_pesquisa.columns:
            tipos_org = df_pesquisa['tipo_organizacao_y'].dropna().unique()
            tipos_selecionados = st.multiselect(
                "Filtre por Tipo de Organização:",
                sorted(tipos_org),
                placeholder="Selecione um ou mais tipos"
            )
        else:
            tipos_selecionados = []
            st.info("A coluna 'tipo_organizacao_y' não foi encontrada para este filtro.")

        # Aplica o filtro ao dataframe
        if tipos_selecionados:
            df_filtrado = df_pesquisa[df_pesquisa['tipo_organizacao_y'].isin(tipos_selecionados)]
        else:
            # Se nenhum filtro for selecionado, usa o dataframe completo
            df_filtrado = df_pesquisa
        
        st.divider()

        # --- VISUALIZAÇÕES AGREGADAS (AGORA USAM O DF FILTRADO) ---
        
        # Verifica se o dataframe filtrado não está vazio antes de continuar
        if not df_filtrado.empty:
            st.subheader("Panorama Geral")
            total_inst = len(df_filtrado)
            total_cidades_pesquisa = df_filtrado['cidade_sede'].nunique()
            
            total_com_nit = 0
            if 'possui_nit' in df_filtrado.columns:
                df_filtrado['possui_nit'] = df_filtrado['possui_nit'].astype(str)
                total_com_nit = df_filtrado[df_filtrado['possui_nit'].str.upper() == 'SIM'].shape[0]
            
            kpi1, kpi2, kpi3 = st.columns(3)
            kpi1.metric("Instituições Encontradas", total_inst)
            kpi2.metric("Cidades Atendidas", total_cidades_pesquisa)
            kpi3.metric("Instituições com NIT", total_com_nit)
            st.divider()

            st.subheader("Distribuições e Áreas de Foco")
            col_graf1, col_graf2 = st.columns(2)
            
            with col_graf1:
                st.markdown("**Top 10 Cidades por Nº de Instituições**")
                cidades_contagem = df_filtrado['cidade_sede'].value_counts().nlargest(10).sort_values(ascending=True)
                st.bar_chart(cidades_contagem, horizontal=True)

            with col_graf2:
                st.markdown("**Top 10 Áreas de Expertise**")
                if 'areas_expertise_x' in df_filtrado.columns:
                    areas_expertise = df_filtrado['areas_expertise_x'].dropna().str.split(',').explode().str.strip()
                    areas_contagem = areas_expertise.value_counts().nlargest(10).sort_values(ascending=True)
                    st.bar_chart(areas_contagem, horizontal=True)
                else:
                    st.info("A coluna 'areas_expertise_x' não foi encontrada.")
            st.divider()

            # --- FICHA DETALHADA (AGORA USA A LISTA FILTRADA) ---
            st.header("Ficha Detalhada da Instituição")
            
            lista_inst = sorted(df_filtrado['nome_organizacao'].unique())
            inst_nome_selecionado = st.selectbox(
                "Selecione uma instituição para ver os detalhes:",
                lista_inst,
                key="select_inst_pesquisa"
            )
            
            if inst_nome_selecionado:
                inst_dados = df_filtrado[df_filtrado['nome_organizacao'] == inst_nome_selecionado].iloc[0]

                def mostrar_info(titulo, valor_chave):
                    valor = inst_dados.get(valor_chave)
                    if pd.notna(valor) and str(valor).strip() not in ["", " ", "não possui", "nan"]:
                        st.markdown(f"**{titulo}:** {valor}")
                
                st.divider()
                col1, col2 = st.columns([1, 4])
                with col1:
                    logo_url = inst_dados.get('logo_url')
                    if pd.notna(logo_url) and str(logo_url).strip():
                        st.image(logo_url, width=150)
                with col2:
                    st.subheader(inst_dados['nome_organizacao'])
                    if pd.notna(inst_dados.get('cidade_sede')):
                        st.caption(f"📍 {inst_dados['cidade_sede']} - {inst_dados['uf_sede']}")
                    mostrar_info("Possui NIT?", 'possui_nit')

                st.divider()

                tab_sobre, tab_contato = st.tabs(["Sobre e Expertise", "Contato"])
                with tab_sobre:
                    st.subheader("Sobre a Instituição")
                    mostrar_info("Descrição", 'descricao_organizacao')
                    st.subheader("Expertise")
                    mostrar_info("Áreas de Expertise", 'areas_expertise_x')

                with tab_contato:
                    st.subheader("Informações de Contato")
                    if pd.notna(inst_dados.get('site_organizacao')):
                        st.markdown(f"**Website:** [{inst_dados['site_organizacao']}]({inst_dados['site_organizacao']})")
                    mostrar_info("Email para Contato", 'email_contato')
                    mostrar_info("Contato para Divulgação Científica", 'contato_divulgacao_cientifica')
            else:
                st.info("Nenhuma instituição selecionada.")
        else:
            st.warning("Nenhuma organização encontrada com os filtros selecionados. Tente uma busca mais ampla.")

    else:
        st.warning("Dados da Base de Conhecimento e P&D não puderam ser carregados.")
# ===== PÁGINA 4: VISUALIZAÇÃO EM TABELA =====
elif pagina_selecionada == "Visualização em Tabela":
    st.header("Visualização por Segmento do Ecossistema")
    
    grupo_tabela = st.selectbox(
        "Selecione o grupo para visualizar em formato de tabela:",
        list(ARQUIVOS_CSV.keys())
    )
    
    df_selecionado = dataframes.get(grupo_tabela)
    if df_selecionado is not None:
        st.success(f"Exibindo **{len(df_selecionado)}** organizações.")
        st.dataframe(df_selecionado)
    else:
        st.warning("Dados não carregados.")
