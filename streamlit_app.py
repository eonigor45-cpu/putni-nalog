import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Putni Nalog", layout="wide")
st.title("🚐 Evidencija korištenja vozila")

DB_FILE = "podaci.csv"
# Tačne kolone prema tvom papiru
KOLONE = ['Datum (1)', 'Početno (2)', 'Krajnje (3)', 'Relacija (4)', 'Polazak (5)', 'Dolazak (6)', 'Pređeno (11)']

# PAMETNO UČITAVANJE: Ako stara tabela ne valja, pravi se nova automatski
if os.path.exists(DB_FILE):
    try:
        df = pd.read_csv(DB_FILE)
        # Ako fale nove kolone (poput Polazak), resetuj tabelu da ne puca
        if 'Polazak (5)' not in df.columns or 'Pređeno (11)' not in df.columns:
            df = pd.DataFrame(columns=KOLONE)
    except:
        df = pd.DataFrame(columns=KOLONE)
else:
    df = pd.DataFrame(columns=KOLONE)

with st.sidebar:
    st.header("Novi unos")
    with st.form("forma", clear_on_submit=True):
        d = st.text_input("Datum (1)")
        p = st.number_input("Početno (2)", value=0)
        k = st.number_input("Krajnje (3)", value=0)
        rel = st.text_input("Relacija (4)")
        pol = st.text_input("Polazak (5)")
        dol = st.text_input("Dolazak (6)")
        
        if st.form_submit_button("Spremi"):
            razlika = k - p
            novi_red = pd.DataFrame([[d, p, k, rel, pol, dol, razlika]], columns=KOLONE)
            df = pd.concat([df, novi_red], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.rerun()

    st.divider()
    # DUGME ZA HITNI RESET - Ako se ikad pojavi crveno, klikni ovo
    if st.button("🗑️ OBRIŠI SVE I POPRAVI"):
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
        st.rerun()

st.subheader("Pregled naloga")
# Prikazujemo tabelu samo ako ima kolone koje nam trebaju
if not df.empty and 'Pređeno (11)' in df.columns:
    st.dataframe(df, use_container_width=True)
    ukupno = pd.to_numeric(df['Pređeno (11)']).sum()
    st.metric("UKUPNO PREĐENO", f"{ukupno} km")
else:
    st.write("Tabela je trenutno prazna. Unesite prve podatke sa strane.")
    st.dataframe(pd.DataFrame(columns=KOLONE), use_container_width=True)
