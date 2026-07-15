import streamlit as st

from repositories.CorrectionRepository import CorrectionRepository

repo = CorrectionRepository()

st.title("Histórico")

st.dataframe(
    repo.get_all()
)