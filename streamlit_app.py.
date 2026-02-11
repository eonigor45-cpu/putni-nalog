import streamlit as st
import pandas as pd

st.title("Moja Evidencija Vožnje")

# Jednostavna baza koja se čuva u fajlu
try:
    df = pd.read_csv("podaci.csv")
except:
    df = pd.DataFrame(columns=['Datum', 'Pocetna', 'Zavrsna', 'Razlika', 'Relacija'])

with st.form("forma"):
    d = st.text_input("Datum (npr. 06.11)")
    p = st.number_input("Početna KM", value=0)
    z = st.number_input("Završna KM", value=0)
    r = st.text_input("Relacija")
    if st.form_submit_button("Spremi"):
        novi = pd.DataFrame([[d, p, z, z-p, r]], columns=df.columns)
        df = pd.concat([df, novi], ignore_index=True)
        df.to_csv("podaci.csv", index=False)
        st.success("Spremljeno!")

st.table(df)
