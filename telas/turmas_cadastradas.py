import streamlit as st
import sqlite3

st.header("📚 Turmas Cadastradas")

# Função para listar e excluir turmas
def exibir_turmas():
    with sqlite3.connect("dashclass.db") as conn:
        c = conn.cursor()
        c.execute("SELECT id, nome, nivel, subnivel, turno FROM turmas")
        turmas = c.fetchall()

        if not turmas:
            st.info("Nenhuma turma cadastrada.")
            return

        for turma in turmas:
            tid, nome, nivel, subnivel, turno = turma
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"**{nome}** ({subnivel} do {nivel}, {turno})")
            with col2:
                if st.button("Excluir", key=f"excluir_{tid}"):
                    excluir_turma(tid)
                    st.success(f"Turma '{nome}' excluída com sucesso!")
                    st.rerun()

# Função para exclusão
def excluir_turma(turma_id):
    with sqlite3.connect("dashclass.db") as conn:
        c = conn.cursor()
        c.execute("DELETE FROM controle_aulas WHERE turma_id = ?", (turma_id,))
        c.execute("DELETE FROM turmas WHERE id = ?", (turma_id,))
        conn.commit()

exibir_turmas()
