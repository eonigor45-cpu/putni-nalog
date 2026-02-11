import streamlit as st
import pandas as pd
import os

# Postavke stranice
st.set_page_config(page_title="Putni Nalog", layout="wide")

st.title("🚐 Evidencija korištenja vozila")

DB_FILE = "podaci.csv"

# Definisanje kolona tačno prema tvom papiru
KOLONE = [
    'Datum (1)', 
    'Početno (2)', 
    'Krajnje (3)', 
    'Relacija (4)', 
    'Polazak (5)', 
    'Dolazak (6)', 
    'Pređeno (11)'
]

# Učitavanje ili kreiranje nove tabele
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
else:
    df = pd.DataFrame(columns=KOLONE)

# --- BOČNA TRAKA ZA UNOS ---
with st.sidebar:
    st.header("Novi unos")
    with st.form("forma", clear_on_submit=True):
        d = st.text_input("Datum (1)")
        p = st.number_input("Stanje: Početno (2)", min_value=0, value=0)
        k = st.number_input("Stanje: Krajnje (3)", min_value=0, value=0)
        rel = st.text_input("Relacija (4)")
        pol = st.text_input("Vrijeme: Polazak (5)")
        dol = st.text_input("Vrijeme: Dolazak (6)")
        
        if st.form_submit_button("Spremi u nalog"):
            razlika = k - p
            # Redoslijed mora pratiti listu KOLONE
            novi_red = pd.DataFrame([[d, p, k, rel, pol, dol, razlika]], columns=KOLONE)
            df = pd.concat([df, novi_red], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.success("Spremljeno!")
            st.rerun()

    st.divider()
    if st.button("Obriši zadnji unos"):
        if not df.empty:
            df = df.drop(df.index[-1])
            df.to_csv(DB_FILE, index=False)
            st.warning("Obrisano.")
            st.rerun()

# --- GLAVNI EKRAN ---
st.subheader("Pregled putnih naloga")
st.dataframe(df, use_container_width=True)

# Sabiranje kilometara
if not df.empty:
    ukupno = df['Pređeno (11)'].sum()
    st.metric("UKUPNO PREĐENO KILOMETARA", f"{ukupno} km")

# Dugme za export
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Preuzmi kao Excel/CSV", csv, "moj_nalog.csv", "text/csv")
