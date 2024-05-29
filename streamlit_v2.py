# -*- coding: utf-8 -*-
"""Streamlit_v2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/118WB9gRmzKcmO6HHaTF2cstZpglFON-T
"""

import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Encuesta Shopper")  # Nombre para configurar la pagina web
st.markdown('<h1 style="text-align: center;">Resultados Encuestas Shopper 2024</h1>', unsafe_allow_html=True)  # Título de la página

# Importar archivos Excel
@st.cache_data
def load_data():
    excel_file = 'Avance_Encuesta_1_py.xlsx'  # Nombre del archivo a importar
    sheet_name = 'Sheet1'  # La hoja de excel que voy a importar

    df = pd.read_excel(excel_file, sheet_name=sheet_name)

    # Preparación data
    df = df[df["flag_calidad"] == "Correcto"]
    return df

df = load_data()

#df1 = pd.read_excel('Lista_Microsegmentos_activos.xlsx', sheet_name='in')
df["Ingrese el código de cliente. Ejemplo: 1245089"]=df["Ingrese el código de cliente. Ejemplo: 1245089"].astype(str)
#df["Ingrese el código de cliente. Ejemplo: 1245089"] = df["Ingrese el código de cliente. Ejemplo: 1245089"].str.lstrip('0')
#df['Ingrese el código de cliente. Ejemplo: 1245089'] = df['Ingrese el código de cliente. Ejemplo: 1245089'].astype(str).str.replace(' ', '').str.lstrip('0')
df = df.sort_values(by=['Ingrese el código de cliente. Ejemplo: 1245089', 'Hora de inicio'])
df['Flag_ocurrencia'] = df.groupby('Ingrese el código de cliente. Ejemplo: 1245089').cumcount() + 1
df = df.sort_values(by=['Ingrese el código de cliente. Ejemplo: 1245089', 'Hora de inicio'], ascending=[True, False])

# Seleccionar el mayor número del flag de ocurrencia por ID
idx = df.groupby('Ingrese el código de cliente. Ejemplo: 1245089')['Flag_ocurrencia'].idxmax()
result = df.loc[idx].sort_values(by='Ingrese el código de cliente. Ejemplo: 1245089')
result.columns = result.columns.str.replace('\xa0', '')
result = result.rename(columns={
    'Ingrese el código de cliente. Ejemplo: 1245089': 'customer_id',
    'Para el bodeguero, ¿Qué lugares están cerca de la bodega (máx a 2 cuadras)? (Marque las opciones que considere)': 'Cercania',
    'Para el vendedor, ¿Cuáles son los exhibidores que tiene la tienda? (marque las opciones que considere)': 'Exhibidores',
    'Para el bodeguero, ¿Cuál es el monto semanal que gastas en la compra total de abarrotes, lavado, limpieza y shampoo? (NO SOLO ALICORP)': 'Monto_semanal',
    'Para el bodeguero, ¿Por qué motivo te compran tus clientes? (Marque hasta 2 opciones)': 'Intencion_compra',
    'Para el bodeguero,¿Cuáles son los productos que suele vender con mayor frecuencia? (Marque hasta 3 opciones)': 'Productos_venta',
    'Para el bodeguero, ¿Cuál es el tamaño de abarrotes/detergentes que más vende? (Marque hasta 2 opciones)': 'Tamaño_producto',
    'Para el bodeguero, ¿Cuántos productos (categorías) distintos le compra un cliente por visita?': 'Productos_cliente',
    'Para el bodeguero, ¿Cuánto suelen gastar tus clientes en cada oportunidad decompra? ': 'Monto_cliente',
    'Para el bodeguero, ¿Cuántas veces a la semana le compra un solo cliente?': 'Frecuencia_cliente'
})
result["customer_id"] = result["customer_id"].astype(str)
#df1["customer_id"] = df1["customer_id"].astype(str)

#result = result.merge(df1[["customer_id", "Departamento", "Microsegmento", "flag_activo"]], on="customer_id", how="left")
#result = result.dropna(subset=['Microsegmento'])
#result = result[result["flag_activo"] == 1]

result_1 = result[['customer_id','Hora de inicio' ,'Fecha', 'Cercania','cercania_op', 'Exhibidores','equipo_op' , 'Intencion_compra','MISION_op', 'Productos_venta','productos_op' ,'Tamaño_producto','tamaño_op', 'Productos_cliente', 'Monto_cliente', 'Frecuencia_cliente', 'Flag_ocurrencia', 'Microsegmento', 'Departamento1']]
#result_1.loc[:,'Mes'] = result_1['Mes'].astype(str).replace({"4": "Abril", "5": "Mayo"})
#result_1['Departamento'] = result_1['Departamento'].fillna("Sin Dato").replace(0, 'Sin Dato')
#result_1 = result_1.head(200)

# Convertir la columna Día a formato de fecha
result_1.loc[:,'Fecha'] = pd.to_datetime(result_1['Fecha'])

# Crear multiselectores
Departamento = result_1['Departamento1'].unique().tolist()
Microsegmento = result_1['Microsegmento'].unique().tolist()
Cercania = result_1['cercania_op'].unique().tolist()
Equipo = result_1['equipo_op'].unique().tolist()
Mision = result_1['MISION_op'].unique().tolist()
Productos = result_1['productos_op'].unique().tolist()
Tamaños = result_1['tamaño_op'].unique().tolist()
Mision1 = result_1['Intencion_compra'].unique().tolist()



#mes_selector = st.multiselect('Mes:', Mes, default=Mes)
Departamento_selector = st.multiselect('Departamento:', Departamento, default=Departamento)
Microsegmento_selector = st.multiselect('Microsegmento:', Microsegmento, default=Microsegmento)
#st.dataframe(df.head(4))
#st.dataframe(df.tail(4))


# Usar st.date_input para seleccionar un rango de fechas
start_date = result_1['Fecha'].min() #if not result_1.empty else None
end_date = result_1['Fecha'].max() #if not result_1.empty else None
#if start_date is not None and end_date is not None:
date_range = st.date_input('Seleccione el rango de fechas:', [start_date, end_date], min_value=start_date, max_value=end_date)

# Filtrar datos según las selecciones
mask = (result_1['Fecha'].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1]))) & (result_1['Departamento1'].isin(Departamento_selector))&(result_1['Microsegmento'].isin(Microsegmento_selector))

numero_resultados = result_1[mask].shape[0]
st.markdown(f'*Resultados Disponibles: {numero_resultados}*')
#st.markdown(f'*Resultados Disponibles: {result.shape[0]}*')
#st.markdown(f'*Resultados Disponibles: {df.shape[0]}*')
#st.markdown(f'*Resultados Disponibles: {result_1.shape[0]}*')
#st.dataframe(df)
#st.dataframe(result_1)
#st.dataframe(result_1[mask])
#st.markdown(date_range)

filtered_data = result_1[mask]

st.subheader('Preguntas Encuestas-Características Shopper')
st.markdown('##### Para el bodeguero, ¿Qué lugares están cerca de la bodega (máx a 2 cuadras)? (Marque las opciones que considere)')
# Agrupación y gráficos
Cercania_selector = st.multiselect('Cercania opción:', Cercania, default=Cercania)
mask1 = (filtered_data['cercania_op'].isin(Cercania_selector))
numero_resultados = filtered_data[mask1].shape[0]
st.markdown(f'*Resultados Disponibles: {numero_resultados}*')
filtered_data1 = filtered_data[mask1]
df_agrupado1 = filtered_data1.groupby(by=['Cercania']).count()[['customer_id']].rename(columns={'customer_id': 'Encuestados'}).reset_index()
df_agrupado1 = df_agrupado1.sort_values(by='Encuestados', ascending=False).head(5)
bar_chart = px.bar(df_agrupado1, x='Cercania', y='Encuestados', text='Encuestados', color_discrete_sequence=['#FF8C00']*len(df_agrupado1), template='plotly_white')
bar_chart.update_layout(
    yaxis=dict(showticklabels=False, title=''),
    xaxis=dict(title='')
)
st.plotly_chart(bar_chart)

st.markdown('##### Para el vendedor, ¿Cuáles son los exhibidores que tiene la tienda? (marque las opciones que considere)')
Exhibidor_selector = st.multiselect('Exhibidor opción:', Equipo, default=Equipo)
mask2 = (filtered_data['equipo_op'].isin(Exhibidor_selector))
numero_resultados = filtered_data[mask2].shape[0]
st.markdown(f'*Resultados Disponibles: {numero_resultados}*')
filtered_data2 = filtered_data[mask2]
df_agrupado2 = filtered_data2.groupby(by=['Exhibidores']).count()[['customer_id']].rename(columns={'customer_id': 'Encuestados'}).reset_index()
df_agrupado2 = df_agrupado2.sort_values(by='Encuestados', ascending=False).head(5)
bar_chart = px.bar(df_agrupado2.sort_values(by='Encuestados', ascending=True), y='Exhibidores', x='Encuestados',orientation='h', text='Encuestados', color_discrete_sequence=['#f5b632']*len(df_agrupado2), template='plotly_white')
bar_chart.update_layout(
    xaxis=dict(showticklabels=False, title=''),
    yaxis=dict(title='')
)
st.plotly_chart(bar_chart)

st.markdown('##### Para el bodeguero,¿Cuáles son los productos que suele vender con mayor frecuencia? (Marque hasta 3 opciones)')
Productos_selector = st.multiselect('Producto opción:', Productos, default=Productos)
mask3 = (filtered_data['productos_op'].isin(Productos_selector))
numero_resultados = filtered_data[mask3].shape[0]
st.markdown(f'*Resultados Disponibles: {numero_resultados}*')
filtered_data3 = filtered_data[mask3]
df_agrupado3 = filtered_data3.groupby(by=['Productos_venta']).count()[['customer_id']].rename(columns={'customer_id': 'Encuestados'}).reset_index()
df_agrupado3 = df_agrupado3.sort_values(by='Encuestados', ascending=False).head(5)
bar_chart = px.bar(df_agrupado3, x='Productos_venta', y='Encuestados', text='Encuestados', color_discrete_sequence=['#32CD32']*len(df_agrupado3), template='plotly_white')
bar_chart.update_layout(
    yaxis=dict(showticklabels=False, title=''),
    xaxis=dict(title='')
)
st.plotly_chart(bar_chart)

st.markdown('##### Para el bodeguero, ¿Cuál es el tamaño de abarrotes/detergentes que más vende? (Marque hasta 2 opciones)')
Tamaños_selector = st.multiselect('Tamaño producto opción:', Tamaños, default=Tamaños)
mask4 = (filtered_data['tamaño_op'].isin(Tamaños_selector))
numero_resultados = filtered_data[mask4].shape[0]
st.markdown(f'*Resultados Disponibles: {numero_resultados}*')
filtered_data4 = filtered_data[mask4]
df_agrupado4 = filtered_data4.groupby(by=['Tamaño_producto']).count()[['customer_id']].rename(columns={'customer_id': 'Encuestados'}).reset_index()
df_agrupado4 = df_agrupado4.sort_values(by='Encuestados', ascending=False).head(5)
bar_chart = px.bar(df_agrupado4.sort_values(by='Encuestados', ascending=True), y='Tamaño_producto', x='Encuestados', text='Encuestados',orientation='h',color_discrete_sequence=['#0000FF']*len(df_agrupado4), template='plotly_white')
bar_chart.update_layout(
    xaxis=dict(showticklabels=False, title=''),
    yaxis=dict(title='')
)
st.plotly_chart(bar_chart)


st.subheader('Preguntas Encuestas-Misiones de compra')
st.markdown('##### Para el bodeguero, ¿Por qué motivo te compran tus clientes? (Marque hasta 2 opciones)')
Mision_selector = st.multiselect('Intención compra opción:', Mision, default=Mision)
mask5 = (filtered_data['MISION_op'].isin(Mision_selector))
numero_resultados = filtered_data[mask5].shape[0]
st.markdown(f'*Resultados Disponibles: {numero_resultados}*')
filtered_data5 = filtered_data[mask5]
df_agrupado5 = filtered_data5.groupby(by=['Intencion_compra']).count()[['customer_id']].rename(columns={'customer_id': 'Encuestados'}).reset_index()
df_agrupado5 = df_agrupado5.sort_values(by='Encuestados', ascending=False).head(5)
bar_chart = px.bar(df_agrupado5.sort_values(by='Encuestados', ascending=True), y='Intencion_compra', x='Encuestados', text='Encuestados', orientation='h', color_discrete_sequence=['#ADD8E6']*len(df_agrupado5), template='plotly_white')
bar_chart.update_layout(
    xaxis=dict(showticklabels=False, title=''),
    yaxis=dict(title='')
)
st.plotly_chart(bar_chart)

st.markdown('##### Para el bodeguero,¿Cuántos productos (categorías) distintos le compra un cliente por visita?')
Mision1_selector = st.multiselect('Intención compra:', Mision1, default=Mision1)
mask6 = (filtered_data['Intencion_compra'].isin(Mision1_selector))
numero_resultados = filtered_data[mask6].shape[0]
st.markdown(f'*Resultados Disponibles: {numero_resultados}*')
filtered_data6 = filtered_data[mask6]
df_agrupado6 = filtered_data6.groupby(by=['Productos_cliente']).count()[['customer_id']].rename(columns={'customer_id': 'Encuestados'}).reset_index()
df_agrupado6 = df_agrupado6.sort_values(by='Encuestados', ascending=False).head(5)
bar_chart = px.bar(df_agrupado6, x='Productos_cliente', y='Encuestados', text='Encuestados', color_discrete_sequence=['#FF7F7F']*len(df_agrupado6), template='plotly_white')
bar_chart.update_layout(
    yaxis=dict(showticklabels=False, title=''),
    xaxis=dict(title='')
)
st.plotly_chart(bar_chart)

st.markdown('##### Para el bodeguero, ¿Cuánto suelen gastar tus clientes en cada oportunidad de compra?')
#Mision2_selector = st.multiselect('Intención compra:', Mision1, default=Mision1)
#mask7 = (filtered_data['Intencion_compra'].isin(Mision2_selector))
#numero_resultados = filtered_data[mask7].shape[0]
st.markdown(f'*Resultados Disponibles: {numero_resultados}*')
filtered_data7 = filtered_data[mask6]
df_agrupado7 = filtered_data7.groupby(by=['Monto_cliente']).count()[['customer_id']].rename(columns={'customer_id': 'Encuestados'}).reset_index()
df_agrupado7 = df_agrupado7.sort_values(by='Encuestados', ascending=False).head(5)
bar_chart = px.bar(df_agrupado7, x='Monto_cliente', y='Encuestados', text='Encuestados', color_discrete_sequence=['#D3D3D3']*len(df_agrupado7), template='plotly_white')
bar_chart.update_layout(
    yaxis=dict(showticklabels=False, title=''),
    xaxis=dict(title='')
)
st.plotly_chart(bar_chart)

st.markdown('##### Para el bodeguero, ¿Cuántas veces a la semana le compra un solo cliente?')
#Mision1_selector = st.multiselect('Intención compra:', Mision1, default=Mision1)
#mask8 = (filtered_data['Intencion_compra'].isin(Mision1_selector))
#numero_resultados = filtered_data[mask8].shape[0]
st.markdown(f'*Resultados Disponibles: {numero_resultados}*')
filtered_data8 = filtered_data[mask6]
df_agrupado8 = filtered_data8.groupby(by=['Frecuencia_cliente']).count()[['customer_id']].rename(columns={'customer_id': 'Encuestados'}).reset_index()
df_agrupado8 = df_agrupado8.sort_values(by='Encuestados', ascending=False).head(5)
bar_chart = px.bar(df_agrupado8, x='Frecuencia_cliente', y='Encuestados', text='Encuestados', color_discrete_sequence=['#DDA0DD']*len(df_agrupado8), template='plotly_white')
bar_chart.update_layout(
    yaxis=dict(showticklabels=False, title=''),
    xaxis=dict(title='')
)
st.plotly_chart(bar_chart)

st.dataframe(result_1[mask])