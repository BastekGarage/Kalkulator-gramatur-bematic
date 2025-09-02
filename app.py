import streamlit as st
import pandas as pd
from datetime import datetime

# Stałe z wzoru
CONSTANT = 11697.80

# Tytuł aplikacji
st.title("Kalkulator Wydajności Maszyny")

# Pola wejściowe
speed = st.number_input("Prędkość maszyny (%)", min_value=0.0, value=64.0, step=0.1)
stretch = st.number_input("Rozciąg siatek (%)", min_value=0.0, value=162.0, step=0.1)
grammage = st.number_input("Gramatura (g/m²)", min_value=0.0, value=120.0, step=0.1)

# Automatyczne ustawianie ilości ułożeń
if grammage >= 300:
    default_layers = 3.75
elif grammage >= 170:
    default_layers = 3.0
else:
    default_layers = 2.0

# Pole dla ilości ułożeń
layers = st.number_input("Ilość ułożeń", min_value=0.0, value=default_layers, step=0.1)

# Przycisk Oblicz
if st.button("Oblicz"):
    # Walidacja
    if speed <= 0 or stretch <= 0 or grammage <= 0 or layers <= 0:
        st.error("Wpisz poprawne dane (większe od 0)!")
    elif speed > 100:
        st.warning("Uwaga: Prędkość powyżej 100% może być nieprawidłowa!")
    else:
        # Oblicz efektywną gramaturę
        effective_grammage = grammage / layers
        # Oblicz wynik
        result = (speed / 100) * (stretch / 100) * (effective_grammage / 1000) * CONSTANT
        # Wyświetl wyniki
        st.success(f"Efektywna gramatura: {effective_grammage:.2f} g/m²")
        st.success(f"Wydajność: {result:.1f} kg/h")
        
        # Zapisz wynik do sesji
        if 'results' not in st.session_state:
            st.session_state.results = []
        st.session_state.results.append({
            'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Prędkość (%)': speed,
            'Rozciąg (%)': stretch,
            'Gramatura (g/m²)': grammage,
            'Ilość ułożeń': layers,
            'Efektywna gramatura (g/m²)': effective_grammage,
            'Wydajność (kg/h)': result
        })

# Przycisk Zapisz wyniki
if st.button("Zapisz wyniki do CSV"):
    if 'results' not in st.session_state or not st.session_state.results:
        st.error("Brak wyników do zapisania!")
    else:
        df = pd.DataFrame(st.session_state.results)
        filename = f"kalkulator_wyniki_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(filename, index=False)
        st.success(f"Wyniki zapisano do: {filename}")
        # Pobieranie pliku
        with open(filename, "rb") as file:
            st.download_button(
                label="Pobierz plik CSV",
                data=file,
                file_name=filename,
                mime="text/csv"
            )
