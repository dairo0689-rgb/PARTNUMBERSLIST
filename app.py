import streamlit as st
import pandas as pd
import numpy as np

# Configuración de página
st.set_page_config(page_title="Gestión de Part Numbers", layout="wide")

# --- BLOQUE DE DISEÑO PERSONALIZADO (CSS) ---
st.markdown("""
    <style>
    [data-testid="stHeader"] {
        background-color: #3392b5 !important;
    }
    
    th {
        background-color: #1f4e79 !important; 
        color: white !important; 
        font-weight: 900 !important; 
        font-size: 14px !important;
        text-transform: uppercase;
    }

    .stDataFrame {
        border: 2px solid #1f4e79;
        border-radius: 10px;
    }
    
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: transparent;
        color: #1f4e79;
        text-align: center;
        padding: 10px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📦 Gestión de Part Numbers")

# --- FUNCIÓN DE LIMPIEZA AGRESIVA ---
def forzar_numero_completo(valor):
    if pd.isna(valor) or str(valor).strip() in ["", "nan", "NaN", "None"]:
        return ""
    
    try:
        # 1. Limpiar el string: quitar espacios y normalizar comas a puntos
        val_limpio = str(valor).strip().replace(',', '.')
        
        # 2. Convertir a float para procesar la notación científica (ej. 2.98E+12)
        numero_float = float(val_limpio)
        
        # 3. Convertir a string con 0 decimales (formato entero largo)
        resultado = "{:.0f}".format(numero_float)
        return resultado
    except:
        # Si falla (ej. es texto real), devolver el valor original sin espacios
        return str(valor).strip()

try:
    # 1. Leer el archivo (dtype=str para que no procese nada automáticamente)
    df = pd.read_csv("PN_APP.csv", sep=None, engine='python', encoding='latin1', dtype=str)

    # 2. APLICAR LIMPIEZA A TODO EL DATAFRAME
    # Esto busca cualquier columna que contenga números con "E+" y los expande
    for col in df.columns:
        df[col] = df[col].apply(forzar_numero_completo)

    # Limpieza de columnas fantasmas de Excel
    df = df.dropna(axis=1, how='all')
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # 3. INTERFAZ: Buscador
    busqueda = st.text_input("🔍 Buscar por nombre o número de parte:", placeholder="Ej: Wire o 298029...")

    if busqueda:
        mask = df.apply(lambda row: row.astype(str).str.contains(busqueda, case=False).any(), axis=1)
        df_filtrado = df[mask]
    else:
        df_filtrado = df

    # 4. MOSTRAR TABLA
    st.write(f"Mostrando **{len(df_filtrado)}** registros:")
    
    # Configuración de columnas para evitar que Streamlit las reconvierta a números
    config_columnas = {col: st.column_config.TextColumn(col) for col in df.columns}

    st.dataframe(
        df_filtrado.fillna(""), 
        use_container_width=True, 
        hide_index=True,
        column_config=config_columnas
    )

except FileNotFoundError:
    st.error("Error: No se encontró 'PN_APP.csv'.")
except Exception as e:
    st.error(f"Error inesperado: {e}")

# --- CRÉDITOS ---
st.markdown('<div class="footer">Created by Dairo Romero</div>', unsafe_allow_html=True)

