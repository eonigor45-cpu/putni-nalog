import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Putni Nalog", layout="wide")

# Naslov aplikacije
st.title("🚐 Evidencija korištenja vozila")

# Putanja do datoteke za čuvanje podataka
DB_FILE = "podaci.csv"

# Učitavanje podataka
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
else:
    df = pd.DataFrame(columns=['Datum', 'Početno (2)', 'Krajnje (3)', 'Pređeno (11)', 'Relacija (4)', 'Polazak (5)', 'Dolazak (6)'])

# --- BOČNA TRAKA ZA UNOS ---
with st.sidebar:
    st.header("Novi unos u nalog")
    with st.form("forma", clear_on_submit=True):
        datum = st.text_input("Datum (1)")
        pocetna = st.number_input("Stanje brojila: Početno (2)", value=0)
        krajnja = st.number_input("Stanje brojila: Krajnje (3)", value=0)
        relacija = st.text_input("Relacija kretanja (4)")
        polazak = st.text_input("Vrijeme: Polaska (5)")
        dolazak = st.text_input("Vrijeme: Dolaska (6)")
        
        submitted = st.form_submit_button("Spremi u nalog")
        
        if submitted:
            razlika = krajnja - pocetna
            novi_red = pd.DataFrame([[datum, pocetna, krajnja, razlika, relacija, polazak, dolazak]], columns=df.columns)
            df = pd.concat([df, novi_red], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.success("Podaci su spremljeni!")
            st.rerun()

    st.divider()
    # Dugme za brisanje zadnjeg reda
    if st.button("Obriši zadnji unos"):
        if not df.empty:
            df = df.drop(df.index[-1])
            df.to_csv(DB_FILE, index=False)
            st.warning("Zadnji unos je obrisan.")
            st.rerun()

# --- GLAVNI EKRAN ---
st.subheader("Pregled naloga (Tabela)")
st.dataframe(df, use_container_width=True)

# Statistika na dnu
if not df.empty:
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        ukupno_km = df['Pređeno (11)'].sum()
        st.metric("UKUPNO PREĐENO", f"{ukupno_km} km")
    with col2:
        broj_voznji = len(df)
        st.metric("BROJ UPISANIH VOŽNJI", broj_voznji)

# Opcija za preuzimanje (ako zatreba za ispis)
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Preuzmi tabelu za Excel", csv, "putni_nalog.csv", "text/csv")
