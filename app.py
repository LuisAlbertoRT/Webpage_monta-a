import streamlit as st
from supabase import create_client, Client
import pandas as pd
import pydeck as pdk
import urllib.parse
from datetime import datetime

# 1. Configuración de la página
st.set_page_config(
    page_title="México Al Aire Libre", 
    page_icon="🏔️", 
    layout="centered"
)

# 2. Conexión a tu proyecto de Supabase
SUPABASE_URL = "https://nmabblcjutzyzipbophi.supabase.co"
SUPABASE_KEY = "sb_publishable_c1eTQYTn6IXBGVkghPSXrA_JJwaMyJT"

@st.cache_resource
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

try:
    supabase: Client = init_supabase()
except Exception as e:
    st.error("Error de conexión con la base de datos.")

# 3. ESTILOS CSS AVANZADOS (Rediseño de Interfaz Premium - MODO LUMINOSO)
st.markdown("""
    <style>
    /* Fondo principal: Blanco alpino texturizado suave */
    .stApp { 
        background-color: #F8FAFC; 
    }
    
    /* Contenedor del Banner Principal con Imagen de Fondo y degradado suave */
    .hero-banner {
        background-image: linear-gradient(rgba(255, 255, 255, 0.1), #F8FAFC), 
                          url('https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1200&q=80');
        background-size: cover;
        background-position: center 35%;
        padding: 55px 20px;
        border-radius: 24px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(15, 23, 42, 0.08);
    }
    .hero-title {
        color: #0F172A;
        font-size: 38px;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 6px;
        text-shadow: 0 2px 10px rgba(255,255,255,0.8);
    }
    .hero-subtitle {
        color: #334155;
        font-size: 15px;
        font-weight: 500;
        text-shadow: 0 2px 8px rgba(255,255,255,0.8);
    }

    /* Pestañas de Navegación Estilizadas (Luminosas) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: #E2E8F0;
        padding: 6px;
        border-radius: 14px;
        border: 1px solid #CBD5E1;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        white-space: pre;
        background-color: transparent;
        border-radius: 10px;
        color: #475569;
        font-weight: 600;
        transition: all 0.3s ease;
        padding: 0 16px;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #0F172A;
        background-color: #F1F5F9;
    }
    .stTabs [aria-selected="true"] {
        background-color: #00C853 !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(0, 200, 83, 0.25);
    }

    /* Tarjetas de Eventos de Diseño Moderno (Cards Claras) */
    .event-card {
        background: #FFFFFF;
        padding: 24px;
        border-radius: 20px;
        border: 1px solid #E2E8F0;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(15, 23, 42, 0.04);
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    }
    .event-card:hover {
        border-color: #00C853;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 200, 83, 0.08);
    }
    .event-title { 
        color: #0F172A; 
        font-size: 23px; 
        font-weight: 700; 
        margin-bottom: 6px; 
    }
    .event-meta { 
        color: #64748B; 
        font-size: 14px; 
        margin-bottom: 16px; 
        display: flex; 
        gap: 18px;
        font-weight: 500;
    }
    .event-desc { 
        color: #334155; 
        font-size: 15px; 
        line-height: 1.6; 
        margin-bottom: 18px; 
    }

    /* Botón Premium Verde Vibrante de WhatsApp */
    .btn-wa-premium {
        background-color: #00C853;
        color: #FFFFFF !important;
        padding: 14px 24px;
        border-radius: 12px;
        text-decoration: none;
        font-weight: 700;
        font-size: 15px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        box-shadow: 0 4px 15px rgba(0, 200, 83, 0.2);
        text-align: center;
    }
    .btn-wa-premium:hover {
        background-color: #00E676;
        box-shadow: 0 6px 20px rgba(0, 200, 83, 0.35);
    }

    /* Estilo Línea del Tiempo de la Agenda (Clara) */
    .agenda-timeline {
        border-left: 3px solid #E2E8F0;
        padding-left: 24px;
        margin-left: 12px;
        margin-top: 20px;
    }
    .agenda-node {
        background: #FFFFFF;
        padding: 20px;
        border-radius: 16px;
        margin-bottom: 18px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 15px rgba(15, 23, 42, 0.04);
        position: relative;
    }
    .agenda-node::before {
        content: '';
        position: absolute;
        left: -37px;
        top: 24px;
        background: #00C853;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        border: 4px solid #F8FAFC;
    }

    /* Estilos Premium para la pestaña Sobre Nosotros en Móvil (Clara) */
    .about-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 20px;
        padding: 22px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(15, 23, 42, 0.04);
    }
    .about-badge {
        background-color: rgba(0, 200, 83, 0.1);
        color: #00B0FF;
        color: #00C853;
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 10px;
        text-transform: uppercase;
    }
    .about-text {
        color: #334155;
        font-size: 15px;
        line-height: 1.6;
    }
    
    /* Pequeños ajustes para inputs del modo claro */
    .stTextInput>div>div>input {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 4. Cabecera Visual (Hero Banner)
st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">🏔️ México Al Aire Libre</div>
        <div class="hero-subtitle">Descubre expediciones, consulta rutas y conecta directo con guías de montaña</div>
    </div>
""", unsafe_allow_html=True)

# 5. Descarga y ORDENACIÓN de datos desde Supabase
try:
    response = supabase.table("eventos_montana").select("*").execute()
    eventos_crudos = response.data
except Exception as e:
    st.error(f"Error al cargar base de datos: {e}")
    eventos_crudos = []

# Lógica de Ordenación Cronológica Ascendente
hoy = datetime.now().date()
eventos_futuros = []
eventos_pasados = []

for ev in eventos_crudos:
    try:
        ev['fecha_dt'] = datetime.strptime(ev['fecha'], "%Y-%m-%d").date()
        if ev['fecha_dt'] >= hoy:
            eventos_futuros.append(ev)
        else:
            eventos_pasados.append(ev)
    except:
        ev['fecha_dt'] = hoy
        eventos_futuros.append(ev)

eventos_futuros.sort(key=lambda x: x['fecha_dt'])
eventos = eventos_futuros + eventos_pasados

# 6. CONFIGURACIÓN DE PESTAÑAS
tab_calendario, tab_lista, tab_mapa, tab_about = st.tabs(["📅 Agenda", "📌 Eventos", "🗺️ Mapa", "🤝 Nosotros"])

# ---------------------------------------------------------
# PESTAÑA 1: AGENDA DE SALIDAS
# ---------------------------------------------------------
with tab_calendario:
    st.markdown("<p style='color: #475569;'>Filtra por mes para ver las próximas cumbres en orden cronológico.</p>", unsafe_allow_html=True)
    
    meses_disponibles = ["Todos los próximos"]
    for ev in eventos_futuros:
        nombre_mes = ev['fecha_dt'].strftime("%B %Y").capitalize()
        if nombre_mes not in meses_disponibles:
            meses_disponibles.append(nombre_mes)
            
    mes_seleccionado = st.radio("Seleccionar período:", meses_disponibles, horizontal=True, label_visibility="collapsed")
    st.markdown("##")
    
    eventos_agenda = eventos_futuros
    if mes_seleccionado != "Todos los próximos":
        eventos_agenda = [e for e in eventos_futuros if e['fecha_dt'].strftime("%B %Y").capitalize() == mes_seleccionado]
        
    if eventos_agenda:
        st.markdown('<div class="agenda-timeline">', unsafe_allow_html=True)
        for ev in eventos_agenda:
            f_format = ev['fecha_dt'].strftime("%A, %d de %B de %Y")
            st.markdown(f"""
            <div class="agenda-node">
                <span style="color: #00C853; font-weight: 700; font-size: 12px; letter-spacing: 0.5px;">🟢 {f_format.upper()}</span>
                <h3 style="margin: 6px 0 4px 0; color: #0F172A; font-size: 21px; font-weight: 700;">{ev['titulo']}</h3>
                <p style="margin: 0; color: #64748B; font-size: 14px;">Guía u Organizador: <b style="color: #334155;">{ev['organizador']}</b></p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander(f"📖 Detalles e Itinerario para {ev['titulo']}"):
                st.write(ev['descripcion'])
                tel = ev.get('telefono_whatsapp', '')
                if tel:
                    texto_wa = f"¡Hola! Me interesa la salida de {ev['titulo']} del {ev['fecha']}. ¿Me das más información?"
                    link_wa = f"https://wa.me/{tel}?text={urllib.parse.quote(texto_wa)}"
                    st.markdown(f'<a href="{link_wa}" target="_blank" class="btn-wa-premium">💬 Unirse al Grupo / Reservar</a>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No hay eventos programados para este mes.")

# ---------------------------------------------------------
# PESTAÑA 2: LISTA GENERAL DE EVENTOS
# ---------------------------------------------------------
with tab_lista:
    search_query = st.text_input("🔍 Buscar rutas o cumbres...", placeholder="Ej. Iztaccíhuatl, Ajusco...")
    
    eventos_filtrados = eventos
    if search_query:
        eventos_filtrados = [e for e in eventos if search_query.lower() in e['titulo'].lower() or search_query.lower() in e['descripcion'].lower()]
        
    if not eventos_filtrados:
        st.info("No se encontraron expediciones.")
    else:
        for ev in eventos_filtrados:
            fecha_formateada = ev['fecha_dt'].strftime("%d %b, %Y") if 'fecha_dt' in ev else ev['fecha']
            es_pasado = " (Finalizado)" if ev.get('fecha_dt') and ev['fecha_dt'] < hoy else ""
            color_titulo = "#94A3B8" if es_pasado else "#0F172A"

            st.markdown(f"""
            <div class="event-card">
                <div class="event-title" style="color: {color_titulo};">{ev['titulo']}<span style="font-size:14px; color:#EF4444; font-weight:500; margin-left:10px;">{es_pasado}</span></div>
                <div class="event-meta">
                    <span>📅 {fecha_formateada}</span>
                    <span>👤 Por: {ev['organizador']}</span>
                </div>
                <div class="event-desc">{ev['descripcion']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if not es_pasado:
                tel = ev.get('telefono_whatsapp', '')
                if tel:
                    texto_mensaje = f"¡Hola! Vi el evento '{ev['titulo']}' del {fecha_formateada}. ¿Quedan lugares?"
                    link_wa = f"https://wa.me/{tel}?text={urllib.parse.quote(texto_mensaje)}"
                    st.markdown(f'<a href="{link_wa}" target="_blank" class="btn-wa-premium">💬 Solicitar Informes vía WhatsApp</a>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# PESTAÑA 3: MAPA EXPLORADOR CORREGIDO (CON ENTORNO CLARO)
# ---------------------------------------------------------
with tab_mapa:
    st.markdown("<h4 style='color: #0F172A; margin-bottom: 2px;'>🗺️ Mapa Base de Expediciones Activas</h4>", unsafe_allow_html=True)
    st.write("Pasa el cursor o presiona los círculos para ver el nombre y la fecha de la expedición.")
    
    coordenadas = []
    for ev in eventos:
        if ev.get('latitud') and ev.get('longitud'):
            try:
                fecha_str = ev['fecha_dt'].strftime("%d %b, %Y") if 'fecha_dt' in ev else ev['fecha']
                coordenadas.append({
                    "lat": float(ev['latitud']),
                    "lon": float(ev['longitud']),
                    "tooltip_text": f"{ev['titulo']} — 📅 {fecha_str}"
                })
            except:
                continue
                
    if coordenadas:
        df_mapa = pd.DataFrame(coordenadas)
        
        layer = pdk.Layer(
            "ScatterplotLayer",
            df_mapa,
            get_position="[lon, lat]",
            get_color="[0, 200, 83, 210]",  # Verde pino unificado
            get_radius=6000,
            pickable=True,
            opacity=0.85,
            stroked=True,
            filled=True,
            radius_scale=1,
            radius_min_pixels=7,
            radius_max_pixels=16,
            line_width_min_pixels=1.5,
            get_line_color=[255, 255, 255]
        )
        
        view_state = pdk.ViewState(
            latitude=df_mapa["lat"].mean(),
            longitude=df_mapa["lon"].mean(),
            zoom=7.0,
            pitch=0
        )
        
        # Estilo "road" nativo que se acopla a la perfección con la paleta limpia del sitio
        st.pydeck_chart(pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip={"text": "{tooltip_text}"},
            map_style="road"
        ))
    else:
        st.info("No hay ubicaciones registradas con coordenadas válidas.")

# ---------------------------------------------------------
# PESTAÑA 4: SOBRE NOSOTROS
# ---------------------------------------------------------
with tab_about:
    st.markdown("<h3 style='color: #0F172A; font-weight: 700; margin-bottom: 5px;'>🤝 Conoce el Proyecto</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #475569;'>Nuestra misión es hacer la montaña accesible y segura para todos.</p>", unsafe_allow_html=True)
    st.markdown("##")
    
    st.image(
        "https://images.unsplash.com/photo-1551632436-cbf8dd35adfa?auto=format&fit=crop&w=800&q=80", 
        caption="Comunidad unida por la naturaleza",
        use_container_width=True
    )
    st.markdown("""
    <div class="about-card">
        <div class="about-badge">Propósito</div>
        <div class="about-text">
            <b>México Al Aire Libre</b> es una iniciativa 100% sin fines de lucro. Nacimos con la idea fija de crear un puente directo entre montañistas apasionados y guías locales, eliminando intermediarios para fomentar el turismo deportivo en México.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.image(
        "https://images.unsplash.com/photo-1522163182402-834f871fd851?auto=format&fit=crop&w=800&q=80", 
        caption="Cuidado mutuo en cada ascenso",
        use_container_width=True
    )
    st.markdown("""
    <div class="about-card">
        <div class="about-badge">Seguridad en Equipo</div>
        <div class="about-text">
            La montaña se respeta. Creamos este espacio no solo para armar rutas, sino para asegurar que ningún equipo salga rezagado. Promovemos el <b>cuidado mutuo</b>, compartimos la logística de seguridad de los líderes de grupo y verificamos que cada expedición cuente con el equipo de comunicación y rescate necesario.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="about-card" style="text-align: center; border-left: 4px solid #00C853;">
        <p style="color: #64748B; font-size: 14px; margin: 0; font-style: italic;">"Subir una montaña no es solo alcanzar la cumbre, es asegurarnos de que todo el grupo regrese a salvo a casa."</p>
    </div>
    """, unsafe_allow_html=True)