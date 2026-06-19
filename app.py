import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configuração da Página
st.set_page_config(
    page_title="Dashboard - Censo Escolar 2025",
    page_icon="📚",
    layout="wide"
)

# Título e cabeçalho do projeto
st.title("📊 Painel Interativo - Censo Escolar 2025")
st.markdown("## Disciplina: Introdução a Bancos de Dados")

# Barra Lateral - Informações dos Membros
st.sidebar.header("🎓 Membros do Grupo")
st.sidebar.info("""
- **Eduardo Henrique Oliveira de Sousa** (2026422871)
- **José Gabriel Claret Barbosa** (2025049522)
- **Joao Vitor de Sales Fonseca Santos** (2025050792)
- **Pedro Henrique Ribeiro Oliveira** (2024013478)
""")

# Navegação
st.sidebar.header("🔍 Navegação por Consultas")
opcao = st.sidebar.selectbox(
    "Escolha uma consulta do TP:",
    [
        "Selecione uma opção...",
        "6.1.1 - Escolas Federais em MG",
        "6.1.2 - Cursos Técnicos (Informação e Comunicação)",
        "6.2.1 - Maiores Escolas em Número de Docentes",
        "6.2.2 - Quantidade de Escolas por Estado (UF)",
        "6.2.3 - Quantidade de Turmas por Etapa",
        "6.3.1 - Vínculos de Docentes por Região",
        "6.3.2 - Escolas com Mais Turmas de EJA",
        "6.3.3 - Escolas que Ofertam Cursos da Área de Saúde",
        "6.4.1 - Escolas sem Acesso à Internet por Região",
        "6.4.2 - Cursos Mais Ofertados no Brasil"
    ]
)

# Função auxiliar para carregar arquivos CSV
def carregar_dados(nome_arquivo):
    if os.path.exists(nome_arquivo):
        return pd.read_csv(nome_arquivo)
    else:
        st.error(f"❌ Arquivo `{nome_arquivo}` não encontrado no GitHub. Certifique-se de fazer o upload do ZIP extraído.")
        return None

if opcao == "Selecione uma opção...":
    st.info("💡 Escolha uma das consultas na barra lateral esquerda para visualizar o comando SQL, a tabela gerada e os gráficos.")

# --- CONSULTA 6.1.1 ---
elif opcao == "6.1.1 - Escolas Federais em MG":
    st.header("🏫 6.1.1 - Escolas da Rede Federal em Minas Gerais")
    
    sql = """SELECT e.nome_escola, l.municipio
FROM Escola e
JOIN Localizacao l ON e.Clocalizacao = l.cod_localizacao
WHERE e.rede_ensino = 'Federal' AND l.sigla_uf = 'MG'
ORDER BY l.municipio, e.nome_escola;"""
    
    with st.expander("📄 Ver Comando SQL Utilizado", expanded=True):
        st.code(sql, language="sql")
        
    df = carregar_dados("consulta1.csv")
    if df is not None:
        st.subheader("📋 Resultado da Consulta")
        st.dataframe(df, use_container_width=True)
        
        st.subheader("📊 Visualização Gráfica")
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.countplot(data=df, y='municipio', ax=ax, palette='viridis', order=df['municipio'].value_counts().index[:10])
        ax.set_title("Top 10 Municípios de MG com mais Escolas Federais")
        st.pyplot(fig)

# --- CONSULTA 6.1.2 ---
elif opcao == "6.1.2 - Cursos Técnicos (Informação e Comunicação)":
    st.header("💻 6.1.2 - Cursos Técnicos da Área de Informação e Comunicação")
    
    sql = """SELECT c.nome_curso, COUNT(fc.Cescola) AS qtd_escolas_ofertantes
FROM Curso c
JOIN Fornece_curso fc ON c.cod_curso = fc.Ccurso
WHERE c.area_curso = 'Informação e comunicação'
GROUP BY c.nome_curso
ORDER BY qtd_escolas_ofertantes DESC;"""
    
    with st.expander("📄 Ver Comando SQL Utilizado", expanded=True):
        st.code(sql, language="sql")
        
    df = carregar_dados("consulta2.csv")
    if df is not None:
        st.subheader("📋 Resultado da Consulta")
        st.dataframe(df, use_container_width=True)
        
        st.subheader("📊 Gráfico Relacionado")
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.barplot(data=df.head(10), x="qtd_escolas_ofertantes", y="nome_curso", ax=ax, palette="Blues_r")
        st.pyplot(fig)

# --- CONSULTA 6.2.1 ---
elif opcao == "6.2.1 - Maiores Escolas em Número de Docentes":
    st.header("👥 6.2.1 - Top 10 Escolas em Número de Docentes (Região Sudeste)")
    
    sql = """SELECT e.nome_escola, l.municipio, COUNT(d.co_docente) as total_docentes
FROM Escola e 
JOIN Localizacao l ON e.Clocalizacao = l.cod_localizacao
JOIN Docente d ON e.cod_escola = d.Cescola
WHERE l.regiao = 'Sudeste'
GROUP BY e.nome_escola, l.municipio
ORDER BY total_docentes DESC
LIMIT 10;"""
    
    with st.expander("📄 Ver Comando SQL Utilizado"):
        st.code(sql, language="sql")
        
    df = carregar_dados("consulta3.csv")
    if df is not None:
        st.subheader("📋 Tabela de Resultados")
        st.dataframe(df, use_container_width=True)
        
        st.subheader("📊 Gráfico das Maiores Escolas")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(data=df, x="total_docentes", y="nome_escola", ax=ax, palette="flare")
        st.pyplot(fig)

# --- CONSULTA 6.2.2 ---
elif opcao == "6.2.2 - Quantidade de Escolas por Estado (UF)":
    st.header("🗺️ 6.2.2 - Quantidade de Escolas por Estado")
    
    sql = """SELECT l.sigla_uf, COUNT(e.cod_escola) AS quantidade_escolas
FROM Escola e
JOIN Localizacao l ON e.Clocalizacao = l.cod_localizacao
GROUP BY l.sigla_uf
ORDER BY quantidade_escolas DESC;"""
    
    with st.expander("📄 Ver Comando SQL Utilizado"):
        st.code(sql, language="sql")
        
    df = carregar_dados("consulta4.csv")
    if df is not None:
        st.subheader("📋 Tabela de Resultados")
        st.dataframe(df, use_container_width=True)
        
        st.subheader("📊 Distribuição de Escolas por Estado")
        fig, ax = plt.subplots(figsize=(12, 5))
        sns.barplot(data=df, x="sigla_uf", y="quantidade_escolas", ax=ax, palette="viridis")
        ax.set_xlabel("Estado (UF)")
        ax.set_ylabel("Quantidade de Escolas")
        st.pyplot(fig)

# --- CONSULTA 6.2.3 ---
elif opcao == "6.2.3 - Quantidade de Turmas por Etapa":
    st.header("📋 6.2.3 - Quantidade de Turmas por Etapa de Ensino")
    
    sql = """SELECT tx_etapa_ensino, COUNT(cod_turma) as quantidade_turmas
FROM turma
GROUP BY tx_etapa_ensino
ORDER BY quantidade_turmas DESC;"""
    
    with st.expander("📄 Ver Comando SQL Utilizado", expanded=True):
        st.code(sql, language="sql")
        
    df = carregar_dados("consulta5.csv")
    if df is not None:
        st.subheader("📋 Resultado da Consulta")
        st.dataframe(df, use_container_width=True)
        
        st.subheader("📊 Gráfico de Distribuição")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(data=df.head(10), x="quantidade_turmas", y="tx_etapa_ensino", ax=ax, palette="mako")
        ax.set_title("Top 10 Etapas de Ensino com Mais Turmas")
        st.pyplot(fig)

# --- CONSULTA 6.3.1 ---
elif opcao == "6.3.1 - Vínculos de Docentes por Região":
    st.header("👔 6.3.1 - Vínculos Empregatícios por Região do País")
    
    sql = """SELECT l.regiao, dv.tipo_vinculo, SUM(dv.quant) AS total_docentes
FROM Docente_Vinculo dv
JOIN Escola e ON dv.Cescola = e.cod_escola
JOIN Localizacao l ON e.Clocalizacao = l.cod_localizacao
GROUP BY l.regiao, dv.tipo_vinculo
ORDER BY l.regiao, total_docentes DESC;"""
    
    with st.expander("📄 Ver Comando SQL Utilizado"):
        st.code(sql, language="sql")
        
    df = carregar_dados("consulta6.csv")
    if df is not None:
        st.subheader("📋 Resultado da Consulta")
        st.dataframe(df, use_container_width=True)
        
        st.subheader("📊 Distribuição de Vínculos por Região")
        fig, ax = plt.subplots(figsize=(12, 5))
        sns.barplot(data=df, x="regiao", y="total_docentes", hue="tipo_vinculo", ax=ax, palette="muted")
        st.pyplot(fig)

# --- CONSULTA 6.3.2 ---
elif opcao == "6.3.2 - Escolas com Mais Turmas de EJA":
    st.header("🌙 6.3.2 - Escolas com Maior Número de Ofertas para EJA")
    
    sql = """SELECT e.nome_escola, l.municipio, COUNT(t.cod_turma) AS qtd_turmas_eja
FROM escola e
JOIN localizacao l ON e.Clocalizacao = l.cod_localizacao
JOIN turma t ON e.cod_escola = t.Cescola
WHERE t.tx_etapa_ensino LIKE '%EJA%' OR t.tx_etapa_ensino LIKE '%Educação de Jovens e Adultos%'
GROUP BY e.nome_escola, l.municipio
ORDER BY qtd_turmas_eja DESC
LIMIT 10;"""
    
    with st.expander("📄 Ver Comando SQL Utilizado"):
        st.code(sql, language="sql")
        
    df = carregar_dados("consulta7.csv")
    if df is not None:
        st.subheader("📋 Resultado da Consulta")
        st.dataframe(df, use_container_width=True)
        
        st.subheader("📊 Top 10 Escolas em Oferta EJA")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(data=df, x="qtd_turmas_eja", y="nome_escola", ax=ax, palette="coolwarm")
        st.pyplot(fig)

# --- CONSULTA 6.3.3 ---
elif opcao == "6.3.3 - Escolas que Ofertam Cursos da Área de Saúde":
    st.header("🏥 6.3.3 - Estados que possuem mais Escolas que Oferecem Cursos na Área de Saúde")
    
    sql = """SELECT l.sigla_uf, COUNT(DISTINCT e.cod_escola) AS qtd_escolas_saude
FROM Escola e
JOIN Localizacao l ON e.Clocalizacao = l.cod_localizacao
JOIN Fornece_curso fc ON e.cod_escola = fc.Cescola
JOIN Curso c ON fc.Ccurso = c.cod_curso
WHERE c.area_curso = 'Ambiente e saúde'
GROUP BY l.sigla_uf
ORDER BY qtd_escolas_saude DESC;"""
    
    with st.expander("📄 Ver Comando SQL Utilizado"):
        st.code(sql, language="sql")
        
    df = carregar_dados("consulta8.csv")
    if df is not None:
        st.subheader("📋 Resultado da Consulta")
        st.dataframe(df, use_container_width=True)
        
        st.subheader("📊 Ranking de Estados com Cursos na Área de Saúde")
        fig, ax = plt.subplots(figsize=(12, 4))
        sns.barplot(data=df, x="sigla_uf", y="qtd_escolas_saude", ax=ax, palette="YlGnBu_r")
        st.pyplot(fig)

# --- CONSULTA 6.4.1 ---
elif opcao == "6.4.1 - Escolas sem Acesso à Internet por Região":
    st.header("🌐 6.4.1 - Estados com Mais Escolas sem Acesso à Internet")
    st.write("Retorna o ranking de estados (UF) com o maior número absoluto de estabelecimentos de ensino sem internet.")
    
    query_641 = """SELECT l.sigla_uf, COUNT(e.cod_escola) AS qtd_escolas_sem_internet
FROM escola e
JOIN localizacao l ON e.Clocalizacao = l.cod_localizacao
WHERE e.inf_internet = 'Não'
GROUP BY l.sigla_uf
ORDER BY qtd_escolas_sem_internet DESC
LIMIT 5;"""
    
    with st.expander("📄 Ver Comando SQL Utilizado", expanded=True):
        st.code(query_641, language="sql")
        
    df = carregar_dados("consulta9.csv")
    if df is not None:
        st.subheader("📋 Resultado da Consulta")
        st.dataframe(df, use_container_width=True)
        
        st.subheader("📊 Visualização Gráfica")
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.barplot(data=df, x="sigla_uf", y="qtd_escolas_sem_internet", ax=ax, palette="Reds_r")
        ax.set_title("Top 5 Estados em Número de Escolas Sem Internet")
        ax.set_xlabel("Estado (UF)")
        ax.set_ylabel("Quantidade de Escolas")
        st.pyplot(fig)

# --- CONSULTA 6.4.2 ---
elif opcao == "6.4.2 - Cursos Mais Ofertados no Brasil":
    st.header("📈 6.4.2 - Cursos Técnicos Mais Ofertados no Território Nacional")
    
    sql = """SELECT c.nome_curso, COUNT(fc.Cescola) AS qtd_escolas
FROM Curso c
JOIN Fornece_curso fc ON c.cod_curso = fc.Ccurso
GROUP BY c.nome_curso
ORDER BY qtd_escolas DESC;"""
    
    with st.expander("📄 Ver Comando SQL Utilizado"):
        st.code(sql, language="sql")
        
    df = carregar_dados("consulta10.csv")
    if df is not None:
        st.subheader("📋 Resultado da Consulta")
        st.dataframe(df, use_container_width=True)
        
        st.subheader("📊 Os 15 Cursos Técnicos mais Ofertados do País")
        fig, ax = plt.subplots(figsize=(10, 6))
        # Exibe os 15 primeiros conforme o gráfico planejado no notebook
        sns.barplot(data=df.head(15), x="qtd_escolas", y="nome_curso", ax=ax, palette="crest")
        st.pyplot(fig)