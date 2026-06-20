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

# 3. ESTILOS CSS AVANZADOS (Estilo Strava Orange + Tooltip Fix + Footer)
st.markdown("""
    <style>
    /* Fondo principal: Blanco alpino */
    .stApp { 
        background-color: #F8FAFC; 
    }
    
    /* Forzar color oscuro en textos globales del sistema */
    .stApp p, .stApp span, .stApp label, .stApp h1, .stApp h2, .stApp h3, .stApp h4 {
        color: #0F172A !important;
    }
    
    /* Contenedor del Banner Principal */
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
    .hero-banner .hero-title {
        color: #0F172A !important;
        font-size: 38px;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 6px;
    }
    .hero-banner .hero-subtitle {
        color: #334155 !important;
        font-size: 15px;
        font-weight: 500;
    }

    /* Pestañas de Navegación (Estilo Strava) */
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
        transition: all 0.3s ease;
        padding: 0 16px;
    }
    .stTabs [data-baseweb="tab"] p {
        color: #475569 !important;
        font-weight: 600 !important;
    }
    .stTabs [data-baseweb="tab"]:hover p {
        color: #0F172A !important;
    }
    /* Pestaña activa: Naranja Strava */
    .stTabs [aria-selected="true"] {
        background-color: #FC4C02 !important;
        box-shadow: 0 4px 12px rgba(252, 76, 2, 0.25);
    }
    .stTabs [aria-selected="true"] p {
        color: #FFFFFF !important;
    }

    /* CORRECCIÓN PARA EXPENDERS */
    [data-testid="stExpander"] details summary {
        color: #0F172A !important;
        font-weight: 600 !important;
    }
    [data-testid="stExpander"] details summary svg {
        fill: #0F172A !important;
    }
    [data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
    }

    /* Tarjetas de Eventos Claras */
    .event-card {
        background: #FFFFFF;
        padding: 24px;
        border-radius: 20px;
        border: 1px solid #E2E8F0;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(15, 23, 42, 0.04);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .event-card:hover {
        border-color: #FC4C02;
        transform: translateY(-2px);
    }
    .event-card .event-title { 
        color: #0F172A !important; 
        font-size: 23px; 
        font-weight: 700; 
        margin-bottom: 6px; 
    }
    .event-card .event-meta { 
        color: #64748B !important; 
        font-size: 14px; 
        margin-bottom: 16px; 
        display: flex; 
        gap: 18px;
        font-weight: 500;
    }
    .event-card .event-desc { 
        color: #334155 !important; 
        font-size: 15px; 
        line-height: 1.6; 
        margin-bottom: 18px; 
    }

    /* Botón Premium Naranja Strava de WhatsApp */
    .btn-wa-premium {
        background-color: #FC4C02;
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
        box-shadow: 0 4px 15px rgba(252, 76, 2, 0.2);
        text-align: center;
    }
    .btn-wa-premium:hover {
        background-color: #FF6624;
    }

    /* Estilo Línea del Tiempo de la Agenda */
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
        background: #FC4C02;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        border: 4px solid #F8FAFC;
    }

    /* Estilos Premium para la pestaña Sobre Nosotros */
    .about-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(15, 23, 42, 0.04);
    }
    .about-badge {
        background-color: rgba(252, 76, 2, 0.1);
        color: #FC4C02;
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 12px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .about-text {
        color: #334155 !important;
        font-size: 15.5px;
        line-height: 1.7;
    }
    
    /* Inputs de texto forzados */
    .stTextInput>div>div>input {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
    }

    /* FIX INYECTADO PARA EL TOOLTIP DEL MAPA EN CELULARES */
    .deckgl-mouse-over-boundary {
        max-width: 280px !important;
        white-space: normal !important;
        word-wrap: break-word !important;
        font-size: 11px !important;
        font-family: inherit !important;
        padding: 8px 12px !important;
        background-color: rgba(15, 23, 42, 0.95) !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
    }

    /* ESTILO PREMIUM PARA EL FOOTER DEL DESARROLLADOR */
    .dev-footer {
        text-align: center;
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid #E2E8F0;
    }
    .dev-footer p {
        font-size: 13px !important;
        color: #64748B !important;
        margin-bottom: 8px !important;
    }
    .dev-footer a {
        color: #FC4C02 !important;
        text-decoration: none !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        transition: color 0.2s ease;
    }
    .dev-footer a:hover {
        color: #FF6624 !important;
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
    st.error("Error de conexión con la base de datos.")
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

# Componente reutilizable del Pie de Página (Footer) para proyectos
def mostrar_developer_footer():
    st.markdown("""
        <div class="dev-footer">
            <p>¿Te gusta esta plataforma o necesitas una solución similar?</p>
            <a href="https://github.com/LuisAlbertoRT" target="_blank">
                <svg height="16" width="16" viewBox="0 0 16 16" style="fill: #FC4C02; vertical-align: middle;"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path></svg>
                Contáctame en GitHub para Proyectos de Programación
            </a>
        </div>
    """, unsafe_allow_html=True)

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
                <span style="color: #FC4C02; font-weight: 700; font-size: 12px; letter-spacing: 0.5px;">🍊 {f_format.upper()}</span>
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
                    st.markdown(f'<a href="{link_wa}" target="_blank" class="btn-wa-premium">💬 Teléfono asociado</a>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No hay eventos programados para este mes.")
        
    mostrar_developer_footer()

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
                    st.markdown(f'<a href="{link_wa}" target="_blank" class="btn-wa-premium">💬 Telefono asociado</a>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
    mostrar_developer_footer()

# ---------------------------------------------------------
# PESTAÑA 3: MAPA EXPLORADOR CON ENTORNO STRAVA & FIXED TOOLTIP
# ---------------------------------------------------------
with tab_mapa:
    st.markdown("<h4 style='color: #0F172A; margin-bottom: 2px;'>🗺️ Mapa Base de Expediciones Activas</h4>", unsafe_allow_html=True)
    st.write("Presiona los círculos para ver los detalles sin que se desborde la pantalla.")
    
    coordenadas = []
    for ev in eventos:
        if ev.get('latitud') and ev.get('longitud'):
            try:
                fecha_str = ev['fecha_dt'].strftime("%d %b, %Y") if 'fecha_dt' in ev else ev['fecha']
                coordenadas.append({
                    "lat": float(ev['latitud']),
                    "lon": float(ev['longitud']),
                    "tooltip_text": f"{ev['titulo']} \n 📅 {fecha_str}"
                })
            except:
                continue
                
    if coordenadas:
        df_mapa = pd.DataFrame(coordenadas)
        
        layer = pdk.Layer(
            "ScatterplotLayer",
            df_mapa,
            get_position="[lon, lat]",
            get_color="[252, 76, 2, 210]",  # Naranja Strava
            get_radius=6000,
            pickable=True,
            opacity=0.85,
            stroked=True,
            filled=True,
            radius_scale=1,
            radius_min_pixels=8,
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
        
        st.pydeck_chart(pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip={"text": "{tooltip_text}"},
            map_style="road"
        ))
    else:
        st.info("No hay ubicaciones registradas con coordenadas válidas.")
        
    mostrar_developer_footer()

# ---------------------------------------------------------
# PESTAÑA 4: SOBRE NOSOTROS (Texto Ampliado y Épico)
# ---------------------------------------------------------
with tab_about:
    st.markdown("<h3 style='color: #0F172A; font-weight: 700; margin-bottom: 5px;'>🤝 Conoce el Proyecto</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #FC4C02; font-weight: bold; font-style: italic;'>Construyendo la red comunitaria de montañismo más grande de México.</p>", unsafe_allow_html=True)
    st.markdown("##")
    
    st.image(
        "https://images.unsplash.com/photo-1757269267274-085b02b0ce8a?q=80&w=870&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", 
        caption="Comunidad unida por la naturaleza",
        use_container_width=True
    )
    st.markdown("""
    <div class="about-card">
        <div class="about-badge">Nuestra Misión</div>
        <div class="about-text">
            <b>México Al Aire Libre</b> nació bajo una premisa firme: la montaña pertenece a todos, pero recorrerla requiere comunidad. Somos un proyecto independiente y 100% sin fines de lucro enfocado en <b>hacer el montañismo y el senderismo accesibles, organizados y seguros en todo el territorio nacional</b>.<br><br>
            A través de esta plataforma, centralizamos las convocatorias de guías locales, clubes de senderismo y líderes de expedición en un solo calendario abierto. Rompemos las barreras de desinformación para que cualquier entusiasta —desde quien busca su primer Ajusco hasta quien se prepara para el Pico de Orizaba— encuentre un grupo respaldado con el cual marchar, reduciendo los riesgos del aislamiento en la naturaleza.
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
        <div class="about-badge">Seguridad e Infraestructura Colectiva</div>
        <div class="about-text">
            Creemos que la seguridad en alta montaña no es opcional, es una responsabilidad compartida. Este espacio promueve de manera rigurosa la <b>coordinación y el cuidado mutuo de los equipos</b>. <br><br>
            No permitimos que ningún senderista camine a ciegas. Exigimos canales de comunicación directa y transparente a través de enlaces directos a grupos de coordinación; así, los equipos validan listas de equipo técnico necesario, comparten el rastreo satelital de las rutas, revisan las condiciones climáticas en tiempo real y aseguran que los líderes cuenten con botiquines de primer respondiente. En la montaña salimos juntos, nos cuidamos en la ruta y regresamos completos.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="about-card" style="text-align: center; border-left: 4px solid #FC4C02;">
        <p style="color: #64748B; font-size: 14px; margin: 0; font-style: italic;">"Subir una montaña no es solo alcanzar la cumbre, es asegurar la logística, respetar el entorno y certificar que todo el grupo regrese a salvo a casa."</p>
    </div>
    """, unsafe_allow_html=True)
    
    mostrar_developer_footer()