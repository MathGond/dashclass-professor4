import streamlit as st
import sqlite3

def obter_disciplinas():
    with sqlite3.connect("dashclass.db") as conn:
        c = conn.cursor()
        c.execute("SELECT id, nome FROM disciplinas")
        return c.fetchall()

def obter_aulas(disciplina_id):
    with sqlite3.connect("dashclass.db") as conn:
        c = conn.cursor()
        c.execute("SELECT id, aula_num, titulo, conteudo FROM aulas WHERE disciplina_id = ? ORDER BY aula_num", (disciplina_id,))
        return c.fetchall()

def atualizar_aula(aula_id, aula_num, titulo, conteudo):
    with sqlite3.connect("dashclass.db") as conn:
        c = conn.cursor()
        c.execute("""
            UPDATE aulas
            SET aula_num = ?, titulo = ?, conteudo = ?
            WHERE id = ?
        """, (aula_num, titulo, conteudo, aula_id))
        conn.commit()

def excluir_aula(aula_id):
    with sqlite3.connect("dashclass.db") as conn:
        c = conn.cursor()
        c.execute("DELETE FROM controle_aulas WHERE aula_id = ?", (aula_id,))
        c.execute("DELETE FROM aulas WHERE id = ?", (aula_id,))
        conn.commit()

# Interface
st.header("Visualizar, Editar e Excluir Aulas Registradas")

disciplinas = obter_disciplinas()
if disciplinas:
    disciplina = st.selectbox("Selecione a Disciplina:", disciplinas, format_func=lambda x: x[1])
    aulas = obter_aulas(disciplina[0])

    if not aulas:
        st.info("Nenhuma aula registrada para esta disciplina.")
    else:
        for aula_id, aula_num, titulo, conteudo in aulas:
            with st.expander(f"Aula {aula_num}: {titulo}"):
                novo_num = st.number_input("Número da Aula", value=aula_num, key=f"num_{aula_id}")
                novo_titulo = st.text_input("Título", value=titulo, key=f"titulo_{aula_id}")
                novo_conteudo = st.text_area("Conteúdo", value=conteudo, height=150, key=f"cont_{aula_id}")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Salvar Alterações", key=f"save_{aula_id}"):
                        atualizar_aula(aula_id, novo_num, novo_titulo, novo_conteudo)
                        st.success("Aula atualizada com sucesso!")
                        st.experimental_rerun()
                with col2:
                    if st.button("Excluir Aula", key=f"del_{aula_id}"):
                        excluir_aula(aula_id)
                        st.warning("Aula excluída com sucesso!")
                        st.experimental_rerun()
else:
    st.info("Nenhuma disciplina cadastrada ainda.")
