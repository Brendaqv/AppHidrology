import streamlit as st
import analisis_ppmaximas as ana
import pandas as pd
import io

# 1. Configuración de página (SIEMPRE debe ser lo primero que ve Streamlit)
st.set_page_config(page_title="MapLecture", page_icon="💧", layout="wide")

# 2. Estilos personalizados (Paleta MapLecture)
st.markdown("""
    <style>
    /* Fondo principal */
    .stApp {
        background-color: #ffffff;
    }
    
    /* Sidebar con tono menta suave */
    [data-testid="stSidebar"] {
        background-color: #f0f7f4;
        border-right: 1px solid #e0e0e0;
    }

    /* Títulos y Botones */
    h1, h2, h3 {
        color: #2e4d31 !important; /* Verde oscuro del logo */
    }
    
    .stButton>button {
        background-color: #4CAF50 !important;
        color: white !important;
        border: none;
        font-weight: bold;
    }
    
    /* Ajuste de márgenes del sidebar solicitado anteriormente */
    [data-testid="stSidebarUserContent"] {
        padding-top: 0rem !important;
        margin-top: -1.5rem !important;
    }
    </style>
    """, unsafe_allow_html=True)


# 3. Barra Lateral - Parte Superior
with st.sidebar:
    # Cargar el logo local (Asegúrate de que el archivo se llame LOGO.jpg en tu carpeta)
    st.image("LOGO.jpg", use_container_width=True)
    st.caption("<p style='text-align: center; color: gray; font-size: 0.8rem; margin-top: -5px'>Educación y Geografía Aplicada</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Subidor de archivos
    archivos = st.sidebar.file_uploader("", type=['csv', 'txt'], accept_multiple_files=True)

    # Nuevo intento de personalización CSS
    st.markdown("""
        <style>
        /* 1. Oculta el texto original en inglés (instrucciones pequeñas) */
        [data-testid="stFileUploaderDropzoneInstructions"] {
            display: none;
        }
        /* 2. Inserta tu propio texto en español */
        [data-testid="stFileUploaderDropzone"]::before {
            content: "📂 Arrastra aquí tus archivos .csv o .txt";
            display: block;
            text-align: center;
            padding: 20px;
            color: #1f77b4; /* Azul profesional */
            font-weight: bold;
        }

        /* 3. Oculta el botón gris original 'Browse files' para que no estorbe */
        [data-testid="stFileUploaderDropzone"] button {
            display: none;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("""
        <style>
        /* 1. Reduce el margen superior del PANEL LATERAL */
        [data-testid="stSidebarUserContent"] {
            padding-top: 0rem !important; /* Ajusta este valor a 0 si lo quieres aún más arriba */
        }

        /* 2. Opcional: Reduce el espacio entre elementos dentro del sidebar */
        [data-testid="stSidebarUserContent"] .stMarkdown, 
        [data-testid="stSidebarUserContent"] .stImage {
            margin-bottom: -10px;
        }

        /* 3. Estilo para el cargador de archivos dentro del sidebar para que sea más denso */
        [data-testid="stFileUploader"] {
            padding-top: 0rem;
        }
        
        /* 4. Ajustar el ancho del sidebar para que no ocupe tanto espacio horizontal */
        [data-testid="stSidebar"] {
            min-width: 250px;
            max-width: 300px;
        }
        </style>
        """, unsafe_allow_html=True)

    # 4. Sección de Apoyo (Esta puede estar fuera porque no depende de los datos)
    st.sidebar.subheader("☕ Apoya este proyecto")
    st.sidebar.write("Esta herramienta es gratuita. Si te sirvió, puedes apoyar su mantenimiento:")
    st.sidebar.markdown("[👉 Invítame un café (PayPal/Card)](https://www.buymeacoffee.com/tu_usuario)")
    st.sidebar.info("📱 Yape/Plin: **9XX XXX XXX**")

# 5. Lógica de procesamiento
if archivos:
    df_todo = ana.procesar_archivos(archivos)
    
    if df_todo is not None:
        # AQUÍ calculamos los años (ahora sí existen)
        anio_inicio = int(df_todo['año'].min())
        anio_fin = int(df_todo['año'].max())
        total_anios = anio_fin - anio_inicio + 1
        
        # --- SECCIÓN DE CRÉDITOS (Movida aquí adentro para que no dé error) ---
        st.sidebar.markdown("---")
        st.sidebar.subheader("🛠️ Desarrollo y Autoría")
        st.sidebar.write(f"""
        **Autora:** Brenda Quiroz 
        **Idea Original:** Análisis de Precipitaciones.  
        **Colaboración:** Desarrollado con el apoyo de IA (Gemini).
        """)

        if 'df_todo' in locals():
            st.sidebar.caption(f"Versión 1.0 | Datos de {anio_inicio} a {anio_fin}")
        else:
            st.sidebar.caption("Versión 1.0 | Esperando datos...")

        # Generación de Matriz y Pestañas
        df_matriz = ana.generar_matriz_maximos(df_todo)
        tab1, tab2, tab3 = st.tabs(["📅 Matriz Mensual", "📄 Datos Diarios", "📈 Gráficos Estadísticos"])
        
        with tab1:
            st.subheader("🕵️ Resumen de Consistencia de Datos")
            st.write("Esta tabla muestra la **cantidad de días registrados** por cada mes. ")
            
            # Llamamos a la nueva función
            df_validacion = ana.generar_resumen_validacion(df_todo)
            
            # Aplicamos un estilo visual: Rojo si faltan muchos días, Verde si está completo
            def destacar_faltantes(val):
                color = 'background-color: #ffcccc' if val < 28 and val > 0 else ''
                return color

            st.dataframe(df_validacion.style.applymap(destacar_faltantes), use_container_width=True)
            
            st.warning("⚠️ **Nota:** Los meses con menos de 28-31 días (marcados en rojo) podrían afectar la precisión de los máximos anuales.")
            st.subheader("Matriz de Precipitaciones Máximas Mensuales")
            st.dataframe(df_matriz, use_container_width=True)
            tobol = io.BytesIO()
            df_matriz.to_excel(tobol, index=True)
            st.download_button("📗 Descargar Matriz Excel", data=tobol.getvalue(), file_name="Matriz_PP.xlsx")
            
        with tab2:
            st.subheader("Compendio de Datos Diarios Unificados")
            st.dataframe(df_todo, use_container_width=True)
            
        with tab3:
            st.header("📈 ¿Cómo leer estos resultados?")
            st.info("Utiliza estos paneles para entender el comportamiento de las lluvias.")

            max_valor = df_todo['pp'].max()
            mes_peligro_num = df_todo.loc[df_todo['pp'].idxmax(), 'mes']
            meses_nombres = {1:'Enero', 2:'Febrero', 3:'Marzo', 4:'Abril', 5:'Mayo', 6:'Junio',
                             7:'Julio', 8:'Agosto', 9:'Septiembre', 10:'Octubre', 11:'Noviembre', 12:'Diciembre'}
            mes_nombre_max = meses_nombres[mes_peligro_num]

            f1, f2, f3, f4 = ana.generar_graficos(df_todo)

            col1, col2 = st.columns(2)
            with col1:
                with st.expander("🔍 EXPLICACIÓN: El historial de tormentas"):
                    st.write(f"Muestra la lluvia más fuerte de cada año desde {anio_inicio} hasta {anio_fin}.")
                st.plotly_chart(f1, use_container_width=True)

            with col2:
                with st.expander("🔍 EXPLICACIÓN: Los meses de mayor riesgo"):
                    st.write(f"Récord histórico en {total_anios} años: {max_valor} mm en {mes_nombre_max}.")
                st.plotly_chart(f2, use_container_width=True)
            
            col3, col4 = st.columns(2)
            with col3: st.plotly_chart(f3, use_container_width=True)
            with col4: st.plotly_chart(f4, use_container_width=True)
    else:
        st.error("No se pudieron procesar los archivos.")
else:
    # 1. Título con diseño limpio
    st.markdown("<h1 style='text-align: center; margin-top: -2rem;'>💧 MapDrop</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray; font-size: 1.2rem;'>Procesamiento inteligente de datos hidrometeorológicos</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 2. Columnas para explicar "Qué hace" y "Cómo usarla"
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### ¿Qué hace MapDrop?
        Es una herramienta diseñada por **MapLecture** para automatizar la gestión de datos del SENAMHI:
        * **Estandarización:** Convierte archivos TXT y CSV convencionales a un formato limpio.
        * **Cálculo Automático:** Genera matrices de precipitaciones máximas mensuales y diarias al instante.
        * **Auditoría:** Evalúa la calidad de tu serie de datos mediante semáforos de completitud.
        """)

    with col2:
        st.markdown("""
        ### ¿Cómo usarla?
        1. **Prepara tus archivos:** Ten a la mano tus descargas del **SENAMHI**. Puedes obtener datos desde:
        * [Web de Datos Hidrometeorológicos (Convencionales)](https://www.senamhi.gob.pe/site/descarga-datos/).
        * [Buscador de Estaciones (Histórico)](https://www.senamhi.gob.pe/?p=estaciones).
        2. **Carga los datos:** Usa el panel lateral izquierdo para arrastrar uno o varios archivos.
        3. **Analiza:** Navega por las pestañas para ver la matriz, los gráficos y la validación.
        4. **Descarga:** Exporta tus resultados directamente a Excel o CSV.
        """)

    st.markdown("---")
    st.info("👈 **Comienza ahora:** Sube tus archivos en la barra lateral para activar el análisis.")