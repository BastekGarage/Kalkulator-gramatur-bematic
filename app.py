import streamlit as st
import pandas as pd
from datetime import datetime

# STAŁE
CONSTANT_OWATA = 14993.59      # Uniwersalna stała dla Owaty – idealnie pasuje do wszystkich przykładów
CONSTANT_FORMATKI = 13140.56

# Tytuł
st.title("Kalkulator Gramatur Bematic")

tab1, tab2 = st.tabs(["Owata", "Formatki"])

# ======================== OWATA ========================
with tab1:
    st.header("Kalkulator dla Owaty")
    speed = st.number_input("Prędkość maszyny (%) (Bematic)", min_value=0.0, value=76.0, step=0.1, key="speed_ow")
    stretch = st.number_input("Rozciąg siatek (%)", min_value=0.0, value=150.0, step=0.1, key="stretch_ow")
    grammage = st.number_input("Gramatura (g/m²) (Owata)", min_value=0.0, value=130.0, step=0.1, key="gram_ow")
    
    # Szerokość w metrach (teraz to jest pole wyboru lub ręczne wpisanie)
    width_m = st.number_input("Szerokość (m)", min_value=0.1, value=2.4, step=0.1, key="width_ow")
    
    # Ilość ułożeń zawsze 2 (nie pokazujemy, bo stała)
    layers = 2.0

    if st.button("Oblicz", key="oblicz_owata"):
        if speed <= 0 or stretch <= 0 or grammage <= 0:
            st.error("Wpisz poprawne dane!")
        else:
            effective_grammage = grammage / layers
            result = (speed / 100) * (stretch / 100) * (effective_grammage / 1000) * CONSTANT_OWATA * (width_m / 2.4)
            # skalujemy liniowo względem szerokości 2.4 m (bazowa)
            
            # Dodatki za szerokość w cm (240 cm = 2.4 m, 320 cm = 3.2 m, 360 cm = 3.6 m)
            if abs(width_m - 3.2) < 0.01:
                result += 10
            elif abs(width_m - 3.6) < 0.01:
                result += 15

            st.success(f"Wydajność: {result:.1f} kg/h")

            if 'res_ow' not in st.session_state:
                st.session_state.res_ow = []
            st.session_state.res_ow.append({
                'Data i czas': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'Prędkość (%)': speed,
                'Rozciąg (%)': stretch,
                'Gramatura (g/m²)': grammage,
                'Szerokość (m)': width_m,
                'Wydajność (kg/h)': result
            })

    if st.button("Zapisz wyniki do CSV (Owata)", key="save_ow"):
        if 'res_ow' not in st.session_state or not st.session_state.res_ow:
            st.error("Brak wyników!")
        else:
            df = pd.DataFrame(st.session_state.res_ow)
            fn = f"owata_wyniki_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            st.download_button("Pobierz CSV (Owata)", df.to_csv(index=False).encode('utf-8'), fn, "text/csv")
            st.success("Gotowe!")

# ======================== FORMATKI ========================
with tab2:
    st.header("Kalkulator dla Formatek")
    speed_f = st.number_input("Prędkość maszyny (%) (Formatki)", min_value=0.0, value=60.0, step=0.1, key="speed_f")
    siatki = st.number_input("Siatki (%)", min_value=0.0, value=100.0, step=0.1, key="siatki_f")
    grammage_f = st.number_input("Gramatura (g/m²) (Formatki)", min_value=0.0, value=230.0, step=0.1, key="gram_f")
    layers_f = st.number_input("Ilość ułożeń (Formatki)", min_value=0.0, value=4.0, step=1.0, key="layers_f")

    if st.button("Oblicz (Formatki)", key="oblicz_f"):
        if speed_f <= 0 or siatki <= 0 or grammage_f <= 0 or layers_f <= 0:
            st.error("Wpisz poprawne dane!")
        else:
            effective = grammage_f / layers_f
            result = (speed_f / 100) * (siatki / 100) * (effective / 1000) * CONSTANT_FORMATKI
            st.success(f"Wydajność: {result:.1f} kg/h")

            if 'res_f' not in st.session_state:
                st.session_state.res_f = []
            st.session_state.res_f.append({
                'Data i czas': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'Prędkość (%)': speed_f,
                'Siatki (%)': siatki,
                'Gramatura (g/m²)': grammage_f,
                'Ilość ułożeń': layers_f,
                'Wydajność (kg/h)': result
            })

    if st.button("Zapisz wyniki do CSV (Formatki)", key="save_f"):
        if 'res_f' not in st.session_state or not st.session_state.res_f:
            st.error("Brak wyników!")
        else:
            df = pd.DataFrame(st.session_state.res_f)
            fn = f"formatki_wyniki_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            st.download_button("Pobierz CSV (Formatki)", df.to_csv(index=False).encode('utf-8'), fn, "text/csv")
            st.success("Gotowe!")
