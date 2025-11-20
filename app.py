import streamlit as st
import pandas as pd
from datetime import datetime

# Uniwersalna stała – idealnie pasuje do Twoich dwóch przykładów
CONSTANT_OWATA = 8819
CONSTANT_FORMATKI = 13140.56

st.title("Kalkulator Gramatur Bematic")

tab1, tab2 = st.tabs(["Owata", "Formatki"])

# =================================== OWATA ===================================
with tab1:
    st.header("Kalkulator dla Owaty")

    col1, col2 = st.columns(2)
    with col1:
        speed = st.number_input("Prędkość maszyny (%) (Bematic)", value=76.0, step=1.0, format="%.0f")
    with col2:
        stretch = st.number_input("Rozciąg siatek (%)", value=150.0, step=1.0, format="%.0f")

    col3, col4 = st.columns(2)
    with col3:
        grammage = st.number_input("Gramatura (g/m²) (Owata)", value=130.0, step=1.0, format="%.0f")
    with col4:
        width_cm = st.selectbox("Szerokość (cm)", [240, 320, 360], index=0)

    # Automatyczne ułożenia
    if grammage >= 300:
        default_layers = 4.0
    elif grammage >= 170:
        default_layers = 3.0
    else:
        default_layers = 2.0

    layers = st.number_input("Ilość ułożeń (Układacz)", value=default_layers, step=1.0, format="%.1f")

    if st.button("OBLICZ – OWATA", use_container_width=True, type="primary"):
        # Główne obliczenie
        result = (speed / 100) * (stretch / 100) * (grammage / layers / 1000) * CONSTANT_OWATA

        # Dodatki tylko przy szerszej szerokości
        if width_cm == 320:
            result += 10
        elif width_cm == 360:
            result += 15

        st.success(f"**Wydajność: {result:.1f} kg/h**")

        # Zapis do historii
        if 'owata' not in st.session_state:
            st.session_state.owata = []

        st.session_state.owata.append({
            'Data i czas': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'Prędkość (%)': int(speed),
            'Rozciąg (%)': int(stretch),
            'Gramatura (g/m²)': grammage,
            'Szerokość (cm)': width_cm,
            'Ułożenia': layers,
            'Wydajność (kg/h)': round(result, 1)
        })

    if st.button("Pobierz CSV – Owata"):
        if st.session_state.get('owata'):
            df = pd.DataFrame(st.session_state.owata)
            st.download_button(
                label="Pobierz plik CSV",
                data=df.to_csv(index=False).encode(),
                file_name="owata_wyniki.csv",
                mime="text/csv"
            )
        else:
            st.info("Brak wyników do zapisania")

# =================================== FORMATKI ===================================
with tab2:
    st.header("Kalkulator dla Formatek")

    col1, col2 = st.columns(2)
    with col1:
        speed_f = st.number_input("Prędkość maszyny (%) (Formatki)", value=60.0, step=1.0, key="speed_f")
    with col2:
        siatki = st.number_input("Siatki (%)", value=100.0, step=1.0, key="siatki")

    col3, col4 = st.columns(2)
    with col3:
        grammage_f = st.number_input("Gramatura (g/m²) (Formatki)", value=230.0, step=1.0, key="gram_f")
    with col4:
        layers_f = st.number_input("Ilość ułożeń (Formatki)", value=4.0, step=1.0, key="layers_f")

    if st.button("OBLICZ – FORMATKI", use_container_width=True, type="primary"):
        result = (speed_f / 100) * (siatki / 100) * (grammage_f / layers_f / 1000) * CONSTANT_FORMATKI
        st.success(f"**Wydajność: {result:.1f} kg/h**")

        if 'formatki' not in st.session_state:
            st.session_state.formatki = []

        st.session_state.formatki.append({
            'Data i czas': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'Prędkość (%)': int(speed_f),
            'Siatki (%)': int(siatki),
            'Gramatura (g/m²)': grammage_f,
            'Ułożenia': layers_f,
            'Wydajność (kg/h)': round(result, 1)
        })

    if st.button("Pobierz CSV – Formatki"):
        if st.session_state.get('formatki'):
            df = pd.DataFrame(st.session_state.formatki)
            st.download_button(
                label="Pobierz plik CSV",
                data=df.to_csv(index=False).encode(),
                file_name="formatki_wyniki.csv",
                mime="text/csv"
            )
        else:
            st.info("Brak wyników do zapisania")
