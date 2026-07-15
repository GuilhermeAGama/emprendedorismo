import streamlit as st

from dependecies import (
    question_service,
    correction_service
)

st.title("Correção de Questões")

# ===============================
# Carrega questões
# ===============================

questions = question_service.list_questions()

if not questions:
    st.warning("Nenhuma questão cadastrada.")
    st.stop()

options = {
    q["enunciado"]: q
    for q in questions
}

selected = st.selectbox(
    "Questão",
    list(options.keys())
)

resposta = st.text_area(
    "Resposta do aluno"
)

# ===============================
# Corrigir
# ===============================

if st.button("Corrigir"):

    question = options[selected]

    resultado = correction_service.correct(
        question["questao_id"],
        resposta
    )

    st.session_state["correcao"] = {
        "questao_id": question["questao_id"],
        "resposta": resposta,
        "resultado": resultado
    }

# ===============================
# Exibe resultado
# ===============================

correcao = st.session_state.get("correcao")

if correcao:

    resultado = correcao["resultado"]

    st.divider()

    st.metric(
        "Nota sugerida",
        resultado["nota"]
    )

    st.metric(
        "Confiança",
        f"{resultado['confianca']*100:.1f}%"
    )

    st.write(resultado["justificativa"])
    
    st.write(resultado["justificativa"])

    # ===========================
    # Correção manual
    # ===========================

    if resultado["confianca"] < 0.90:

        st.warning(
            "Baixa confiança. Recomenda-se revisão manual."
        )

        nota = st.number_input(
            "Nota do professor",
            min_value=0.0,
            max_value=10.0,
            value=float(resultado["nota"]),
            step=0.5
        )

        feedback = st.text_area(
            "Feedback do professor"
        )

        if st.button("Salvar Correção Manual"):

            correction_service.save_manual_correction(

                correcao["questao_id"],

                correcao["resposta"],

                nota,

                feedback

            )

            st.success("Correção salva com sucesso!")

            del st.session_state["correcao"]

    # ===========================
    # Aceitar automática
    # ===========================

    else:

        if st.button("Aceitar Correção"):

            correction_service.save_automatic_correction(

                correcao["questao_id"],

                correcao["resposta"],

                resultado

            )

            st.success("Correção salva com sucesso!")

            del st.session_state["correcao"]