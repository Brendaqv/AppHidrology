import pandas as pd
import io
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Layout base reutilizable para todos los gráficos
BASE_LAYOUT = dict(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial, sans-serif", size=14, color="#1a1a1a"),
    xaxis=dict(
        showgrid=True, gridcolor='#eeeeee', linecolor='#cccccc',
        tickfont=dict(size=13, color="#1a1a1a"),
        title_font=dict(size=14, color="#1a1a1a")
    ),
    yaxis=dict(
        showgrid=True, gridcolor='#eeeeee', linecolor='#cccccc',
        tickfont=dict(size=13, color="#1a1a1a"),
        title_font=dict(size=14, color="#1a1a1a")
    ),
    margin=dict(l=60, r=40, t=50, b=60),
    hoverlabel=dict(bgcolor="white", font_size=13, font_family="Arial"),
)

def procesar_archivos(lista_archivos_subidos):
    lista_df = []
    for archivo in lista_archivos_subidos:
        try:
            nombre = archivo.name.lower()
            # LECTURA DEL TXT
            if nombre.endswith('.txt'):
                contenido = archivo.read().decode('utf-8')
                lineas_limpias = [l.strip() for l in contenido.split('\n') if l.strip()]
                df = pd.read_csv(io.StringIO('\n'.join(lineas_limpias)), sep=r'\s+', header=None)
                df = df.iloc[:, [0, 1, 2, 3]]
                df.columns = ['año', 'mes', 'dia', 'pp']
                archivo.seek(0)
            # LECTURA DEL CSV
            else:
                df = pd.read_csv(archivo, skiprows=7, header=None)
                df = df.iloc[:, [0, 4]]
                df.columns = ['fecha_full', 'pp']
                df['fecha_full'] = pd.to_datetime(df['fecha_full'], errors='coerce')
                df['año'] = df['fecha_full'].dt.year
                df['mes'] = df['fecha_full'].dt.month
                df['dia'] = df['fecha_full'].dt.day
                df = df[['año', 'mes', 'dia', 'pp']]

            # LIMPIEZA
            df['pp'] = df['pp'].astype(str).str.upper().replace('S/D', '0').replace('T', '0.05')
            df['pp'] = pd.to_numeric(df['pp'], errors='coerce').fillna(0)
            df.loc[df['pp'] < 0, 'pp'] = 0
            df = df.dropna(subset=['año', 'mes'])
            df[['año', 'mes', 'dia']] = df[['año', 'mes', 'dia']].astype(int)
            lista_df.append(df)
        except Exception as e:
            print(f"Error en {archivo.name}: {e}")

    if not lista_df: return None
    res = pd.concat(lista_df, ignore_index=True).drop_duplicates(subset=['año', 'mes', 'dia'])
    return res.sort_values(by=['año', 'mes', 'dia']).reset_index(drop=True)

def generar_matriz_maximos(df):
    if df is None or df.empty: return None
    df_max = df.groupby(['año', 'mes'])['pp'].max().reset_index()
    matriz = df_max.pivot(index='año', columns='mes', values='pp')
    meses = {1:'Ene', 2:'Feb', 3:'Mar', 4:'Abr', 5:'May', 6:'Jun',
             7:'Jul', 8:'Ago', 9:'Set', 10:'Oct', 11:'Nov', 12:'Dic'}
    return matriz.rename(columns=meses)

def generar_graficos(df):
    if df is None or df.empty: return None, None, None, None
    
    # 1. Gráfico de Tendencia (Línea)
    df_anual = df.groupby('año')['pp'].max().reset_index()
    fig_linea = px.line(df_anual, x='año', y='pp', title='📈 Máximas Precipitaciones Anuales (Histórico)',
                        markers=True, labels={'pp':'PP Máx (mm)', 'año':'Año'})
    fig_linea.update_layout(**BASE_LAYOUT)
    
    # 2. Boxplot Mensual (Estacionalidad)
    meses_nombres = {1:'Ene', 2:'Feb', 3:'Mar', 4:'Abr', 5:'May', 6:'Jun',
                     7:'Jul', 8:'Ago', 9:'Set', 10:'Oct', 11:'Nov', 12:'Dic'}
    df_plot = df.copy()
    df_plot['Nombre Mes'] = df_plot['mes'].map(meses_nombres)
    fig_box = px.box(df_plot, x='Nombre Mes', y='pp', title='📊 Variabilidad Estacional de Lluvias (Boxplot)',
                     category_orders={"Nombre Mes": list(meses_nombres.values())},
                     color='Nombre Mes', labels={'pp':'Lluvia (mm)'})
    fig_box.update_layout(**BASE_LAYOUT)
    
    # 3. Histograma de Frecuencias (Distribución)
    fig_hist = px.histogram(df[df['pp'] > 0], x='pp', nbins=50, 
                            title='📉 Distribución de Frecuencias (¿Cuántas veces llueve X cantidad?)',
                            labels={'pp':'Precipitación (mm)', 'count':'Frecuencia (Días)'},
                            color_discrete_sequence=['#00CC96'])
    fig_hist.update_layout(**BASE_LAYOUT)

    # 4. Gráfico de Dispersión Temporal (Todos los datos)
    fig_scatter = px.scatter(df, x='año', y='pp', color='mes',
                             title='☁️ Dispersión Histórica de Eventos Diarios',
                             labels={'pp':'Lluvia Diaria (mm)', 'año':'Año'},
                             color_continuous_scale=px.colors.sequential.Viridis)
    fig_scatter.update_layout(**BASE_LAYOUT)
    
    return fig_linea, fig_box, fig_hist, fig_scatter

def generar_resumen_validacion(df):
    resumen = df.groupby(['año', 'mes']).size().unstack(fill_value=0)
    meses_nombres = {1:'Ene', 2:'Feb', 3:'Mar', 4:'Abr', 5:'May', 6:'Jun',
                     7:'Jul', 8:'Ago', 9:'Set', 10:'Oct', 11:'Nov', 12:'Dic'}
    resumen = resumen.rename(columns=meses_nombres)
    return resumen

def extraer_info_estacion(archivo):
    info = {
        "Estación": "NO ENCONTRADA", 
        "Departamento": "N/A", 
        "Provincia": "N/A", 
        "Distrito": "N/A", 
        "Código": "N/A",
        "Tipo": "N/A"
    }
    
    try:
        archivo.seek(0)
        contenido = archivo.getvalue().decode('latin-1').splitlines()
        
        for linea in contenido[:40]:
            partes = [p.strip() for p in linea.split(',')]
            
            for i, fragmento in enumerate(partes):
                f_up = fragmento.upper()
                
                if "DEPARTAMENTO" in f_up and (i + 1) < len(partes):
                    info["Departamento"] = partes[i+1].replace(':', '').strip().upper()
                
                elif "PROVINCIA" in f_up and (i + 1) < len(partes):
                    info["Provincia"] = partes[i+1].replace(':', '').strip().upper()
                
                elif "DISTRITO" in f_up and (i + 1) < len(partes):
                    info["Distrito"] = partes[i+1].replace(':', '').strip().upper()
                
                elif "CODIGO" in f_up or "CÓDIGO" in f_up:
                    info["Código"] = partes[i+1].replace(':', '').strip()

                elif "TIPO" in f_up and (i + 1) < len(partes):
                    info["Tipo de estación"] = partes[i+1].replace(':','').strip().upper()
                
                elif "ESTACI" in f_up or "ESTACIÓN" in f_up:
                    if ":" in fragmento:
                        info["Estación"] = fragmento.split(":")[-1].strip().upper()
                    elif (i + 1) < len(partes):
                        info["Estación"] = partes[i+1].replace(':', '').strip().upper()

        archivo.seek(0)
    except Exception:
        archivo.seek(0)
        
    return info

def grafico_pp_max_anual(df):
    if df is None or df.empty: 
        return None, 0, 0
    
    df_anual = df.groupby('año')['pp'].max().reset_index()
    
    u_medio = df_anual['pp'].quantile(0.50)
    u_alto = df_anual['pp'].quantile(0.90)
    
    colores = [
        '#e74c3c' if v > u_alto else '#f1c40f' if v > u_medio else '#2ecc71' 
        for v in df_anual['pp']
    ]

    fig = go.Figure()

    fig.add_hline(
        y=u_alto, 
        line_dash="dash", 
        line_color="red", 
        annotation_text=f"Umbral Crítico (> {u_alto:.1f} mm)",
        annotation_position="top left",
        annotation_font=dict(size=13, color="red")
    )

    fig.add_trace(go.Scatter(
        x=df_anual['año'], 
        y=df_anual['pp'],
        mode='lines+markers',
        line=dict(color='rgba(150, 150, 150, 0.3)', width=1),
        marker=dict(size=10, color=colores, line=dict(width=1, color='DarkSlateGrey')),
        name="Máxima Anual",
        hovertemplate="<b>Año: %{x}</b><br>Precipitación: %{y} mm<extra></extra>"
    ))

    fig.update_layout(
        **BASE_LAYOUT,
        xaxis_title="Año",
        yaxis_title="PP Máx (mm)",
        hovermode="x"
    )

    return fig, u_medio, u_alto

def grafico_boxplot(df):
    if df is None or df.empty: return None, "N/A"
    
    meses_nombres = {1:'Ene', 2:'Feb', 3:'Mar', 4:'Abr', 5:'May', 6:'Jun',
                     7:'Jul', 8:'Ago', 9:'Set', 10:'Oct', 11:'Nov', 12:'Dic'}
    
    df_plot = df.copy()
    df_plot['Nombre Mes'] = df_plot['mes'].map(meses_nombres)
    
    resumen_mensual = df.groupby('mes')['pp'].median()
    mes_critico_num = resumen_mensual.idxmax()
    mes_critico_nombre = meses_nombres[mes_critico_num]

    fig = px.box(
        df_plot, 
        x='Nombre Mes', 
        y='pp', 
        points="outliers",
        category_orders={"Nombre Mes": list(meses_nombres.values())},
        color='Nombre Mes',
        color_discrete_sequence=px.colors.qualitative.Safe,
        labels={'pp':'Lluvia (mm)', 'Nombre Mes': 'Mes'}
    )

    fig.update_layout(**BASE_LAYOUT, showlegend=False)
    
    return fig, mes_critico_nombre

def grafico_histograma(df):
    if df is None or df.empty: return None, 0
    
    df_lluvia = df[df['pp'] > 0.1] 
    media_intensidad = df_lluvia['pp'].mean()
    
    fig = px.histogram(
        df_lluvia, 
        x='pp', 
        nbins=50,
        labels={'pp':'Precipitación (mm)', 'count':'Número de días'},
        color_discrete_sequence=['#2ecc71']
    )
    
    fig.update_layout(**BASE_LAYOUT, showlegend=False)
    
    return fig, media_intensidad