import streamlit as st
import pandas as pd
from datetime import datetime

# Stałe z wzoru
CONSTANT_SIATKI = 11697.80
CONSTANT_FORMATKI = 13140.56

# Tytuł aplikacji
st.title("Kalkulator Gramatur")

# Karty
tab1, tab2 = st.tabs(["Siatki", "Formatki"])

# Karta Siatki
with tab1:
    st.header("Kalkulator dla owaty")
    speed_siatki = st.number_input("Prędkość maszyny (%) (Siatki)", min_value=0.0, value=64.0, step=0.1, key="speed_siatki")
    stretch = st.number_input("Rozciąg siatek (%)", min_value=0.0, value=162.0, step=0.1, key="stretch")
    grammage_siatki = st.number_input("Gramatura (g/m²) (Siatki)", min_value=0.0, value=120.0, step=0.1, key="grammage_siatki")

    # Automatyczne ustawianie ilości ułożeń dla siatki
    if grammage_siatki >= 300:
        default_layers_siatki = 3.75
    elif grammage_siatki >= 170:
        default_layers_siatki = 3.0
    else:
        default_layers_siatki = 2.0

    layers_siatki = st.number_input("Ilość ułożeń (Siatki)", min_value=0.0, value=default_layers_siatki, step=0.1, key="layers_siatki")

    if st.button("Oblicz (Siatki)", key="calculate_siatki"):
        if speed_siatki <= 0 or stretch <= 0 or grammage_siatki <= 0 or layers_siatki <= 0:
            st.error("Wpisz poprawne dane (większe od 0)!")
        elif speed_siatki > 100:
            st.warning("Uwaga: Prędkość powyżej 100% może być nieprawidłowa!")
        else:
            effective_grammage = grammage_siatki / layers_siatki
            result = (speed_siatki / 100) * (stretch / 100) * (effective_grammage / 1000) * CONSTANT_SIATKI
            st.success(f"Efektywna gramatura: {effective_grammage:.2f} g/m²")
            st.success(f"Wydajność: {result:.1f} kg/h")
            
            if 'results_siatki' not in st.session_state:
                st.session_state.results_siatki = []
            st.session_state.results_siatki.append({
                'Data i czas': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'Prędkość (%)': speed_siatki,
                'Rozciąg (%)': stretch,
                'Gramatura (g/m²)': grammage_siatki,
                'Ilość ułożeń': layers_siatki,
                'Efektywna gramatura (g/m²)': effective_grammage,
                'Wydajność (kg/h)': result
            })

    if st.button("Zapisz wyniki do CSV (Siatki)", key="save_siatki"):
        if 'results_siatki' not in st.session_state or not st.session_state.results_siatki:
            st.error("Brak wyników do zapisania!")
        else:
            df = pd.DataFrame(st.session_state.results_siatki)
            filename = f"siatki_wyniki_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Pobierz plik CSV (Siatki)",
                data=csv_data,
                file_name=filename,
                mime="text/csv",
                key="download_siatki"
            )
            st.success(f"Plik {filename} gotowy do pobrania!")

# Karta Formatki
with tab2:
    st.header("Kalkulator dla Formatek")
    speed_formatki = st.number_input("Prędkość maszyny (%) (Formatki)", min_value=0.0, value=60.0, step=0.1, key="speed_formatki")
    siatki = st.number_input("Siatki (%)", min_value=0.0, value=100.0, step=0.1, key="siatki")
    grammage_formatki = st.number_input("Gramatura (g/m²) (Formatki)", min_value=0.0, value=230.0, step=0.1, key="grammage_formatki")
    layers_formatki = st.number_input("Ilość ułożeń (Formatki)", min_value=0.0, value=4.0, step=1.0, key="layers_formatki")

    if st.button("Oblicz (Formatki)", key="calculate_formatki"):
        if speed_formatki <= 0 or siatki <= 0 or grammage_formatki <= 0 or layers_formatki <= 0:
            st.error("Wpisz poprawne dane (większe od 0)!")
        elif speed_formatki > 100:
            st.warning("Uwaga: Prędkość powyżej 100% może być nieprawidłowa!")
        else:
            effective_grammage = grammage_formatki / layers_formatki
            result = (speed_formatki / 100) * (siatki / 100) * (effective_grammage / 1000) * CONSTANT_FORMATKI
            st.success(f"Efektywna gramatura: {effective_grammage:.2f} g/m²")
            st.success(f"Wydajność: {result:.1f} kg/h")
            
            if 'results_formatki' not in st.session_state:
                st.session_state.results_formatki = []
            st.session_state.results_formatki.append({
                'Data i czas': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'Prędkość (%)': speed_formatki,
                'Siatki (%)': siatki,
                'Gramatura (g/m²)': grammage_formatki,
                'Ilość ułożeń': layers_formatki,
                'Efektywna gramatura (g/m²)': effective_grammage,
                'Wydajność (kg/h)': result
            })

    if st.button("Zapisz wyniki do CSV (Formatki)", key="save_formatki"):
        if 'results_formatki' not in st.session_state or not st.session_state.results_formatki:
            st.error("Brak wyników do zapisania!")
        else:
            df = pd.DataFrame(st.session_state.results_formatki)
            filename = f"formatki_wyniki_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Pobierz plik CSV (Formatki)",
                data=csv_data,
                file_name=filename,
                mime="text/csv",
                key="download_formatki"
            )
            st.success(f"Plik {filename} gotowy do pobrania!")
