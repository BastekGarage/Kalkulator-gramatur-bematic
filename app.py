import streamlit as st
import pandas as pd
from datetime import datetime

# STAŁE
CONSTANT_OWATA = 14993.59      # idealnie pasuje do wszystkich przykładów Owaty
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
        grammage = st.number_input("Gramatura (g/m²)", min_value=0.0, value=130.0, step=1.0, format="%.0f")
    with col4:
        width_m = st.number_input("Szerokość robocza (m)", min_value=1.0, max_value=5.0, value=2.4, step=0.4, format="%.1f")

    col5, col6 = st.columns(2)
    with col5:
        layers = st.number_input("Ilość ułożeń (Układacz)", min_value=1.0, value=2.0, step=1.0, format="%.0f")

    if st.button("OBLICZ – OWATA", use_container_width=True, type="primary"):
        if speed <= 0 or stretch <= 0 or grammage <= 0 or layers <= 0:
            st.error("Wpisz poprawne dane!")
        else:
            effective = grammage / layers
            result = (speed / 100) * (stretch / 100) * (effective / 1000) * CONSTANT_OWATA * (width_m / 2.4)

            # Dopłaty za szerszą szerokość
            if round(width_m, 1) == 3.2:
                result += 10
            elif round(width_m, 1) == 3.6:
                result += 15

            st.success(f"**Wydajność: {result:.1f} kg/h**")
            st.caption(f"Gramatura {grammage} g/m² | Szerokość {width_m} m | Ułożenia {int(layers)}")

            if 'owata' not in st.session_state:
                st.session_state.owata = []
            st.session_state.owata.append({
                'Data i czas': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'Prędkość (%)': int(speed),
                'Rozciąg (%)': int(stretch),
                'Gramatura (g/m²)': int(grammage),
                'Szerokość (m)': width_m,
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
        speed_f = st.number_input("Prędkość maszyny (%) (Formatki)", min_value=0.0, value=60.0, step=1.0, format="%.0f", key="sf")
    with col2:
        siatki = st.number_input("Siatki (%)", min_value=0.0, value=100.0, step=1.0, format="%.0f", key="si")

    col3, col4 = st.columns(2)
    with col3:
        grammage_f = st.number_input("Gramatura (g/m²) (Formatki)", min_value=0.0, value=230.0, step=1.0, format="%.0f", key="gf")
    with col4:
        layers_f = st.number_input("Ilość ułożeń (Formatki)", min_value=1.0, value=4.0, step=1.0, format="%.0f", key="lf")

    if st.button("OBLICZ – FORMATKI", use_container_width=True, type="primary"):
        if speed_f <= 0 or siatki <= 0 or grammage_f <= 0 or layers_f <= 0:
            st.error("Wpisz poprawne dane!")
        else:
            effective = grammage_f / layers_f
            result = (speed_f / 100) * (siatki / 100) * (effective / 1000) * CONSTANT_FORMATKI
            st.success(f"**Wydajność: {result:.1f} kg/h**")

            if 'formatki' not in st.session_state:
                st.session_state.formatki = []
            st.session_state.formatki.append({
                'Data i czas': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'Prędkość (%)': int(speed_f),
                'Siatki (%)': int(siatki),
                'Gramatura (g/m²)': int(grammage_f),
                'Ilość ułożeń': int(layers_f),
                'Wydajność (kg/h)': round(result, 1)
            })

    if st.button("Pobierz historię CSV – Formatki"):
        if 'formatki' in st.session_state and st.session_state.formatki:
            df = pd.DataFrame(st.session_state.formatki)
            csv = df.to_csv(index=False).encode()
            st.download_button("Pobierz CSV", csv, "formatki_historia.csv", "text/csv")
        else:
            st.info("Brak obliczeń")
