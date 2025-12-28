import streamlit as st
import requests
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Monitor de Seguridad - Bolivia", page_icon="🔍")

st.title("🕵️‍♂️ Monitor de Noticias: Seguridad y Narcotráfico")
st.markdown("---")

# Tu API Key de NewsAPI
API_KEY = "58af0eee6902477c9c63d8af2fae2fca"
TOPIC = "bolivia AND (droga OR narcotrafico OR incautacion)"

def buscar_noticias():
    url = f"https://newsapi.org/v2/everything?q={TOPIC}&language=es&sortBy=publishedAt&apiKey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('articles', [])
    else:
        st.error("Error al conectar con la API")
        return []

noticias = buscar_noticias()

if not noticias:
    st.warning("No se encontraron noticias recientes.")
else:
    for art in noticias:
        with st.container():
            col1, col2 = st.columns([1, 3])
            with col1:
                if art['urlToImage']:
                    st.image(art['urlToImage'])
            with col2:
                st.subheader(art['title'])
                st.write(f"**Fuente:** {art['source']['name']} | **Fecha:** {art['publishedAt'][:10]}")
                st.write(art['description'])
                st.markdown(f"[Leer noticia completa]({art['url']})")
            st.markdown("---")
