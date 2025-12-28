import streamlit as st
import requests
from fpdf import FPDF  # <--- Asegúrate de tener 'fpdf' en requirements.txt

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Monitor Bolivia", page_icon="🕵️‍♂️")

# 2. SEGURIDAD: REEMPLAZO DE LA LÍNEA DE LA API KEY
# Aquí usamos el secreto que guardamos en el cuadro azul de Streamlit
API_KEY = st.secrets["NEWS_API_KEY"] 

TOPIC = "bolivia AND (droga OR narcotrafico OR incautacion)"

# 3. FUNCIÓN DE BÚSQUEDA CON CACHÉ
@st.cache_data(ttl=3600) 
def buscar_noticias():
    url = f"https://newsapi.org/v2/everything?q={TOPIC}&language=es&sortBy=publishedAt&apiKey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('articles', [])
    return []

# 4. FUNCIÓN PARA GENERAR EL PDF
def generar_pdf(noticias):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Reporte de Inteligencia - Bolivia", ln=True, align='C')
    pdf.ln(10)
    
    for art in noticias:
        pdf.set_font("Arial", 'B', 12)
        # Limpieza de caracteres para evitar errores en el PDF
        titulo = art['title'].encode('latin-1', 'ignore').decode('latin-1')
        pdf.multi_cell(0, 10, txt=titulo)
        
        pdf.set_font("Arial", '', 10)
        fuente = f"Fuente: {art['source']['name']} | Fecha: {art['publishedAt'][:10]}"
        pdf.cell(0, 10, txt=fuente.encode('latin-1', 'ignore').decode('latin-1'), ln=True)
        pdf.ln(10)
    return pdf.output(dest='S').encode('latin-1')

# 5. INTERFAZ VISUAL
st.title("🕵️‍♂️ Monitor de Noticias: Seguridad y Narcotráfico")
noticias = buscar_noticias()

# 6. LÓGICA DEL BOTÓN DE DESCARGA EN LA BARRA LATERAL
if noticias:
    st.sidebar.header("Opciones de Reporte")
    pdf_bytes = generar_pdf(noticias)
    st.sidebar.download_button(
        label="📥 Descargar Reporte PDF",
        data=pdf_bytes,
        file_name="reporte_bolivia.pdf",
        mime="application/pdf"
    )
    
    # Mostrar noticias en pantalla
    for art in noticias:
        with st.container():
            st.subheader(art['title'])
            st.write(f"**Fuente:** {art['source']['name']} | **Fecha:** {art['publishedAt'][:10]}")
            st.write(art['description'])
            st.markdown(f"[Leer noticia completa]({art['url']})")
            st.markdown("---")
else:
    st.warning("No se encontraron noticias con los criterios actuales.")
