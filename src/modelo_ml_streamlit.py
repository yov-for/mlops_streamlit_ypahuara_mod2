import streamlit as st #Para hacer una web de datos
from PIL import Image #Para el manejo de imágenes
import pandas as pd #Para generar los Dataframes de mis CSV
import time #Para la parte de sincronía y para medir el tiemp de procesamiento

import joblib #Este es para recibir el Pipeline del Ingeniero de Datos y del Ing de ML
import numpy as np #Para operaciones matemáticas
import matplotlib.pyplot as plt #Para plotear algunas gráficas (Histogramas)

#------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------

def prediccion_o_inferencia(pipeline_de_test, datos_de_test):
    #Dropeamos
    # datos_de_test.drop('car_ID', axis=1, inplace=True)
    # Cast MSSubClass as object
    # datos_de_test['MSSubClass'] = datos_de_test['MSSubClass'].astype('O')
    # datos_de_test = datos_de_test[config.FEATURES] #Aquí estoy aplicando mi SELECTED FEATURES

    # new_vars_with_na = [
    #     var for var in config.FEATURES
    #     if var not in config.CATEGORICAL_VARS_WITH_NA_FREQUENT +
    #     config.CATEGORICAL_VARS_WITH_NA_MISSING +
    #     config.NUMERICAL_VARS_WITH_NA
    #     and datos_de_test[var].isnull().sum() > 0]
    
    # datos_de_test.dropna(subset=new_vars_with_na, inplace=True)

    predicciones = pipeline_de_test.predict(datos_de_test)
    # predicciones_sin_escalar = np.exp(predicciones)

    return predicciones, datos_de_test



#Diseno de la Interface
st.title("Proyecto Modelo ML - Yovani Pahuara - DATAPATH")

image = Image.open('src/images/datapath-logo.png') #src/
st.image(image, use_container_width=True) #use_column_width esta "deprecated"

st.sidebar.write("Suba el archivo CSV correspondiente para realizar la predicción")

#------------------------------------------------------------------------------------------
# Cargar el archivo CSV desde la barra lateral
uploaded_file = st.sidebar.file_uploader(" ", type=['csv'])

if uploaded_file is not None:
    #Leer el archivo CSV y lo pasamos a Dataframe
    df_de_los_datos_subidos = pd.read_csv(uploaded_file)

    #Mostrar el contenido del archivo CSV
    st.write('Contenido del archivo CSV en formato Dataframe:')
    st.dataframe(df_de_los_datos_subidos)
#-------------------------------------------------------------------------------------------
#Cargar el Modelo ML o Cargar el Pipeline
pipeline_de_produccion = joblib.load('src/precios-autos-proyecto.joblib') #src/

if st.sidebar.button("click aqui para enviar el CSV al Pipeline"):
    if uploaded_file is None:
        st.sidebar.write("No se cargó correctamente el archivo, subalo de nuevo")
    else:
        with st.spinner('Pipeline y Modelo procesando...'):

            prediccion, datos_procesados = prediccion_o_inferencia(pipeline_de_produccion, df_de_los_datos_subidos)
            time.sleep(5)
            st.success('Listo!')

            # Mostramos los resultados de la predicción
            st.write('Resultados de la predicción:')
            st.write(prediccion)
            # st.write(prediccion_sin_escalar)

            #Graficar los precios de venta predichos
            fig, ax = plt.subplots()
            pd.Series((prediccion)).hist(bins=50, ax=ax)
            ax.set_title('Histograma de los precios de venta predichos')
            ax.set_xlabel('Precio')
            ax.set_ylabel('Frecuencia')

            #Mostramos la gráfica en Streamlit
            st.pyplot(fig)

            #Proceso para descargar todo el archivo con las predicciones
            #----------------------------------------------------------------------------
            #Concatenamos predicciones con el archivo original subido
            df_resultado = datos_procesados.copy()
            df_resultado['Predicción Escalada'] = prediccion
            # df_resultado['Predicción Sin Escalar'] = prediccion_sin_escalar

            #Mostrar el Dataframe contatenado
            st.write('Datos originales con predicciones:')
            st.dataframe(df_resultado)

            #Creamos el archivo CSV para descargar
            csv = df_resultado.to_csv(index=False).encode('utf-8')

            #Botón para descargar el CSV
            st.download_button(
                label="Descargar archivo CSV con predicciones",
                data=csv,
                file_name='predicciones_autos.csv',
                mime='text/csv',
            )
            #-------------------------------------------------------------------

#Comando para lanzar la aplicación de forma LOCAL:
#streamlit run modelo_ml_streamlit.py
