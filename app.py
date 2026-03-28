import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Gestión de Part Numbers", layout="wide")

# --- BLOQUE DE DISEÑO PERSONALIZADO ---
st.markdown("""
    <style>
    /* Cambia el color de fondo de la cabecera de la tabla */
    thead tr th {
        background-color: #004280 !important; /* Azul oscuro empresarial */
        color: white !important;               /* Texto blanco */
        font-weight: bold !important;          /* Negrilla */
        text-transform: uppercase;             /* Mayúsculas */
    }
    
    /* Cambia el color de fondo de toda la app */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Estilo para el título principal */
    .titulo-custom {
        color: #004280;
        text-align: center;
        padding: 20px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="titulo-custom">📦 Visor de Inventario: Part Numbers</h1>', unsafe_allow_html=True)

try:
    # 1. Leer el archivo
    df = pd.read_csv("PN_APP.csv", sep=None, engine='python', encoding='latin1')

    # 2. LIMPIEZA PROFUNDA (Mantenemos lo anterior)
    df = df.replace(['None', 'none', 'nan', '', ' '], np.nan)
    df = df.dropna(axis=1, how='all')
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # 3. INTERFAZ: Buscador
    busqueda = st.text_input("🔍 Buscar por nombre o número de parte:", placeholder="Ej: CABLE")

    if busqueda:
        mask = df.apply(lambda row: row.astype(str).str.contains(busqueda, case=False).any(), axis=1)
        df = df[mask]

    # 4. MOSTRAR TABLA
    st.write(f"Mostrando **{len(df)}** registros:")
    
    # Usamos st.table para que el CSS de la cabecera se aplique más fácilmente
    # O mantenemos st.dataframe si prefieres que sea desplazable
    st.dataframe(df.fillna(""), use_container_width=True, hide_index=True)

except Exception as e:
    st.error(f"Error: {e}")


