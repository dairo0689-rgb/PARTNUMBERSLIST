import streamlit as st
import pandas as pd

# Configuración de la página con un toque más profesional
st.set_page_config(page_title="Gestión de Part Numbers", layout="wide")

# Estilo personalizado para mejorar la interfaz
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stDataFrame { border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("📦 Visor de Inventario: Part Numbers")

try:
    # 1. Leer el archivo
    df = pd.read_csv("PN_APP.csv", sep=None, engine='python', encoding='latin1')

    # 2. LIMPIEZA: Eliminar columnas completamente vacías (None) o con "Unnamed"
    df = df.dropna(axis=1, how='all') # Elimina columnas vacías
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')] # Elimina las columnas "Unnamed"

    # 3. INTERFAZ: Buscador y Filtros
    st.subheader("Búsqueda Rápida")
    busqueda = st.text_input("🔍 Escribe el nombre o número de parte para filtrar:", placeholder="Ej: ACTUATOR")

    if busqueda:
        # Filtra en todas las columnas sin importar mayúsculas/minúsculas
        mask = df.apply(lambda row: row.astype(str).str.contains(busqueda, case=False).any(), axis=1)
        df = df[mask]

    # 4. MOSTRAR TABLA: Con diseño interactivo
    st.write(f"Mostrando **{len(df)}** registros encontrados:")
    st.dataframe(df, use_container_width=True, hide_index=True)

    # 5. BOTÓN DE DESCARGA (Opcional pero útil)
    csv = df.to_csv(index=False).encode('latin1')
    st.download_button(label="📥 Descargar esta vista como CSV", data=csv, file_name='part_numbers_filtrado.csv', mime='text/csv')

except Exception as e:
    st.error(f"Error al procesar los datos: {e}")
