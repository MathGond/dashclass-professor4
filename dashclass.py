import streamlit as st
from pathlib import Path
import sqlite3  # ✅ necessário para verificar turmas no banco

# Configuração da interface
st.set_page_config(page_title="DashClass", layout="centered")
st.markdown("<h2 style='text-align: center;'>DashClass - Gerenciamento de Aulas</h2>", unsafe_allow_html=True)

# Função para checar se o banco já tem turmas cadastradas
def usuario_tem_turmas():
    try:
        with sqlite3.connect("dashclass.db") as conn:
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM turmas")
            total = c.fetchone()[0]
            return total > 0
    except:
        return False

# Menu lateral
st.sidebar.markdown("### Navegação")
menu_opcoes = [
    "Cadastro de Turmas",
    "Turmas Cadastradas",
    "Registro de Aulas",
    "Controle de Aulas Dadas",
    "Gráfico de Aulas Dadas",
    "Visualizar Aulas Registradas",
    "Excluir Disciplina"
]

# Define a tela inicial com base no uso do app
if "menu" not in st.session_state:
    if usuario_tem_turmas():
        st.session_state["menu"] = "Controle de Aulas Dadas"
    else:
        st.session_state["menu"] = "Cadastro de Turmas"

# Interface de navegação
menu = st.sidebar.radio("Selecione a opção desejada:", menu_opcoes, index=menu_opcoes.index(st.session_state["menu"]))


# Caminho base para as telas
tela_path = Path("telas")

# Mapeamento das telas para seus respectivos arquivos .py
telas = {
    "Cadastro de Turmas": "cadastro_turmas.py",
    "Turmas Cadastradas": "turmas_cadastradas.py",  # ✅ NOVA TELA
    "Registro de Aulas": "registro_aulas.py",
    "Controle de Aulas Dadas": "controle_aulas.py",
    "Gráfico de Aulas Dadas": "graficos.py",
    "Visualizar Aulas Registradas": "visualizar_aulas.py",
    "Excluir Turma": "excluir_turma.py",
    "Excluir Disciplina": "excluir_disciplina.py"
}

# Execução da tela selecionada
tela_arquivo = tela_path / telas[menu]

if tela_arquivo.exists():
    with open(tela_arquivo, "r", encoding="utf-8") as f:
        exec(f.read())
else:
    st.error("Tela não encontrada. Verifique se o arquivo existe em /telas.")
