# 🏔️ México Al Aire Libre

<p align="center">
  <img src="https://img.shields.io/badge/UI_Style-Strava_Orange-FC4C02?style=for-the-badge" alt="Estilo Strava">
  <img src="https://img.shields.io/badge/Database-Supabase-3ECF8E?style=for-the-badge&logo=supabase" alt="Supabase">
  <img src="https://img.shields.io/badge/Framework-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit" alt="Streamlit">
</p>

<p align="center">
  <strong><i>Construyendo la red comunitaria de montañismo más grande de México.</i></strong>
</p>

---

## 🎯 Propósito del Proyecto

**México Al Aire Libre** es una plataforma web e interfaz móvil de código abierto diseñada para democratizar el acceso al montañismo, trail running y senderismo técnico en México. El sistema actúa como un puente directo y transparente entre entusiastas del deporte al aire libre y guías o comités organizadores locales, eliminando intermediarios y centralizando la logística de expediciones de forma segura y ordenada.

El diseño del ecosistema prioriza la comodidad del usuario en entornos de alta montaña o exteriores mediante una interfaz luminosa (*Light Mode Premium*) inspirada en la sinergia visual de plataformas de rendimiento deportivo como **Strava**.

---

## ✨ Características Principales

* **📅 Agenda Cronológica Avanzada:** Clasificación y renderizado dinámico en orden cronológico ascendente de las próximas expediciones, separando eventos futuros de históricos de forma automática.
* **🗺️ Mapa Base de Expediciones Activas:** Visualización geoespacial interactiva impulsada por `pydeck` (ScatterplotLayer) acoplada a un mapa base de carreteras, optimizada con *tooltips* responsivos y auto-ajustables para pantallas móviles.
* **📌 Motor de Búsqueda:** Filtrado reactivo en tiempo real de rutas, cumbres o distancias mediante consultas cruzadas sobre los campos de título y descripción.
* **💬 Integración Directa (One-Click Booking):** Generación dinámica de enlaces con codificación URL para la apertura directa de hilos de conversación en WhatsApp con los líderes del evento.
* **🛡️ Arquitectura Serverless:** Conexión segura, asíncrona y optimizada mediante caché a una base de datos relacional remota.

---

## 💻 Stack Tecnológico

* **Frontend & Reactividad:** [Streamlit](https://streamlit.io/) (Framework de python para aplicaciones de datos).
* **Base de Datos Relacional:** [Supabase](https://supabase.com/) (PostgreSQL administrado con persistencia en la nube).
* **Visualización Geoespacial:** [PyDeck](https://deckgl.readthedocs.io/) (Renderizado de capas WebGL de alta densidad).
* **Procesamiento de Datos:** [Pandas](https://pandas.pydata.org/) (Estructuración de vectores de coordenadas).
* **Estilos e Inyección de UI:** CSS3 avanzado inyectado en el DOM nativo de Streamlit.

---

## 🗄️ Arquitectura de la Base de Datos

La información del backend reside en una tabla relacional dentro de Supabase denominada `eventos_montana`. A continuación se detalla su esquema técnico de datos:

| Campo | Tipo de Datos | Descripción |
| :--- | :--- | :--- |
| `id` | `BIGINT (Primary Key)` | Identificador único incremental del evento. |
| `titulo` | `VARCHAR / TEXT` | Nombre oficial de la cumbre, carrera o trail. |
| `organizador` | `VARCHAR / TEXT` | Nombre de la entidad, guía o club organizador. |
| `fecha` | `DATE (YYYY-MM-DD)` | Fecha programada del evento (formato ISO). |
| `descripcion` | `TEXT` | Itinerario completo, requerimientos de seguridad y detalles técnicos. |
| `telefono_whatsapp` | `VARCHAR` | Número de contacto internacional para el enlace dinámico. |
| `latitud` | `NUMERIC / FLOAT` | Coordenada decimal geográfica (Latitud). |
| `longitud` | `NUMERIC / FLOAT` | Coordenada decimal geográfica (Longitud). |

---

## 🛠️ Instalación y Configuración Local

Sigue estos pasos para clonar el repositorio y ejecutar el entorno de desarrollo local:

### 1. Clonar el repositorio
```bash
git clone [https://github.com/TU_USUARIO/mexico-al-aire-libre.git](https://github.com/TU_USUARIO/mexico-al-aire-libre.git)
cd mexico-al-aire-libre
