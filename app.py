import streamlit as st
import pandas as pd
from datetime import datetime

# JEDYNA STAŁA – idealnie pasuje do Twoich dwóch przykładów
CONSTANT_OWATA = 8888.89
CONSTANT_FORMATKI = 13140.56

st.title("Kalkulator Gramatur Bematic")

tab1, tab2 = st.tabs(["Owata", "Formatki"])

# =================================== OWATA ===================================
with tab1:
    st.header("Kalkulator dla Owaty")

    col1, col2 = st.columns(2)
    with col1:
        speed = st.number_input("Prędkość maszyny (%) (Bematic)", min_value=0.0, value=76.0, step=1.0, format="%.0f")
    with col2:
        stretch = st.number_input("Rozciąg siatek (%)", min_value=0.0, value=150.0, step=1.0, format="%.0f")

    col3, col4 = st.columns(2)
    with col3:
        grammage = st.number_input("Gramatura (g/m²) (Owata)", min_value=0.0, value=130.0, step=1.0, format="%.0f")
    with col4:
        width_cm = st.selectbox("Szerokość (cm)", [240, 320, 360], index=0)

    # Automatyczne ułożenia (tak jak było wcześniej)
    if grammage >= 300:
        default_layers = 4.0
    elif grammage >= 170:
        default_layers = 3.0
    else:
        default_layers = 2.0

    layers = st.number_input("Ilość ułożeń (Układacz)", min_value=default_layers, step=1.0)

    if st.button("OBLICZ – OWATA", use_container_width=True, type="primary"):
        if speed <= 0 or stretch <= 0 or grammage <= 0:
            st.error("Wpisz poprawne dane!")
        else:
            result = (speed / 100) * (stretch / 100) * (grammage / layers / 1000) * CONSTANT_OWATA

            if width_cm == 320:
                result += 10
            elif width_cm == 360:
                result += 15

            st.success(f"**Wydajność: {result:.1f} kg/h**")

            if 'owata' not in st.session_state:
                st.session_state.owata = []
            st.session_state.owata.append({
                'Data i czas': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'Prędkość (%)': int(speed),
                'Rozciąg (%)': int(stretch),
                'Gramatura (g/m²)': grammage,
                'Szerokość (cm)': width_cm,
                'Ułożenia': int(layers),
                'Wydajność (kg/h)': round(result, 1)
            })

    if st.button("Pobierz historię CSV – Owata"):
        if 'owata' in st.session_state and st.session_state.owata:
            df = pd.DataFrame(st.session_state.owata)
            csv = df.to_csv(index=False).encode()
            st.download_button("Pobierz CSV", csv, "owata_historia.csv", "text/csv")
        else:
            st.info("Brak obliczeń")

# =================================== FORMATKI ===================================
with tab2:
    st.header("Kalkulator dla Formatek")

    col1, col2 = st.columns(2)
    with col1:
        speed_f = st.number_input("Prędkość maszyny (%) (Formatki)", value=60.0, step=1.0, key="sf")
    with col2:
        siatki = st.number_input("Siatki (%)", value=100.0, step=1.0, key="si")

    col3, col4 = st.columns(2)
    with col3:
        grammage_f = st.number_input("Gramatura (g/m²) (Formatki)", value=230.0, step=1.0, key="gf")
    with col4:
        layers_f = st.number_input("Ilość ułożeń (Formatki)", value=4.0, step=1.0, key="lf")

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
            'Ułożenia': int(layers_f),
            'Wydajność (kg/h)': round(result, 1)
        })

    if st.button("Pobierz historię CSV – Formatki"):
        if 'formatki' in st.session_state and st.session_state.formatki:
            df = pd.DataFrame(st.session_state.formatki)
            csv = df.to_csv(index=False).encode()
            st.download_button("Pobierz CSV", csv, "formatki_historia.csv", "text/csv")
        else:
            st.info("Brak obliczeń")
