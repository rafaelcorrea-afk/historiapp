# A continuación instalamos las librerías
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import random
import datetime
import random, datetime
import openpyxl
import streamlit as st
from streamlit.components.v1 import html

# import (TODAS LAS LIBRERIAS) luego poner pip install

st.set_page_config(layout="wide")

#cargamos la base de datos
ha_pe = pd.read_excel('Dataset.xlsx')


# Este comando sirve para ejecutar un script de Python en Streamlit.
# python -m streamlit run plantilla.py



# Creamos la lista de páginas
paginas = ['Bienvenido', 'Mapa Histórico', 'Hecho del Día']

# Creamos botones de navegación tomando la lista de páginas
pagina_seleccionada = st.sidebar.selectbox('Selecciona la sección que deseas ver', paginas)

# Generamos condicionales para mostrar el contenido de cada página
if pagina_seleccionada == 'Bienvenido':

    # La función st.markdown permite centrar y agrandar la letra del título de la web en Streamlit.
    st.markdown("<h1 style='text-align: center;'>HISTORIAPP🕰️🇵🇪</h1>", unsafe_allow_html=True)

    # En la primera columna colocamos la imagen de perfil
    col1, col2, col3 = st.columns([1, 4, 1])  # la columna central es más grande

    with col2:
        st.image("portada.jpg", use_container_width=True)

    texto = """Bienvenido a HistoriApp 🇵🇪✨, un espacio creado para que el descubrir la historia del Perú sea fácil, entretenido y al alcance de todos. Aquí podrás explorar hechos clave, personajes, efemérides y hasta recibir un hecho histórico del día con solo un click. Mi objetivo es acercar nuestro pasado de una forma clara, didáctica y moderna, para que cualquier peruano —desde estudiantes hasta curiosos— pueda aprender, recordar y conectar con las raíces de nuestro país. ¡Prepárate para viajar por el tiempo de manera simple y divertida! 🚀📚    """
    
    # Mostramos el texto
    st.markdown(f"""<div style='display: flex; justify-content: center;'>
            <div style='max-width: 900px; text-align: justify; font-size: 20px;'>
                {texto}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    # <div style='text-align: justify; font-size: 15px;'>{texto}</div>: Esta es una cadena de código HTML. 
    # La etiqueta <div> se utiliza para agrupar contenido en HTML. 
    # En este caso, el texto está justificado (text-align: justify;). 
    # El tamaño de la fuente se establece en 15 píxeles (font-size: 15px;).
    # El texto dentro de las etiquetas <div> es la variable texto.
    # f"": Esto es un f-string en Python.
    # Permite insertar el valor de una variable directamente en la cadena. 
    # En este caso, {texto} se reemplaza por el valor de la variable texto.

elif  pagina_seleccionada == 'Mapa Histórico':

    # Agregamos un título
    st.markdown("<h1 style='text-align: center;'>🗺️ Donde Pasó la Historia</h1>", unsafe_allow_html=True)

    # Agregar un  texto
    texto_2 = """
✨ Explora el Perú como nunca antes ✨
Este mapa interactivo te invita a viajar por el tiempo y el territorio. Solo haz clic en los pines 📍 y descubre dónde y qué ocurrió en distintas regiones del Perú durante las últimas décadas. Cada punto es una historia esperando ser contada… ¡dale zoom, curiosea y déjate sorprender! 🗺️🔥    """

    # Mostramos el texto
    st.markdown(f"<div style='text-align: justify; font-size: 18px;'>{texto_2}</div>", unsafe_allow_html=True)

    # <div style='text-align: justify; font-size: 15px;'>{texto_2}</div>: Esta es una cadena de código HTML.
    # La etiqueta <div> se utiliza para agrupar contenido en HTML.
    # En este caso, el texto está justificado (text-align: justify;).
    # El tamaño de la fuente se establece en 15 píxeles (font-size: 15px;).
    # El texto dentro de las etiquetas <div> es la variable texto_2.
    # f"": Esto es un f-string en Python.
    # Permite insertar el valor de una variable directamente en la cadena. 
    # En este caso, {texto_2} se reemplaza por el valor de la variable texto.


    # Crear mapa base
    mapa = folium.Map(location=[-10.39, -74.14], zoom_start=6)

    # Crear clúster
    cluster = MarkerCluster().add_to(mapa)

    # Añadir marcadores
    for index, row in ha_pe.iterrows():
        popup_html = f"""
        <div style="width:260px; font-family:Arial;">

            <!-- Fecha del suceso -->
            <p style="font-size:12px; color:#777; margin-bottom:5px;">
                📅 {row['fecha']}
            </p>

            <!-- Imagen principal -->
            <img src="{row['imagen']}" 
                style="width:100%; height:auto; border-radius:10px;">

            <!-- Título del evento -->
            <h4 style="margin-top:10px; margin-bottom:5px;">
                {row['titulo_evento']}
            </h4>

            <!-- Lugar -->
            <p style="margin:0;">
                <b>📍 Lugar:</b> {row['lugar']}
            </p>

            <!-- Descripción -->
            <p style="margin-top:8px;">
                {row['descripcion_corta']}
            </p>

        </div>
        """

        folium.Marker(
            location=[row['latitud'], row['longitud']],
            popup=folium.Popup(popup_html, max_width=300)
        ).add_to(cluster)

    # Render del mapa
    map_html = mapa._repr_html_()

    # Mostrar en Streamlit
    html(map_html, height=2000) 
    
else:

    # Agregamos un título para la página de gráficos
    st.markdown("<h1 style='text-align: center;'>🎲 Elige tu Hecho Histórico</h1>", unsafe_allow_html=True)

    # --- Cargar la data ---
    df = pd.read_excel("Dataset.xlsx")

    st.write("Explora hechos históricos por década, región o categoría… o deja que el destino decida por ti 😎✨")

    # Lista de décadas según tu dataset (ya vienen como "1980s", "1990s", etc.)
    decadas = sorted(df['decada'].dropna().unique())

    # LUGARES: puedes usarlos como "departamentos" o "ciudades"
    lugares = sorted(df['lugar'].dropna().unique())

    # Categorías
    categorias = sorted(df['categoria'].dropna().unique())

    # --- Selectores ---
    col1, col2, col3 = st.columns(3)

    decada_filtro = col1.selectbox("📅 Década", ["Cualquiera"] + decadas)
    lugar_filtro = col2.selectbox("📍 Lugar", ["Cualquiera"] + lugares)
    cat_filtro = col3.selectbox("🏷️ Categoría", ["Cualquiera"] + categorias)

    # --- Botón ---
    if st.button("🎲 Mostrar hecho histórico"):

        df_filtrado = df.copy()

        # Filtrar por década
        if decada_filtro != "Cualquiera":
            df_filtrado = df_filtrado[df_filtrado["decada"] == decada_filtro]

        # Filtrar por lugar
        if lugar_filtro != "Cualquiera":
            df_filtrado = df_filtrado[df_filtrado["lugar"] == lugar_filtro]

        # Filtrar por categoría
        if cat_filtro != "Cualquiera":
            df_filtrado = df_filtrado[df_filtrado["categoria"] == cat_filtro]

        # Validación
        if df_filtrado.empty:
            st.error("😓 No hay hechos históricos con esos filtros. Prueba con otros.")
        else:
            # Elegir uno al azar
            evento = df_filtrado.sample(1).iloc[0]

            # --- Mostrar tarjeta estilo Instagram ---
            st.markdown("---")

            html_evento = f"""
            <div style="border-radius:15px; padding:15px; background:black; box-shadow:0 0 10px rgba(0,0,0,0.1); font-family:Arial;">
    
            <h2 style="margin-top:0;">✨ {evento['titulo_evento']}</h2>

            <p><b>📅 Fecha:</b> {str(evento['fecha']).split(' ')[0]}</p>
            <p><b>📍 Lugar:</b> {evento['lugar']}</p>
            <p><b>🏷️ Categoría:</b> {evento['categoria']}</p>

            <p style="margin-top:10px;">{evento['descripcion_corta']}</p>

            </div>
            """

            # 🔥 Aquí está la clave:
            st.markdown(html_evento, unsafe_allow_html=True)

            if pd.notna(evento["imagen"]):
                st.image(evento["imagen"], use_container_width=True)
            else:
                st.info("No hay imagen disponible para este suceso.")