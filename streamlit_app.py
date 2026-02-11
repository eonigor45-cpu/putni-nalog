import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Putni Nalog - Više Vozača", layout="wide")

st.title("🚐 Evidencija korištenja vozila")

# --- LOGIN DIO ---
if 'vozac' not in st.session_state:
    st.session_state['vozac'] = None

if st.session_state['vozac'] is None:
    with st.container():
        st.subheader("Prijavite se")
        ime = st.text_input("Unesite vaše ime (bez kvačica, npr. Marko):").strip().capitalize()
        if st.button("Uđi u nalog"):
            if ime:
                st.session_state['vozac'] = ime
                st.rerun()
            else:
                st.error("Morate unijeti ime.")
    st.stop()

# Ako je vozač prijavljen, nastavlja se ovdje
trenutni_vozac = st.session_state['vozac']
DB_FILE = f"podaci_{trenutni_vozac}.csv"
KOLONE = ['Datum (1)', 'Početno (2)', 'Krajnje (3)', 'Relacija (4)', 'Polazak (5)', 'Dolazak (6)', 'Pređeno (11)']

st.sidebar.info(f"Prijavljeni vozač: **{trenutni_vozac}**")
if st.sidebar.button("Odjavi se"):
    st.session_state['vozac'] = None
    st.rerun()

# Učitavanje podataka za specifičnog vozača
if os.path.exists(DB_FILE):
    try:
        df = pd.read_csv(DB_FILE)
        if list(df.columns) != KOLONE:
            df = pd.DataFrame(columns=KOLONE)
    except:
        df = pd.DataFrame(columns=KOLONE)
else:
    df = pd.DataFrame(columns=KOLONE)

# --- BOČNA TRAKA ZA UNOS ---
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
    if st.button("Obriši zadnji unos"):
        if not df.empty:
            df = df.drop(df.index[-1])
            df.to_csv(DB_FILE, index=False)
            st.rerun()
    
    if st.button("🗑️ OBRIŠI MOJ NALOG (Reset)"):
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
            st.rerun()

# --- GLAVNI EKRAN ---
st.subheader(f"Pregled naloga za: {trenutni_vozac}")
if not df.empty:
    st.dataframe(df, use_container_width=True)
    ukupno = pd.to_numeric(df['Pređeno (11)']).sum()
    st.metric(f"UKUPNO PREĐENO ({trenutni_vozac})", f"{ukupno} km")
    
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(f"Preuzmi nalog ({trenutni_vozac})", csv, f"nalog_{trenutni_vozac}.csv", "text/csv")
else:
    st.write("Vaša tabela je prazna.")
