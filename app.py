import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

st.set_page_config(page_title="No Programados", page_icon="📊", layout="wide")
st.title("📊 Dashboard Personal No Programado")
st.markdown("---")

@st.cache_data
def cargar_archivo(uploaded_file):
    if uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file, engine='openpyxl')
    else:
        df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip().str.upper().str.replace(' ', '_')
    return df


def convertir_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Datos')
    output.seek(0)
    return output

uploaded_file = st.file_uploader('Seleccione archivo Excel', type=['xls','xlsx'])
if uploaded_file is None:
    st.info('Cargue un archivo para comenzar.')
    st.stop()

df = cargar_archivo(uploaded_file)

for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].astype(str).str.strip()

st.sidebar.header('Filtros')
if 'REGIONAL' in df.columns:
    regional = st.sidebar.multiselect('Regional', sorted(df['REGIONAL'].dropna().unique()))
    if regional:
        df = df[df['REGIONAL'].isin(regional)]

if 'CLIENTE' in df.columns:
    cliente = st.sidebar.multiselect('Cliente', sorted(df['CLIENTE'].dropna().unique()))
    if cliente:
        df = df[df['CLIENTE'].isin(cliente)]

c1,c2,c3 = st.columns(3)
c1.metric('Registros', len(df))
c2.metric('Regionales', df['REGIONAL'].nunique() if 'REGIONAL' in df.columns else 0)
c3.metric('Clientes', df['CLIENTE'].nunique() if 'CLIENTE' in df.columns else 0)

if 'REGIONAL' in df.columns:
    regionales = df['REGIONAL'].value_counts().reset_index()
    regionales.columns=['Regional','Cantidad']
    fig = px.bar(regionales, x='Cantidad', y='Regional', orientation='h')
    st.plotly_chart(fig, use_container_width=True)

st.dataframe(df, use_container_width=True)

excel_file = convertir_excel(df)
st.download_button('Descargar Excel', excel_file, 'no_programados_filtrado.xlsx')
