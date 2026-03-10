# 💧 MapDrop
### Procesamiento hidrometeorológico · MapLecture

**MapDrop** es una herramienta web educativa desarrollada por [MapLecture](https://maplecture.com) para el procesamiento y análisis exploratorio de datos de precipitación del SENAMHI (Perú).

Está dirigida a profesionales de ingeniería, geografía y gestión de riesgos que necesitan interpretar series de datos hidrometeorológicos sin ser especialistas en hidrología.

🔗 **[Acceder a la app](https://mapdrop.streamlit.app)** ← reemplaza con tu URL real

---

## ¿Qué hace MapDrop?

- **Estandarización:** Lee archivos `.csv` y `.txt` descargados directamente desde el SENAMHI y los convierte a un formato limpio y estructurado.
- **Validación de datos:** Genera una matriz de completitud por mes/año con semáforo visual para detectar períodos con datos faltantes.
- **Estadística de precipitaciones máximas:** Calcula la precipitación máxima en 24 horas por mes y año, con métricas históricas clave.
- **Análisis gráfico:** Visualiza la serie histórica, la variabilidad mensual y la distribución de frecuencias, con explicaciones educativas integradas.
- **Exportación:** Descarga la matriz de precipitaciones máximas en formato Excel (`.xlsx`).

---

## Archivos compatibles

| Formato | Fuente | Descripción |
|--------|--------|-------------|
| `.csv` | [SENAMHI - Datos convencionales](https://www.senamhi.gob.pe/site/descarga-datos/) | Incluye cabecera con metadatos de la estación |
| `.txt` | [SENAMHI - Buscador histórico](https://www.senamhi.gob.pe/?p=estaciones) | Datos en formato de columnas separadas por espacios |

> Si subes un `.txt` sin cabecera junto con un `.csv` de la misma estación, MapDrop extrae automáticamente los metadatos del CSV.

---

## Fundamento metodológico

El análisis se basa en la **Guía de Prácticas Hidrológicas** de la Organización Meteorológica Mundial:

> Organización Meteorológica Mundial. (2009). *Guía de prácticas hidrológicas* (6.ª ed., OMM-N° 168, Cap. 27–28). OMM.
> [📄 Descargar libro](https://www.academia.edu/28131870/GUIDE_YDROLOGICAL_PRACTICES_ADQUISICI%C3%93N_Y_PROCESO_DE_DATOS_AN%C3%81LISIS_PREDICCI%C3%93N_Y_OTRAS_APLICACIONES_GU%C3%8DA_DE_PR%C3%81CTICAS_HIDROL%C3%93GICAS_Bienvenido)

Los umbrales de precipitación se calculan mediante **percentiles empíricos (P50 y P90)** sobre la serie histórica cargada. Los resultados son de carácter exploratorio y su aplicación en decisiones técnicas requiere la revisión de un profesional especializado.

---

## Tecnologías

- [Python 3](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Plotly](https://plotly.com/python/)
- [XlsxWriter](https://xlsxwriter.readthedocs.io/)

---

## Autoría

**Desarrollado por:** Brenda Quiroz — Ingeniera Geógrafa  
**Proyecto:** MapLecture — Educación y Geografía Aplicada  
**Colaboración:** Desarrollado con apoyo de IA (Gemini, Claude)  
**Versión:** 1.0

---

## Licencia

Este proyecto es de uso libre con fines educativos y académicos.  
Para uso comercial o institucional, contactar a MapLecture.
