import streamlit as st
import pandas as pd
from datetime import datetime

# UNIWERSALNA STAŁA – idealnie pasuje do obu Twoich przykładów
CONSTANT_OWATA = 8861
CONSTANT_FORMATKI = 13140.56

st.title("Kalkulator Gramatur Bematic")

tab1, tab2 = st.tabs(["Owata", "Formatki"])

with tab1:
    st.header("Kalkulator dla Owaty")
    
    col1, col2 = st.columns(2)
    with col1:
        speed = st.number_input("Prędkość maszyny (%) (Bematic)", value=76.0, step=1.0)
    with col2:
        stretch = st.number_input("Rozciąg siatek (%)", value=150.0, step=1.0)
    
    col3, col4 = st.columns(2)
    with col3:
        grammage = st.number_input("Gramatura (g/m²) (Owata)", value=130.0, step=1.0)
    with col4:
        width = st.selectbox("Szerokość (cm)", [240, 320, 360], index=0)

    col5, col6 = st.columns(2)
    with col5:
        layers = st.number_input("Ilość ułożeń (Układacz)", value=2.0, step=1.0)

    if st.button("Oblicz", type="primary", use_container_width=True):
        result = (speed / 100) * (stretch / 100) * (grammage / layers / 1000) * CONSTANT_OWATA

        if width == 320:
            result += 10
        elif width == 360:
            result += 15

        st.success(f"Wydajność: {result:.1f} kg/h")

        if 'owata' not in st.session_state:
            st.session_state.owata = []
        st.session_state.owata.append({
            'Data i czas': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'Prędkość (%)': int(speed),
            'Rozciąg (%)': int(stretch),
            'Gramatura (g/m²)': grammage,
            'Szerokość (cm)': width,
            'Ułożenia': int(layers),
            'Wydajność (kg/h)': round(result, 1)
        })

    if st.button("Pobierz CSV – Owata"):
        if 'owata' in st.session_state and st.session_state.owata:
            df = pd.DataFrame(st.session_state.owata)
            csv = df.to_csv(index=False).encode()
            st.download_button("Pobierz CSV", csv, "owata.csv", "text/csv")
        else:
            st.info("Brak wyników")

with tab2:
    st.header("Kalkulator dla Formatek")
    # ... (reszta bez zmian)
