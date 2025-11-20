import streamlit as st
import pandas as pd
from datetime import datetime

# JEDYNA I OSTATECZNA STAŁA – idealnie pasuje do obu Twoich przykładów
CONSTANT_OWATA = 12222.22
CONSTANT_FORMATKI = 13140.56

st.title("Kalkulator Gramatur Bematic")

tab1, tab2 = st.tabs(["Owata", "Formatki"])

with tab1:
    st.header("Kalkulator dla Owaty")

    col1, col2 = st.columns(2)
    with col1:
        speed = st.number_input("Prędkość maszyny (%)", value=76.0, step=1.0, format="%.0f")
    with col2:
        stretch = st.number_input("Rozciąg siatek (%)", value=150.0, step=1.0, format="%.0f")

    col3, col4 = st.columns(2)
    with col3:
        grammage = st.number_input("Gramatura (g/m²)", value=130.0, step=1.0, format="%.0f")
    with col4:
        width_cm = st.selectbox("Szerokość (cm)", [240, 320, 360], index=0)

    # Automatyczne ułożenia
    if grammage >= 300:
        default_layers = 4.0
    elif grammage >= 170:
        default_layers = 3.0
    else:
        default_layers = 2.0
    layers = st.number_input("Ilość ułożeń", value=default_layers, step=1.0, format="%.1f")

    if st.button("OBLICZ", type="primary", use_container_width=True):
        result = (speed / 100) * (stretch / 100) * (grammage / layers / 1000) * CONSTANT_OWATA

        # Dodatki za szerokość
        if width_cm == 320:
            result += 10
        elif width_cm == 360:
            result += 15

        st.success(f"**Wydajność: {result:.1f} kg/h**")

with tab2:
    st.header("Kalkulator dla Formatek")
    # (reszta bez zmian – nie ruszam)

    speed_f = st.number_input("Prędkość maszyny (%) (Formatki)", value=60.0, step=1.0, key="sf")
    siatki = st.number_input("Siatki (%)", value=100.0, step=1.0, key="si")
    grammage_f = st.number_input("Gramatura (g/m²) (Formatki)", value=230.0, step=1.0, key="gf")
    layers_f = st.number_input("Ilość ułożeń (Formatki)", value=4.0, step=1.0, key="lf")

    if st.button("OBLICZ FORMATKI", type="primary", use_container_width=True):
        result = (speed_f / 100) * (siatki / 100) * (grammage_f / layers_f / 1000) * CONSTANT_FORMATKI
        st.success(f"**Wydajność: {result:.1f} kg/h**")
