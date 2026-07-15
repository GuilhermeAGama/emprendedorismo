import streamlit as st

from services.QuestionService import QuestionService
from repositories.QuestionRepository import QuestionRepository


repository = QuestionRepository()
service = QuestionService(repository)

st.title("Cadastro de Questões")

disciplina = st.text_input("ID da Disciplina")

enunciado = st.text_area(
    "Enunciado"
)

resposta_modelo = st.text_area(
    "Resposta modelo"
)

nota_maxima = st.number_input(
    "Nota máxima",
    min_value=0,
    value=10
)

if st.button("Salvar"):

    service.create_question(

        disciplina,

        enunciado,

        resposta_modelo,

        nota_maxima

    )

    st.success("Questão cadastrada!")
    
st.divider()

st.subheader("Questões cadastradas")

questoes = service.list_questions()

st.dataframe(questoes)