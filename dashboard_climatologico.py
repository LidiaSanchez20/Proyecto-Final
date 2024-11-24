import streamlit as st
import pandas as pd
import plotly.express as px
import pickle

# Configuración de la página
st.set_page_config(page_title="Dashboard Climatológico", layout="wide", page_icon="🌍")

# Carga del DataFrame
df = pd.read_csv("base_actualizada.csv")
df['Temperatura'] = df['Temperatura'].round(3)
df['Precipitaciones'] = df['Precipitaciones'].round(3)

# Eliminar registros con valores nulos en latitud o longitud
df = df.dropna(subset=['Latitud', 'Longitud'])

# Cargar modelos entrenados
with open('modelo_logistico_lluvia.pkl', 'rb') as file:
    modelo_lluvia = pickle.load(file)
with open('scaler_lluvia.pkl', 'rb') as file:
    scaler_lluvia = pickle.load(file)

with open('modelo_logistico_temperatura.pkl', 'rb') as file:
    modelo_temp = pickle.load(file)
with open('scaler_temp.pkl', 'rb') as file:
    scaler_temp = pickle.load(file)

# Sidebar (Menú Lateral)
st.sidebar.title("Menú")
opcion = st.sidebar.radio("Selecciona una vista:", ["Principal", "Mapa Interactivo", "Búsqueda por País", "Probabilidades"])

# Vista Principal
if opcion == "Principal":
    st.title("Dashboard climatológico")
     # Contexto del Proyecto
    st.write("""
    **Bienvenido**  
    Este proyecto tiene como objetivo analizar y predecir patrones climáticos basados en datos históricos, 
    ayudando a comprender la variabilidad climática a nivel mundial. Aquí encontrarás información sobre:  
    - Los países con mayor y menor precipitaciones y temperaturas.
    - Mapas interactivos para explorar datos geográficos.
    - Predicciones de eventos extremos como temperaturas altas y lluvias abundantes.  
    Esta herramienta puede ser útil para investigadores, agricultores y responsables de la toma de decisiones 
    en torno a los efectos del cambio climático.
    """)

    # Métricas clave
    st.subheader("Métricas Resumidas")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Máx. Precipitaciones", f"{df['Precipitaciones'].max()} mm", df.loc[df['Precipitaciones'].idxmax(), 'País'])
    col2.metric("Mín. Temperatura", f"{df['Temperatura'].min()} °C", df.loc[df['Temperatura'].idxmin(), 'País'])
    col3.metric("Mín. Precipitaciones", f"{df['Precipitaciones'].min()} mm", df.loc[df['Precipitaciones'].idxmin(), 'País'])
    col4.metric("Máx. Temperatura", f"{df['Temperatura'].max()} °C", df.loc[df['Temperatura'].idxmax(), 'País'])
    col5.metric("Total de Países", f"{len(df['País'].unique())}")

    # Gráficos Comparativos
    st.subheader("Gráficos Comparativos")
    col1, col2 = st.columns(2)

    # Gráfico 1: Top 10 países con más precipitaciones
    with col1:
        fig1 = px.bar(
            df.sort_values('Precipitaciones', ascending=False).head(10),
            x='País',
            y='Precipitaciones',
            title="Top 10 Países con Más Precipitaciones",
            color='País',
            color_discrete_sequence=px.colors.sequential.Cividis_r
        )
        st.plotly_chart(fig1, use_container_width=True)

    # Gráfico 2: Top 10 países con menos precipitaciones
    with col2:
        fig2 = px.bar(
            df.sort_values('Precipitaciones').head(10),
            x='País',
            y='Precipitaciones',
            title="Top 10 Países con Menos Precipitaciones",
            color='País',
            color_discrete_sequence=px.colors.sequential.Viridis_r
        )
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    # Gráfico 3: Top 10 países con mayores temperaturas
    with col3:
        fig3 = px.bar(
            df.sort_values('Temperatura', ascending=False).head(10),
            x='País',
            y='Temperatura',
            title="Top 10 Países con Mayor Temperatura",
            color='País',
            color_discrete_sequence=px.colors.sequential.Magma_r
        )
        st.plotly_chart(fig3, use_container_width=True)

    # Gráfico 4: Top 10 países con menores temperaturas
    with col4:
        fig4 = px.bar(
            df.sort_values('Temperatura').head(10),
            x='País',
            y='Temperatura',
            title="Top 10 Países con Menor Temperatura",
            color='País',
            color_discrete_sequence=px.colors.sequential.ice_r
        )
        st.plotly_chart(fig4, use_container_width=True)

# Mapa Interactivo
elif opcion == "Mapa Interactivo":
    st.title("Mapa Interactivo")
    st.write("""
    Explora patrones climáticos alrededor del mundo con este mapa interactivo.
    Utiliza los filtros disponibles para visualizar datos específicos según el mes y la variable seleccionada, ya sea precipitaciones o temperaturas.
    """)
    filtro_variable = st.selectbox("Selecciona una variable", ["Precipitaciones", "Temperatura"])
    filtro_mes = st.selectbox("Selecciona el mes", df['Mes'].unique())
    df_filtrado = df[df['Mes'] == filtro_mes]

    if not df_filtrado.empty:
        fig_mapa = px.scatter_mapbox(
            df_filtrado,
            lat="Latitud",
            lon="Longitud",
            hover_name="País",
            color=filtro_variable,
            size=filtro_variable,
            zoom=1,
            mapbox_style="carto-positron"
        )
        st.plotly_chart(fig_mapa, use_container_width=True)
    else:
        st.warning(f"No hay datos disponibles para {filtro_mes}. Verifica el archivo.")

# Búsqueda por País
# Código dentro de la sección de búsqueda por país
if opcion == "Búsqueda por País":
    st.title("Búsqueda por País")
    st.write("""
    Selecciona un país para visualizar su información climática específica, incluyendo temperaturas máximas, mínimas, precipitaciones y su ubicación en el mapa.
    """)

    # Desplegable para seleccionar el país
    pais_seleccionado = st.selectbox("Selecciona un país", df['País'].unique())

    # Filtrar los datos por el país seleccionado
    datos_pais = df[df['País'] == pais_seleccionado]

    if not datos_pais.empty:
        # Mostrar las métricas clave del país seleccionado
        col1, col2 = st.columns(2)
        col1.metric("Máx. Precipitaciones", f"{datos_pais['Precipitaciones'].max()} mm")
        col1.metric("Mín. Precipitaciones", f"{datos_pais['Precipitaciones'].min()} mm")
        col2.metric("Máx. Temperatura", f"{datos_pais['Temperatura'].max()} °C")
        col2.metric("Mín. Temperatura", f"{datos_pais['Temperatura'].min()} °C")

        # Mostrar el mapa interactivo con el país seleccionado
        st.subheader("Ubicación en el Mapa")
        fig_mapa = px.scatter_mapbox(
            datos_pais,
            lat="Latitud",
            lon="Longitud",
            hover_name="País",
            zoom=4,
            mapbox_style="carto-positron",  # Estilo claro
            title=f"Ubicación de {pais_seleccionado}",
        )
        # Personalizar el tamaño y color del marcador
        fig_mapa.update_traces(marker=dict(size=15, color='green'))
        fig_mapa.update_layout(title_font_size=18, margin=dict(t=50, b=0))

        st.plotly_chart(fig_mapa, use_container_width=True)
    else:
        st.warning(f"No se encontraron datos para {pais_seleccionado}.")

# Probabilidades
elif opcion == "Probabilidades":
    st.title("Probabilidades de Eventos Climáticos")
    st.write("""
    Selecciona un país y un mes para calcular la probabilidad de enfrentar temperaturas extremas o lluvias abundantes.
    """)
    pais = st.selectbox("Selecciona un país", df['País'].unique())
    mes = st.selectbox("Selecciona un mes", df['Mes'].unique())
    datos = df[(df['País'] == pais) & (df['Mes'] == mes)]

    if not datos.empty:
        # Preparar datos para predicción
        prec = datos['Precipitaciones'].mean()
        temp = datos['Temperatura'].mean()
        prob_lluvia = modelo_lluvia.predict_proba(scaler_lluvia.transform([[prec]]))[0][1]
        prob_temp = modelo_temp.predict_proba(scaler_temp.transform([[temp]]))[0][1]

        col1, col2 = st.columns(2)
        col1.metric("Probabilidad de Lluvias Abundantes", f"{prob_lluvia * 100:.2f}%")
        col2.metric("Probabilidad de Temperaturas Altas", f"{prob_temp * 100:.2f}%")
    else:
        st.warning(f"No hay datos disponibles para {pais} en {mes}.")
