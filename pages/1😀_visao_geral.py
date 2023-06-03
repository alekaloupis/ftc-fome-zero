#Libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import inflection

st.set_page_config(page_title = 'Fome Zero', page_icon = '😀',layout = 'wide')


#Importando a base de dados
df = pd.read_csv('zomato.csv')

#Ajustando determinadas informações e colunas do DataFrame

#1. Começando pela coluna de Países (Country_Code)

#As identificações abaixo são os códigos referentes a cada um dos países

COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}

#Essa função criada retorna o nome de um país ao passar um ID
def country_name(country_id):
    return COUNTRIES[country_id]

#Aplicando a função nos valores de cada uma das linhas da coluna Country Code
df['Country Code'] = list(map(country_name, df['Country Code']))

#2. Essa função transforma as categorias de tipo de preço em texto

def create_price_type(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"
    
#Aplicamos a função nos valores da coluna Price Range, transformando os valores    
df['Price range'] = list(map(create_price_type, df['Price range']))  


#3. Ajustando os codigos das cores
#Criando as categorias de cores com base no código de cada cor

COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}

def color_name(color_code):
    return COLORS[color_code]

#Aplicando a função criada em todos os valores da coluna Rating color
df['Rating color'] = list(map(color_name, df['Rating color']))


#4. Função que renomeia e padroniza as colunas do DataFrame

def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df

#O objeto df está recebendo as modificações nos titulos feitas a partir da função
#rename_columns
df = rename_columns(df)

#5. Conforme orientação do exercício, precisamos categorizar os restaurantes somente por um tipo de culinaria
#Para isso, escrevemos a função abaixo
df['cuisines'] = df['cuisines'].astype(str)
df["cuisines"] = df.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])

#Sem remover as duplicadas, temos 7527 linhas no DataFrame
len(df)

#Essa linha de codigo remove todas as linhas identicas do codigo, mantendo apenas uma versao
df1 = df.drop_duplicates()

#Removendo as duplicatas, o DataFrame passou a ter 6942 linhas
len(df1)


def Building_Map(df1):
    
    df_new_ax = df1.groupby(by =['country_code', 'city','latitude',
    'longitude']).count().reset_index()[['country_code','city','latitude', 'longitude']]
    
    mapa = folium.Map()
    
    marcadores = MarkerCluster().add_to(mapa)

    
    for index, valor in df_new_ax.iterrows():
        
        latitude = valor ['latitude']
        longitude = valor ['longitude']
        city = valor ['city']
        
        folium.Marker(
        location = [latitude, longitude],
        popup = city       
        ).add_to(marcadores)
        
    folium_static(mapa, width = 1024 , height = 1024)  



#Construindo as barras laterais


   

st.sidebar.markdown('# Fome Zero')

countries = df1['country_code'].unique()

country_options = st.sidebar.multiselect(
'Quais os países que deseja incluir na seleção', 
countries,
default = countries
)   



st.sidebar.markdown("Powered by Alessandro Kaloupis")

#Indicando para que o filtro de data pegue todas as datas anteriores às que eu filtrei

linhas_selecionadas = df1['country_code'].isin(country_options)

df1 = df1.loc[linhas_selecionadas, :]

#Layout do Streamlit

st.title("Fome Zero!")
st.header("O melhor lugar para encontrar seu mais novo restaurante favorito")
st.header("Temos as seguintes marcas dentro da nossa plataforma")
with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        col1.metric("Restaurantes únicos cadastrados", df1['restaurant_id'].nunique())
    with col2: 
        col2.metric("Países únicos",df1['country_code'].nunique())
    with col3:
         col3.metric("Cidades únicas", df1['city'].nunique())
    with col4:
          col4.metric("Tipos de culinárias oferecidas", df1['cuisines'].nunique())
    with col5:
        col5.metric("Avaliações feitas na plataforma", df1['votes'].sum())
        
with st.container():
    Building_Map(df1)
      

    



