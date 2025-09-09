import streamlit as st
import pandas as pd
from datetime import datetime

# Stałe z wzoru
CONSTANT_OWATA_DEFAULT = 11697.80  # Dla innych gramatur
CONSTANT_OWATA_200 = 12246.68     # Dla gramatury 200 g/m²
CONSTANT_FORMATKI = 13140.56

# Funkcja do obliczania stałej dla Owaty
def get_owata_constant(grammage):
    return CONSTANT_OWATA_200 if abs(grammage - 200) < 0.1 else CONSTANT_OWATA_DEFAULT

# Tytuł aplikacji
st.title("Kalkulator Gramatur Bematic")

# Karty
tab1, tab2 = st.tabs(["Owata", "Formatki"])

# Karta Owata
with tab1:
    st.header("Kalkulator dla Owaty")
    speed_owata = st.number_input("Prędkość maszyny (%) (Bematic)", min_value=0.0, value=64.0, step=0.1, key="speed_owata")
    stretch = st.number_input("Rozciąg siatek (%)", min_value=0.0, value=162.0, step=0.1, key="stretch")
    grammage_owata = st.number_input("Gramatura (g/m²) (Owata)", min_value=0.0, value=120.0, step=0.1, key="grammage_owata")
    width_owata = st.selectbox("Szerokość (cm)", [240, 320], index=0, key="width_owata")

    # Automatyczne ustawianie ilości ułożeń dla Owaty
    if grammage_owata >= 300:
        default_layers_owata = 3.75
    elif grammage_owata >= 170:
        default_layers_owata = 3.0
    else:
        default_layers_owata = 2.0

    layers_owata = st.number_input("Ilość ułożeń (Układacz)", min_value=0.0, value=default_layers_owata, step=0.1, key="layers_owata")

    if st.button("Oblicz", key="calculate_owata"):
        if speed_owata <= 0 or stretch <= 0 or grammage_owata <= 0 or layers_owata <= 0:
            st.error("Wpisz poprawne dane (większe od 0)!")
        elif speed_owata > 100:
            st.warning("Uwaga: Prędkość powyżej 100% może być nieprawidłowa!")
        else:
            effective_grammage = grammage_owata / layers_owata
            constant = get_owata_constant(grammage_owata)
            result = (speed_owata / 100) * (stretch / 100) * (effective_grammage / 1000) * constant
            # Dodaj 10 kg/h dla szerokości 320 cm
            if width_owata == 320:
                result += 10.0
            st.success(f"Wydajność: {result:.1f} kg/h")
            
            if 'results_owata' not in st.session_state:
                st.session_state.results_owata = []
            st.session_state.results_owata.append({
                'Data i czas': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'Prędkość (%)': speed_owata,
                'Rozciąg (%)': stretch,
                'Gramatura (g/m²)': grammage_owata,
                'Szerokość (cm)': width_owata,
                'Ilość ułożeń': layers_owata,
                'Wydajność (kg/h)': result
            })

    if st.button("Zapisz wyniki do CSV (
