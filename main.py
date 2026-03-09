import streamlit as st
import analisis_ppmaximas as ana
import pandas as pd
import io
import calendar


# 1. Configuración de página (SIEMPRE debe ser lo primero que ve Streamlit)
st.set_page_config(
    page_title="MapLecture", 
    page_icon="💧", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Estilos personalizados (Paleta MapLecture)
st.markdown("""
    <style>

    /* === FORZAR TEMA CLARO COMPLETO (Windows/Mac/Linux) === */

    html, body, .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"], .main, .block-container {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div,
    [data-testid="stSidebarContent"] {
        background-color: #f0f7f4 !important;
        border-right: 1px solid #e0e0e0 !important;
        color: #1a1a1a !important;
        min-width: 250px !important;
        max-width: 300px !important;
    }

    [data-testid="stSidebarUserContent"] {
        padding-top: 0rem !important;
        margin-top: -1.5rem !important;
    }

    [data-testid="stSidebarUserContent"] .stMarkdown,
    [data-testid="stSidebarUserContent"] .stImage {
        margin-bottom: -10px;
    }

    /* Forzar color oscuro solo en texto de contenido, NO en gráficos */
    .stApp > header, .stApp > div > div > div > div,
    [data-testid="stMainBlockContainer"] p,
    [data-testid="stMainBlockContainer"] li,
    [data-testid="stMainBlockContainer"] span:not([class*="plotly"]),
    [data-testid="stMainBlockContainer"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] div {
        color: #1a1a1a !important;
    }

    /* Excepciones */
    a, [data-testid="stMarkdownContainer"] a { color: #1155cc !important; }

    /* Botones de acción */
    .stButton > button {
        background-color: #6db38a !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        border-radius: 6px !important;
    }
    .stButton > button:hover {
        background-color: #3d7a5a !important;
    }

    /* Botones de descarga */
    .stDownloadButton > button {
        background-color: #f4faf7 !important;
        color: #3d7a5a !important;
        border: 1.5px solid #6db38a !important;
        font-weight: 600 !important;
        border-radius: 6px !important;
    }
    .stDownloadButton > button:hover {
        background-color: #dff0ec !important;
    }

    /* Link buttons del sidebar */
    .stLinkButton > a {
        background-color: #dff0ec !important;
        color: #3d7a5a !important;
        border: 1.5px solid #b2d8c8 !important;
        font-weight: 600 !important;
        border-radius: 6px !important;
        text-decoration: none !important;
    }
    .stLinkButton > a:hover {
        background-color: #b2d8c8 !important;
        color: #2e4d31 !important;
    }
    h1, h2, h3,
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3 {
        color: #2e4d31 !important;
    }

    /* Tabs */
    .stTabs [aria-selected="true"] {
        color: #2e4d31 !important;
        border-bottom-color: #2e4d31 !important;
    }

    /* Métricas */
    [data-testid="stMetric"] { background-color: #ffffff !important; }
    [data-testid="stMetricValue"] { color: #1a1a1a !important; }
    [data-testid="stMetricLabel"] { color: #555555 !important; }

    /* Expanders */
    [data-testid="stExpander"],
    [data-testid="stExpander"] * { background-color: #ffffff !important; }

    /* Alertas / Info boxes */
    [data-testid="stAlert"] {
        background-color: #eef4ff !important;
        color: #1a1a1a !important;
    }

    /* File uploader */
    [data-testid="stFileUploader"],
    [data-testid="stFileUploaderDropzone"] {
        background-color: #f9f9f9 !important;
        padding-top: 0rem;
    }
    [data-testid="stFileUploaderDropzoneInstructions"] { display: none; }
    [data-testid="stFileUploaderDropzone"]::before {
        content: "📂 Arrastra aquí tus archivos .csv o .txt";
        display: block;
        text-align: center;
        padding: 20px;
        color: #1f77b4 !important;
        font-weight: bold;
    }
    [data-testid="stFileUploaderDropzone"] button { display: none; }

    /* Tamaño de fuente base */
    .stApp p, .stApp li, .stApp label,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li {
        font-size: 1rem !important;
        line-height: 1.6 !important;
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
    archivos = st.file_uploader("", type=['csv', 'txt'], accept_multiple_files=True)

     # 4. Sección de Apoyo (Esta puede estar fuera porque no depende de los datos)
    url_whatsapp = "https://wa.me/51986688805?text=Hola%20MapLecture,%20quiero%20apoyar%20el%20proyecto%20MapDrop"
    url_buymeacoffee = "https://buymeacoffee.com/maplecture"
    st.sidebar.subheader("☕ Apoya este proyecto")
    st.sidebar.write("Esta herramienta es gratuita. Si te sirvió, puedes apoyar su mantenimiento:")
    st.link_button("👉 Invítame un café (PayPal/Card)", url_buymeacoffee, use_container_width=True)
    st.link_button("👉 Donar por Yape/Plin (WhatsApp)", url_whatsapp, use_container_width=True)

    
# 5. Lógica de procesamiento
if archivos:
    # Obtenemos la metadata del primer archivo de la lista
    metadata = ana.extraer_info_estacion(archivos[0])
    
   # Mostramos el nombre real extraído
    st.markdown(f"## 📍 Estación: {metadata['Estación']}")
    
   # 3. Fila de información técnica
    col_dep, col_ubi = st.columns([1, 2])
    
    with col_dep:
        st.write(f"**Departamento:**\n\n{metadata['Departamento']}")
        
    with col_ubi:
        st.write(f"**Provincia / Distrito:**\n\n{metadata['Provincia']} / {metadata['Distrito']}")

    st.divider()

    # --- PROCESAMIENTO DE DATOS ---
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

        st.sidebar.caption(f"Versión 1.0 | Datos de {anio_inicio} a {anio_fin}")

        # Generación de Matriz y Pestañas
        df_matriz = ana.generar_matriz_maximos(df_todo)

        # --- HEADER PERSISTENTE ---
        st.markdown(
            "<div style='display:flex; align-items:center; gap:10px; margin-bottom:0.5rem;'>"
            "<span style='font-size:1.6rem;'>💧</span>"
            "<span style='font-size:1.4rem; font-weight:700; color:#3d7a5a; letter-spacing:1px;'>MapDrop</span>"
            "<span style='font-size:0.9rem; color:#888; margin-left:4px;'>| Procesamiento hidrometeorológico · MapLecture</span>"
            "</div>",
            unsafe_allow_html=True
        )
        st.markdown("<hr style='margin-top:0; margin-bottom:1rem; border-color:#dff0ec;'>", unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs(["🕵️ Validación de datos", "📅 Estadística de datos", "📈 Análisis Visual de datos"])
        
        with tab1:
            st.subheader("🕵️ Valida los datos cargados")
            st.write("Si ves casillas en rojo significa que hay días del mes que no tienen registro, es importante que lo verifiques pues podría afectar la precisión del análisis .")

            # Llamamos a la nueva función
            df_validacion = ana.generar_resumen_validacion(df_todo)
            
            # Aplicamos un estilo visual: Rojo si faltan muchos días, Verde si está completo
            
            def destacar_faltantes(row):
                # Crear una lista de estilos vacíos del mismo largo que la fila
                styles = [''] * len(row)
                
                # El nombre de la fila suele ser el Año si es el índice
                try:
                    anio = int(row.name)
                except (ValueError, TypeError):
                    anio = 2024  # Año por defecto si hay error
                
                # Lista de meses para comparar (ajusta según tus columnas)
                meses_dict = {
                    'Ene': 1, 'Feb': 2, 'Marz': 3, 'Abr': 4, 'May': 5, 'Jun': 6,
                    'Jul': 7, 'Ago': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dic': 12
                }

                for i, (col_nombre, valor) in enumerate(row.items()):
                    if col_nombre in meses_dict:
                        mes_num = meses_dict[col_nombre]
                        # Obtener días exactos del mes/año (considera bisiestos)
                        dias_reales = calendar.monthrange(anio, mes_num)[1]
                        
                        # Si faltan días (es mayor a 0 pero menor al total del mes)
                        if valor < dias_reales:
                            styles[i] = 'background-color: #ffcccc; color: #842029'
                            
                return styles

            st.dataframe(df_validacion.style.apply(destacar_faltantes, axis=1), use_container_width=True)
       
           # --- NUEVA SECCIÓN DE DESCARGA (Reemplaza la visualización de datos) ---
            st.subheader("📥 Exportar datos")
            st.write("Descarga la serie completa de datos diarios procesados en formato Excel.")
            
            # Preparar el archivo Excel en memoria
            buffer_datos = io.BytesIO()
            with pd.ExcelWriter(buffer_datos, engine='xlsxwriter') as writer:
                df_todo.to_excel(writer, index=False, sheet_name='Datos_Diarios')
            buffer_datos.seek(0)
            
            st.download_button(
                label="Excel de Datos Diarios",
                data=buffer_datos.getvalue(),
                file_name=f"Datos_Diarios_{metadata['Estación']}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                icon="📊"
            )

        with tab2:
            st.subheader("📅 Estadística de Precipitaciones Máximas")
            st.markdown("""
            Esta matriz presenta los valores de **precipitación máxima de 24 horas** registrados en cada mes. 
                        
            **¿Para qué sirve esta información?**
            * **Identificación de Eventos Extremos:** Permite detectar los años con tormentas excepcionales (como años de El Niño).
            * **Ingeniería y Diseño:** Es el insumo principal para calcular caudales de diseño en cunetas, alcantarillas y defensas ribereñas.
            * **Gestión del Riesgo (EVAR):** Ayuda a determinar periodos de retorno y la probabilidad de ocurrencia de inundaciones o activaciones de quebradas.
            """)
            st.markdown(f"""**Para la Estación: {metadata['Estación']}**""")

            # --- CÁLCULOS ESTADÍSTICOS HISTÓRICOS ---
            # 1. Precipitación Máxima Absoluta y su fecha
            max_val = df_todo['pp'].max()
            idx_max = df_todo['pp'].idxmax()
            
            # Buscamos la columna de fecha (puede ser 'fecha', 'Fecha' o construida)
            col_fecha = next((c for c in df_todo.columns if c.lower() == 'fecha'), None)
            
            if col_fecha:
                fecha_obj = df_todo.loc[idx_max, col_fecha]
                # Si es string, no tiene .strftime, si es datetime sí
                try:
                    fecha_max_str = fecha_obj.strftime('%d/%m/%Y')
                except (AttributeError, ValueError):
                    fecha_max_str = str(fecha_obj)
            else:
                # Si no hay columna fecha, la armamos con año-mes-dia si existen
                try:
                    d = df_todo.loc[idx_max]
                    fecha_max_str = f"{int(d['dia'])}/{int(d['mes'])}/{int(d['año'])}"
                except (KeyError, ValueError, TypeError):
                    fecha_max_str = "No disponible"

            # 2. Precipitación Media Anual (Suma de cada año, luego promedio de esas sumas)
            lluvia_anual_total = df_todo.groupby('año')['pp'].sum()
            promedio_anual = lluvia_anual_total.mean()

            # 3. Precipitación Media Diaria (de toda la serie)
            media_diaria = df_todo['pp'].mean()

            # --- PANEL DE MÉTRICAS ---
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric(
                    label="Máxima Histórica", 
                    value=f"{max_val} mm",
                    help="Es el valor de precipitación más alto registrado en un solo día (24 horas) en toda la historia de la estación. Representa el evento extremo más severo detectado."
                )
                st.caption(f"Fecha: {fecha_max_str}")
                
            with m2:
                st.metric(
                    label="P. Media Anual", 
                    value=f"{promedio_anual:.2f} mm",
                    help="Es el promedio de la suma total de lluvia de cada año. Indica cuánta precipitación se espera que caiga en la estación durante un año completo normal."
                )
                st.caption("Total anual promedio")
                
            with m3:
                st.metric(
                    label="P. Media Diaria", 
                    value=f"{media_diaria:.2f} mm",
                    help="Es el promedio matemático de todos los registros diarios de la serie, incluyendo los días en que no llovió (0 mm). Refleja la intensidad diaria habitual."
                )
                st.caption("Promedio de todos los días")

            st.markdown("---")
            st.caption(
                "📚 **Fuente metodológica:** Chow et al. (1994) *Hidrología Aplicada*; WMO-No.168 (2009). "
                "Los valores presentados corresponden a estadísticos descriptivos de la serie cargada. "
                "Para análisis de períodos de retorno se recomienda complementar con distribuciones probabilísticas (Gumbel, Log-Pearson III)."
            )
            
            # --- MATRIZ Y DESCARGA ---
            st.markdown("### 📥 Precipitaciones Máximas Mensuales")
            st.write("Haz clic en el botón de abajo para obtener la matriz completa en formato Excel.")
            
            # Preparamos el Excel de la Matriz
            tobol = io.BytesIO()
            with pd.ExcelWriter(tobol, engine='xlsxwriter') as writer:
                df_matriz.to_excel(writer, index=True, sheet_name='Matriz_PP_Max')
            tobol.seek(0)
            
            st.download_button(
                label="📗 Descargar tabla de Precipitaciones Máximas (.xlsx)",
                data=tobol.getvalue(),
                file_name=f"Matriz_PP_Max_{metadata['Estación']}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True # Botón grande y profesional
            )

            # --- VISTA OPCIONAL (Por transparencia técnica) ---
            with st.expander("🔍 Ver tabla de datos (Opcional)"):
                st.write("Esta tabla te permite una visualización rápida de los datos.")
                st.dataframe(df_matriz, use_container_width=True)
            
        with tab3:
            st.subheader("📈 Descripción Estadística")
            # --- TEXTO INTRODUCTORIO Y OBJETIVO ---
            st.markdown(f"""
            ### **Estación: {metadata['Estación']}**
            
            Estos gráficos permiten:
            
            1. **Visualizar la Variabilidad:** Observar rápidamente qué tan extremas han sido las lluvias en comparación con el promedio histórico.
            2. **Detectar Tendencias:** Identificar si la intensidad de las tormentas está aumentando con el paso de los años.
            3. **Análisis de Riesgo:** Localizar visualmente los meses con mayores picos de precipitación, lo cual es vital para la planificación de contingencias ante activaciones de quebradas o inundaciones.
            """)

            # --- DISCLAIMER ---
            st.warning(
                "⚠️ **Aviso importante sobre la interpretación de los umbrales**\n\n"
                "Los umbrales de riesgo mostrados en esta herramienta se calculan de forma **estadística y relativa**, "
                "utilizando los percentiles 50 y 90 de la propia serie de datos cargada. "
                "Esto significa que **series cortas (menos de 15-20 años) pueden subestimar o sobreestimar "
                "los umbrales reales de criticidad** de una localidad.\n\n"
                "Por ejemplo, una serie de 9 años podría arrojar un umbral crítico de 150 mm, "
                "cuando en la realidad local eventos desde 100 mm ya generan riesgo. "
                "**Los resultados de esta herramienta son de carácter orientativo y exploratorio. "
                "Siempre deben ser validados y contrastados con profesionales en hidrología, "
                "gestión de riesgos o ingeniería hidráulica antes de usarse en decisiones técnicas o de planificación.**"
            )

            # --- METODOLOGÍA (expander con icono) ---
            with st.expander("📐 ¿Cómo se calculan los umbrales? — Metodología"):
                st.markdown(
"**Método utilizado: Percentiles empíricos sobre la serie histórica**\n\n"
"MapDrop calcula dos umbrales de referencia a partir de la serie de máximas anuales de precipitación:\n\n"
"* **Umbral Normal (Percentil 50 — Mediana):** El 50% de los años registraron una precipitación máxima anual igual o inferior a este valor. Representa el comportamiento habitual de la estación.\n"
"* **Umbral Crítico (Percentil 90):** Solo el 10% de los años superaron este valor. Se interpreta como un evento de baja frecuencia y alta energía, con potencial de generar daños.\n\n"
"**Limitaciones conocidas del método:**\n"
"* Con series menores a 15 años, los percentiles son estadísticamente inestables.\n"
"* El método no reemplaza el análisis de frecuencias con distribuciones probabilísticas (Gumbel, Log-Pearson III, GEV) que permiten estimar períodos de retorno formales.\n"
"* No incorpora información fisiográfica ni de uso de suelo que puede modificar la criticidad real.\n\n"
"**Referencias bibliográficas:**\n"
"* Chow, V. T., Maidment, D. R., & Mays, L. W. (1994). *Hidrología Aplicada*. McGraw-Hill.\n"
"* Ven Te Chow (1964). *Handbook of Applied Hydrology*. McGraw-Hill.\n"
"* WMO (2009). *Guide to Hydrological Practices, Vol. II* (WMO-No. 168). World Meteorological Organization.\n"
"* SENAMHI Perú (2023). *Guía de uso de datos hidrometeorológicos*. Lima, Perú. [senamhi.gob.pe](https://www.senamhi.gob.pe)\n"
"* Kite, G. W. (1977). *Frequency and Risk Analyses in Hydrology*. Water Resources Publications."
                )

            st.divider()
            
        # 1. Generamos el gráfico y obtenemos los umbrales calculados
            f1_dinamico, umbral_medio, umbral_alto = ana.grafico_pp_max_anual(df_todo)
                
         # 2. Otros cálculos para el texto
            max_historico = df_todo['pp'].max()
            anio_max = df_todo.loc[df_todo['pp'].idxmax(), 'año']
            veces_promedio = max_historico / umbral_medio if umbral_medio > 0 else 0
            eventos_criticos = len(df_todo[df_todo['pp'] > umbral_alto])

                # --- Tendencia ---
            st.write(f"### Máximas Precipitaciones Anuales entre {anio_inicio} al {anio_fin}")
            st.info(f"""
                Este análisis se basa en el comportamiento histórico de la estación **{metadata['Estación']}**:
                
                * **Normalidad:** El 50% de los años, la lluvia máxima no supera los **{umbral_medio:.1f} mm**.
                * **Riesgo Local:** Valores sobre **{umbral_alto:.1f} mm** se consideran extremos para esta zona.
                * **Evento Crítico:** El récord de **{max_historico:.1f} mm** (año {int(anio_max)}) superó en **{veces_promedio:.1f} veces** lo habitual.
                * **Frecuencia:** Se han registrado **{eventos_criticos} eventos** en **umbral alto** en esta serie (superando el Percentil 90).
                * Esto ayuda a entender qué tan recurrentes son las lluvias extremas para la estación **{metadata['Estación']}**.
                """)
            st.plotly_chart(f1_dinamico, use_container_width=True)
            
            st.divider()

                            # --- BOXPLOT---
            st.write(f"### Variabilidad Mensual entre {anio_inicio} al {anio_fin}")
            f2_boxplot, mes_habitual = ana.grafico_boxplot(df_todo)

            st.info(f"""
                Este Análisis permite visualizar la variabilidad estacional de las lluvias, identificando qué meses presentan los mayores rangos de precipitación y cuáles registran eventos excepcionales (puntos fuera de la caja) que rompen el comportamiento normal de la estación 
                * **Periodo Crítico:** Históricamente, **{mes_habitual}** es el mes con mayor recurrencia de lluvias significativas en esta zona.
                * **Eventos Atípicos (Outliers):** Los puntos aislados sobre las cajas representan lluvias que rompieron el **umbral normal** de ese mes.
                * Esta dispersión ayuda a definir los meses de mayor exposición para la planificación de obras de prevención.
                """)
            
            st.plotly_chart(f2_boxplot, use_container_width=True)

            st.divider()


            # 1. Generamos el gráfico
            f3_hist, intensidad_media = ana.grafico_histograma(df_todo)
                
            st.write("### Frecuencia de Intensidades")
            st.info(f"""
                Este gráfico muestra cuántas veces se repiten diferentes intensidades de lluvia, permitiendo identificar si la zona tiende a registrar eventos leves frecuentes o si tiene una alta incidencia de tormentas severas.
                * **Intensidad Promedio:** Cuando llueve en esta estación, el promedio de descarga es de **{intensidad_media:.1f} mm/día**.
                * **Análisis de Cola:** Los bloques hacia la derecha representan eventos de baja frecuencia pero alta energía, fundamentales para el cálculo de caudales de diseño en **EVAR**.
                """)
            
                # 3. Renderizado
            st.plotly_chart(f3_hist, use_container_width=True)
                
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
        st.markdown("<h3 style='color:#2e4d31; font-size:1.4rem;'>¿Qué hace MapDrop?</h3>", unsafe_allow_html=True)
        st.markdown("Es una herramienta diseñada por **MapLecture** para automatizar la gestión de datos del SENAMHI:")
        st.markdown("* **Estandarización:** Convierte archivos TXT y CSV convencionales a un formato limpio.")
        st.markdown("* **Cálculo Automático:** Genera matrices de precipitaciones máximas mensuales y diarias al instante.")
        st.markdown("* **Auditoría:** Evalúa la calidad de tu serie de datos mediante semáforos de completitud.")

    with col2:
        st.markdown("<h3 style='color:#2e4d31; font-size:1.4rem;'>¿Cómo usarla?</h3>", unsafe_allow_html=True)
        st.markdown("1. **Prepara tus archivos:** Ten a la mano tus descargas del **SENAMHI**. Puedes obtener datos desde:")
        st.markdown("   * [Web de Datos Hidrometeorológicos (Convencionales)](https://www.senamhi.gob.pe/site/descarga-datos/)")
        st.markdown("   * [Buscador de Estaciones (Histórico)](https://www.senamhi.gob.pe/?p=estaciones)")
        st.markdown("2. **Carga los datos:** Usa el panel lateral izquierdo para arrastrar uno o varios archivos.")
        st.markdown("3. **Analiza:** Navega por las pestañas para ver la matriz, los gráficos y la validación.")
        st.markdown("4. **Descarga:** Exporta tus resultados directamente a Excel o CSV.")

    st.markdown("---")
    st.info("👈 **Comienza ahora:** Sube tus archivos en la barra lateral para activar el análisis.")