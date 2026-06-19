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

# Mapeamento e Navegação das 10 consultas reais encontradas no template
st.sidebar.header("🔍 Navegação por Consultas")
opcao = st.sidebar.selectbox(
    "Escolha uma consulta do TP:",
    [
        "Selecione uma opção...",
        "6.1.1 - Escolas Federais em MG",
        "6.1.2 - Cursos Técnicos (Informação e Comunicação)",
        "6.2.1 - Maiores Escolas em Número de Docentes",
        "6.2.2 - Quantidade de Escolas por Estado (UF)",
        "6.2.3 - Tipo de Vínculo de Docentes por Região",
        "6.3.1 - Alunos Matriculados por Sexo e Cor/Raça",
        "6.3.2 - Escolas com Mais Turmas de EJA",
        "6.3.3 - Escolas que Ofertam Cursos da Área de Saúde",
        "6.4.1 - Escolas sem Acesso à Internet por Região",
        "6.4.2 - Cursos Mais Ofertados no Brasil"
    ]
)

# Função auxiliar para carregar arquivos CSV com tratamento de erro
def carregar_dados(nome_arquivo):
    if os.path.exists(nome_arquivo):
        return pd.read_csv(nome_arquivo)
    else:
        st.warning(f"⚠️ O arquivo `{nome_arquivo}` ainda não foi adicionado ao repositório GitHub. Exibindo dados simulados de amostra.")
        return None

# Lógica das Opções da Tela
if opcao == "Selecione uma opção...":
    st.info("💡 Escolha uma das consultas na barra lateral esquerda para visualizar o comando SQL, a tabela gerada e os gráficos interativos.")

# --- CONSULTA 1 ---
elif opcao == "6.1.1 - Escolas Federais em MG":
    st.header("🏫 6.1.1 - Escolas da Rede Federal em Minas Gerais")
    st.write("Retorna o nome e a cidade de todas as escolas que pertencem à rede federal e que estão localizadas no estado de Minas Gerais.")
    
    sql = """SELECT e.nome_escola, l.municipio
FROM Escola e
JOIN Localizacao l ON e.Clocalizacao = l.cod_localizacao
WHERE e.rede_ensino = 'Federal' AND l.sigla_uf = 'MG'
ORDER BY l.municipio, e.nome_escola;"""
    
    with st.expander("📄 Ver Comando SQL Utilizado", expanded=True):
        st.code(sql, language="sql")
        
    df = carregar_dados("consulta1.csv")
    if df is None:
        df = pd.DataFrame({"nome_escola": ["IFMG Campus Ouro Preto", "CEFET-MG Campus I"], "municipio": ["Ouro Preto", "Belo Horizonte"]})
        
    st.subheader("📋 Resultado da Consulta")
    st.dataframe(df, use_container_width=True)

# --- CONSULTA 2 ---
elif opcao == "6.1.2 - Cursos Técnicos (Informação e Comunicação)":
    st.header("💻 6.1.2 - Cursos Técnicos da Área de Informação e Comunicação")
    st.write("Retorna o nome de todos os cursos técnicos cuja área de especialização é 'Informação e Comunicação'.")
    
    sql = """SELECT c.nome_curso, COUNT(fc.Cescola) AS qtd_escolas_ofertantes
FROM Curso c
JOIN Fornece_curso fc ON c.cod_curso = fc.Ccurso
WHERE c.area_curso = 'Informação e comunicação'
GROUP BY c.nome_curso
ORDER BY qtd_escolas_ofertantes DESC;"""
    
    with st.expander("📄 Ver Comando SQL Utilizado", expanded=True):
        st.code(sql, language="sql")
        
    df = carregar_dados("consulta2.csv")
    if df is None:
        df = pd.DataFrame({"nome_curso": ["Informática", "Desenvolvimento de Sistemas", "Redes de Computadores"], "qtd_escolas_ofertantes": [120, 85, 40]})
        
    st.subheader("📋 Resultado da Consulta")
    st.dataframe(df, use_container_width=True)
    
    st.subheader("📊 Gráfico Relacionado")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.barplot(data=df.head(10), x="qtd_escolas_ofertantes", y="nome_curso", ax=ax, palette="Blues_r")
    st.pyplot(fig)

# --- CONSULTA 3 ---
elif opcao == "6.2.1 - Maiores Escolas em Número de Docentes":
    st.header("👥 6.2.1 - Top 10 Escolas em Número de Docentes")
    st.write("Retorna o nome das escolas, municípios e o total de docentes alocados, listando as maiores instituições.")
    
    sql = """SELECT e.nome_escola, l.municipio, COUNT(d.co_docente) as total_docentes
-- Ajuste com base no seu notebook real
LIMIT 10;"""
    with st.expander("📄 Ver Comando SQL Utilizado"):
        st.code(sql, language="sql")
        
    df = carregar_dados("consulta3.csv")
    st.subheader("📋 Tabela de Resultados")
    if df is not None: st.dataframe(df, use_container_width=True)

# --- CONSULTA 4 ---
elif opcao == "6.2.2 - Quantidade de Escolas por Estado (UF)":
    st.header("🗺️ 6.2.2 - Concentração de Escolas por Estado")
    
    sql = """SELECT estado, quantidade_escolas FROM ..."""
    with st.expander("📄 Ver Comando SQL Utilizado"): st.code(sql, language="sql")
        
    df = carregar_dados("consulta4.csv")
    if df is not None:
        st.dataframe(df, use_container_width=True)
        st.subheader("📊 Distribuição de Escolas")
        fig, ax = plt.subplots(figsize=(12, 5))
        sns.barplot(data=df.sort_values(by="quantidade_escolas", ascending=False), x="estado", y="quantidade_escolas", ax=ax, palette="viridis")
        st.pyplot(fig)

# --- CONSULTA 5 ---
elif opcao == "6.2.3 - Tipo de Vínculo de Docentes por Região":
    st.header("👔 6.2.3 - Vínculos Empregatícios por Região do País")
    
    sql = """SELECT l.regiao, dv.tipo_vinculo, total_docentes FROM ..."""
    with st.expander("📄 Ver Comando SQL Utilizado"): st.code(sql, language="sql")
        
    df = carregar_dados("consulta5.csv")
    if df is not None:
        st.dataframe(df, use_container_width=True)
        st.subheader("📊 Tipo de Contrato por Região")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(data=df, x="regiao", y="total_docentes", hue="tipo_vinculo", ax=ax)
        st.pyplot(fig)

# --- CONSULTA 6 ---
elif opcao == "6.3.1 - Alunos Matriculados por Sexo e Cor/Raça":
    st.header("📊 6.3.1 - Perfil Demográfico de Matrículas")
    df = carregar_dados("consulta6.csv")
    if df is not None: st.dataframe(df, use_container_width=True)

# --- CONSULTA 7 ---
elif opcao == "6.3.2 - Escolas com Mais Turmas de EJA":
    st.header("🌙 6.3.2 - Escolas com Maior Número de Ofertas para EJA")
    df = carregar_dados("consulta7.csv")
    if df is not None: st.dataframe(df, use_container_width=True)

# --- CONSULTA 8 ---
elif opcao == "6.3.3 - Escolas que Ofertam Cursos da Área de Saúde":
    st.header("🏥 6.3.3 - Oferta de Cursos Técnicos voltados à Saúde")
    df = carregar_dados("consulta8.csv")
    if df is not None: st.dataframe(df, use_container_width=True)

# --- CONSULTA 9 ---
elif opcao == "6.4.1 - Escolas sem Acesso à Internet por Região":
    st.header("🌐 6.4.1 - Análise de Infraestrutura Digital e Conectividade")
    df = carregar_dados("consulta9.csv")
    if df is not None:
        st.dataframe(df, use_container_width=True)
        st.subheader("📊 Taxa sem Internet por Estado")
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.barplot(data=df, x="estado", y="taxa_sem_internet", ax=ax, palette="Reds_r")
        st.pyplot(fig)

# --- CONSULTA 10 ---
elif opcao == "6.4.2 - Cursos Mais Ofertados no Brasil":
    st.header("📈 6.4.2 - Cursos Técnicos Mais Ofertados no Território Nacional")
    df = carregar_dados("consulta10.csv")
    if df is not None: st.dataframe(df, use_container_width=True)