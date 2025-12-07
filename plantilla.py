# ============================
# 📦 Importación de librerías
# ============================

# Manejo de bases de datos y lectura de Excel
import pandas as pd
# Creación de mapas interactivos
import folium
from folium.plugins import MarkerCluster # Agrupa marcadores para no saturar el mapa
# Lectura de archivos Excel (.xlsx)
import openpyxl
# Creación de la interfaz web
import streamlit as st
from streamlit.components.v1 import html # Permite incrustar HTML dentro de Streamlit

# import (TODAS LAS LIBRERIAS) luego ponemos pip install en el Terminal

# ============================
# ⚙️ Configuración inicial de Streamlit
# ============================

# Establece el ancho de la página a "wide" (más espacio horizontal para el contenido)
st.set_page_config(layout="wide")

# ============================
# 📂 Cargar la base de datos
# ============================

# Lee el archivo Excel donde está toda la información histórica (nuestra base de datos)
ha_pe = pd.read_excel('Dataset.xlsx')

# ============================
# 📌 Navegación entre páginas
# ============================

# Lista de secciones disponibles en la barra lateral
paginas = ['Bienvenido', 'Mapa Histórico', 'Hecho del Día']

# Crea un menú desplegable en la barra lateral para elegir la página
pagina_seleccionada = st.sidebar.selectbox('Selecciona la sección que deseas ver', paginas)

# ============================
# 🏠 Página: BIENVENIDO
# ============================

if pagina_seleccionada == 'Bienvenido':

    # La función st.markdown permite centrar y agrandar la letra del título de la web en Streamlit.
    st.markdown("<h1 style='text-align: center;'>HISTORIAPP🕰️🇵🇪</h1>", unsafe_allow_html=True)

    # Creamos una fila de 3 columnas para centrar la imagen en la segunda
    col1, col2, col3 = st.columns([1, 4, 1])  # La columna 2 es la más grande

    # Mostramos la imagen dentro de la columna central
    with col2:
        st.image("portada.jpg", use_container_width=True)

    # Texto de bienvenida
    texto = """Bienvenido a HistoriApp 🇵🇪✨, un espacio creado para que el descubrir la historia del Perú sea fácil, entretenido y al alcance de todos. Aquí podrás explorar hechos clave, personajes, efemérides y hasta recibir un hecho histórico del día con solo un click. Mi objetivo es acercar nuestro pasado de una forma clara, didáctica y moderna, para que cualquier peruano —desde estudiantes hasta curiosos— pueda aprender, recordar y conectar con las raíces de nuestro país. ¡Prepárate para viajar por el tiempo de manera simple y divertida! 🚀📚    """
    
   # Centramos el párrafo con HTML + ancho máximo
    st.markdown(f"""<div style='display: flex; justify-content: center;'>
            <div style='max-width: 900px; text-align: justify; font-size: 20px;'>
                {texto}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    # <div style='max-width: 900px; text-align: justify; font-size: 20px;'>{texto}</div>: Esta es una cadena de código HTML. 
    # La etiqueta <div> se utiliza para agrupar contenido en HTML. 
    # En este caso, el texto está justificado (text-align: justify;). 
    # El tamaño de la fuente se establece en 20 píxeles (font-size: 20px;).
    # El texto dentro de las etiquetas <div> es la variable texto.
    # f"": Esto es un f-string en Python.
    # Permite insertar el valor de una variable directamente en la cadena. 
    # En este caso, {texto} se reemplaza por el valor de la variable texto.

# ============================
# 🗺️ Página: MAPA HISTÓRICO
# ============================

elif  pagina_seleccionada == 'Mapa Histórico':

    # Agregamos un título centrado
    st.markdown("<h1 style='text-align: center;'>🗺️ Donde Pasó la Historia</h1>", unsafe_allow_html=True)

    # Agregamos un  texto explicativo del mapa
    texto_2 = """
✨ Explora el Perú como nunca antes ✨
Este mapa interactivo te invita a viajar por el tiempo y el territorio. Solo haz clic en los pines 📍 y descubre dónde y qué ocurrió en distintas regiones del Perú durante las últimas décadas. Cada punto es una historia esperando ser contada… ¡dale zoom, curiosea y déjate sorprender! 🗺️🔥    """

    # Mostramos el texto
    st.markdown(f"<div style='text-align: justify; font-size: 18px;'>{texto_2}</div>", unsafe_allow_html=True)

    # Creamos mapa centrado en Perú
    mapa = folium.Map(location=[-10.39, -74.14], zoom_start=6)

    # Creamos clúster o contenedor para agrupar marcadores
    cluster = MarkerCluster().add_to(mapa)

    # Recorremos cada fila del dataset para crear un marcador
    for index, row in ha_pe.iterrows():
        
        # HTML personalizado para cada popup
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

        # Añadimos el marcador al mapa
        folium.Marker(
            location=[row['latitud'], row['longitud']],
            popup=folium.Popup(popup_html, max_width=300)
        ).add_to(cluster)

    # Render del mapa: convertimos el mapa a HTML para mostrarlo en Streamlit
    map_html = mapa._repr_html_()

    # Mostrar en Streamlit
    html(map_html, height=2000) 

# ============================
# 🎲 Página: HECHO DEL DÍA
# ============================

else:

    # Agregamos un título para la página de gráficos
    st.markdown("<h1 style='text-align: center;'>🎲 Elige tu Hecho Histórico</h1>", unsafe_allow_html=True)

    # Recargamos el dataset (puede ser el mismo, pero por si se edita)
    df = pd.read_excel("Dataset.xlsx")

    st.write("Explora hechos históricos por década, región o categoría… o deja que el destino decida por ti 😎✨") # Agregamos una descripción

    # Obtenemos listas de filtros desde la base de datos
    decadas = sorted(df['decada'].dropna().unique())
    lugares = sorted(df['lugar'].dropna().unique())
    categorias = sorted(df['categoria'].dropna().unique())

    # Filtramos en 3 columnas
    col1, col2, col3 = st.columns(3)
    decada_filtro = col1.selectbox("📅 Década", ["Cualquiera"] + decadas)
    lugar_filtro = col2.selectbox("📍 Lugar", ["Cualquiera"] + lugares)
    cat_filtro = col3.selectbox("🏷️ Categoría", ["Cualquiera"] + categorias)

    # Botón para mostrar un hecho al azar
    if st.button("🎲 Mostrar hecho histórico"):

        df_filtrado = df.copy()

        # Aplicamos filtros según lo elegido
        if decada_filtro != "Cualquiera":
            df_filtrado = df_filtrado[df_filtrado["decada"] == decada_filtro]

        # Filtramos por lugar
        if lugar_filtro != "Cualquiera":
            df_filtrado = df_filtrado[df_filtrado["lugar"] == lugar_filtro]

        # Filtramos por categoría
        if cat_filtro != "Cualquiera":
            df_filtrado = df_filtrado[df_filtrado["categoria"] == cat_filtro]

        # Si no queda nada, mostramos un error
        if df_filtrado.empty:
            st.error("😓 No hay hechos históricos con esos filtros. Prueba con otros.")
        else:
            # Elegimos un evento al azar
            evento = df_filtrado.sample(1).iloc[0]

            # --- Mostrar tarjeta estilo Instagram ---
            st.markdown("---")

            # COnfiguramos tarjeta estilo Instagram
            html_evento = f"""
            <div style="border-radius:15px; padding:15px; background:#F0F0F0; box-shadow:0 0 10px rgba(0,0,0,0.1); font-family:Arial;">
    
            <h2 style="margin-top:0;">🇵🇪 {evento['titulo_evento']}</h2>

            <p><b>📅 Fecha:</b> {str(evento['fecha']).split(' ')[0]}</p>
            <p><b>📍 Lugar:</b> {evento['lugar']}</p>
            <p><b>🏷️ Categoría:</b> {evento['categoria']}</p>

            <p style="margin-top:10px;">{evento['descripcion_corta']}</p>

            </div>
            """

            # Mostramos la tarjeta
            st.markdown(html_evento, unsafe_allow_html=True)

            # Mostramos imagen si existe
            if pd.notna(evento["imagen"]):
                st.image(evento["imagen"], use_container_width=True)
            else:
                st.info("No hay imagen disponible para este suceso.")