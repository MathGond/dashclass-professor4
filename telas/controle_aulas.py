import streamlit as st
import sqlite3

st.header("Controle de Aulas Dadas")

# Filtros de busca
nivel = st.selectbox("Filtrar por Nível:", ["Ensino Fundamental", "Ensino Médio", "Ensino Superior", "Curso Técnico / Outro"])
subnivel = ""
if nivel == "Ensino Fundamental":
    subnivel = st.selectbox("Filtrar por Ano:", [f"{i}º ano" for i in range(1, 10)])
elif nivel == "Ensino Médio":
    subnivel = st.selectbox("Filtrar por Ano:", ["1º ano", "2º ano", "3º ano"])
else:
    subnivel = st.text_input("Filtrar por Subnível (Ex: 1º período, Técnico 2, etc.):")

turno = st.selectbox("Filtrar por Turno:", ["Matutino", "Vespertino", "Noturno"])

# Buscar turmas compatíveis com o filtro
with sqlite3.connect("dashclass.db") as conn:
    c = conn.cursor()

    c.execute('''
        SELECT id, nome FROM turmas
        WHERE nivel = ? AND subnivel = ? AND turno = ?
    ''', (nivel, subnivel, turno))
    
    turmas = c.fetchall()

# Exibir turmas com aulas vinculadas
if turmas:
    turma_opcao = st.selectbox("Selecione a Turma:", turmas, format_func=lambda x: x[1])
    turma_id = turma_opcao[0]

    # Buscar aulas associadas a essa turma
    c.execute('''
        SELECT ca.id, d.nome, a.aula_num, a.titulo, ca.status
        FROM controle_aulas ca
        JOIN aulas a ON ca.aula_id = a.id
        JOIN disciplinas d ON a.disciplina_id = d.id
        WHERE ca.turma_id = ?
        ORDER BY d.nome, a.aula_num
    ''', (turma_id,))
    
    registros = c.fetchall()

    if registros:
        for controle_id, disciplina, aula_num, titulo, status in registros:
            marcado = (status == "✅")
            nova_marcacao = st.checkbox(f"{disciplina} - Aula {aula_num}: {titulo}", value=marcado, key=controle_id)
            novo_status = "✅" if nova_marcacao else "❌"
            if novo_status != status:
                c.execute("UPDATE controle_aulas SET status = ? WHERE id = ?", (novo_status, controle_id))
                conn.commit()
    else:
        st.warning("Esta turma ainda não tem aulas registradas.")
else:
    st.info("Nenhuma turma com aulas cadastradas para esse filtro.")
