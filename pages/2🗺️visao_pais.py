#Libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import folium
from streamlit_folium import folium_static
import inflection

st.set_page_config(page_title = 'Fome Zero', page_icon = '🗺️', layout = 'wide')


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


def City_Restaurant(df1):    
    ''' Função para retornar a quantidade de cidades por país 
    '''
    
    #Agrupamos os dados a partir do país e da cidade
    df_aux = pd.DataFrame(df1.groupby(by = ['country_code', 'city']).count().reset_index()[['country_code','city']])
    #Cada cidade especifica vai receber o valor 1 na coluna 'auxiliar' Quantities
    df_aux['quantities'] = 1
    #Depois agrupamos por pais e somamos as quantidades de cidade
    df_aux = pd.DataFrame(df_aux.groupby(by =['country_code']).sum().sort_values(by = ['quantities'],  ascending = False).reset_index()[['country_code','quantities']])
    
    df_aux = df_aux.rename(columns = {'quantities': 'quantidades de cidades' })
    
    fig = px.bar(df_aux, x = 'country_code', y = 'quantidades de cidades', title = 'Quantidade de cidades por país',text = 'quantidades de cidades', hover_data = ['quantidades de cidades'], color = 'quantidades de cidades')
                                                                            
    fig.update_xaxes(title_text='Países')
    fig.update_yaxes(title_text='Quantidade de Cidades')
    
    fig.update_layout(
    autosize=False,
    width=1000,
    height=500)
    return fig


def Country_Restaurant(df1):
    '''Função para retornar a quantidade de restaurantes por país
    '''
    
    #Função que retorna a quantidade de restaurantes por país
    df_aux = df1.groupby(by = ['country_code']).count().sort_values(by = ['restaurant_id'],
    ascending = False).reset_index()[['country_code','restaurant_id']]
    
    df_aux = df_aux.rename(columns = {'restaurant_id': 'quantidades de restaurantes' })

    fig = px.bar(df_aux, x = 'country_code', y = 'quantidades de restaurantes', title = 'Quantidade de restaurantes por país',text = 'quantidades de restaurantes', hover_data = ['quantidades de restaurantes'], color = 'quantidades de restaurantes')
                 
                 
    fig.update_xaxes(title = 'Países')
    fig.update_yaxes(title = 'Quantidade de Restaurantes')    
    
    
    fig.update_layout(
    autosize=False,
    width=1000,
    height=500)
    return fig
    
    return fig

def Country_Distinct_Cuisines(df1):
    #Função para descobrir a quantidade de culinarias distintas que temos em cada pais
    
    #Agrupamos por tipo de país e tipo de culinaria os DataFrames
    df_aux = df1.groupby(by = ['country_code','cuisines']).count().reset_index()[['country_code','cuisines']]
    
    #Cada tipo de culinária receberá o valor 1
    df_aux['quantities'] = 1
    
    #Essa coluna auxiliar será utlizada para fazermos a soma de cada um dos tipos de culinaria por pais
    df_aux = pd.DataFrame(df_aux.groupby(by =['country_code']).sum().sort_values(by = ['quantities'],
    ascending = False).reset_index()[['country_code','quantities']])
    
    df_aux = df_aux.rename(columns = {'quantities': 'quantidades de culinarias'})

    
    
    fig = px.bar(df_aux, x = 'country_code', y = 'quantidades de culinarias', title = 'Quantidade de tipos de culinária por país',text = 'quantidades de culinarias',
          hover_data = ['quantidades de culinarias'], color = 'quantidades de culinarias'   
                )
    fig.update_xaxes(title = 'Países')
    fig.update_yaxes(title = 'Quantidades Culinárias')
    
    
    fig.update_layout(
    autosize=False,
    width=1000,
    height=500)
    
    return fig
    


def Sum_Votes_per_Country(df1):
    
    #Função para somar as avaliacoes de restaurantes feitas por pais
    
    #Essa soma das avaliações será obtida multiplicando a quantidade de votações e a média das avaliações para cada restaurante
   

    df_aux = df1.groupby(by =['country_code']).sum().sort_values(by = ['votes'],
    ascending = False).reset_index()[['country_code','votes']]
    
    df_aux = df_aux.rename(columns = {'votes': 'quantidade de avaliações'})
   
    fig = px.bar(df_aux, x = 'country_code', y = 'quantidade de avaliações', 
                 title = 'País x Quantidade de Avaliações feitas',
                 text = 'quantidade de avaliações', hover_data =['quantidade de avaliações'], color = 'quantidade de avaliações')   
    
    fig.update_xaxes(title = 'Países')
    fig.update_yaxes(title = 'Total das Avaliações Feitas')
    
    fig.update_layout(
    autosize=False,
    width=1000,
    height=500)
    
    return fig

def Country_Mean_Votes(df1):
    
#Função que agrupa os paises e retorna a media das quantidades de avaliações feitas por pais

#Agrupamos por pais e depois fizemos a media das avaliações atribuidas aos restaurantes

    df_aux = df1.groupby(by = ['country_code']).mean().sort_values(by = ['votes'], 
    ascending = False).reset_index()[['country_code','votes']]
    
#Arredondamos para nenhuma casa decimal os resultaados    
    df_aux['votes'] = list(map(lambda x: round(x,0), df_aux['votes']))
    
    df_aux = df_aux.rename(columns = {'votes': 'média das quantidades de avaliações'})
   
   
    fig = px.bar(df_aux, x = 'country_code', y = 'média das quantidades de avaliações',title = 'País x Média das Quantidades de Avaliações',
                 text = 'média das quantidades de avaliações', hover_data =['média das quantidades de avaliações'], color = 'média das quantidades de avaliações')
    
    fig.update_xaxes(title = 'Países')
    fig.update_yaxes(title = 'Média das Quantidades de Avaliações')
    
    
    fig.update_layout(
    autosize=False,
    width=1000,
    height=500)
    
    return fig


def Gourmet_Restaurant_Country(df1):
    '''Função que retorna a quantidade de restaurantes classificados como gourmet por país
    '''
    
    #Restaurantes com nivel preço igual 4 são aqueles classificados como gourmet
    
    df_aux = df1.loc[(df1['price_range'] == 'gourmet')].groupby(by = ['price_range',
 'country_code']).count().sort_values(by = 
                                      ['restaurant_id'], ascending = False).reset_index()[['price_range','country_code','restaurant_id']]
    
    df_aux = df_aux.rename(columns = {'restaurant_id':'quantidade de restaurantes'})
    
    fig = px.bar(df_aux, x = 'country_code', y = 'quantidade de restaurantes', title = 'Quantidade de Restaurantes Gourmet por País',text = 'quantidade de restaurantes', hover_data = ['quantidade de restaurantes'], color = 'quantidade de restaurantes')
    
    fig.update_xaxes(title = 'Países')
    fig.update_yaxes(title = 'Restaurantes - Gourmet')
    
    
    fig.update_layout(
    autosize=False,
    width=1000,
    height=500)
    
    return fig  


def Restaurant_Quantity_Delivering_Country(df1):
    
    #Função para somar a quantidade de restaurantes distintos por pais
    
    #Vamos considerar o valor da coluna 0 para False e 1 para True
    
    #A coluna (is delivering now) como a coluna que fornece a informação sobre se o restaurante realiza a entrega
    
    #Organizei um dataframe que possui o nome do pais e do restaurante pertencente ao pais
    df_aux = df1.loc[(df1['is_delivering_now'] == 1)].groupby(by = ['country_code', 
                               'restaurant_name']).count().reset_index()[['country_code','restaurant_name']]
    
    df_aux['quantities'] = 1
    
    df_aux = df_aux.groupby(by = ['country_code']).sum().sort_values(by = ['quantities'],
    ascending = False).reset_index()[['country_code', 'quantities']]
    
    df_aux = df_aux.rename(columns = {'quantities':'quantidade de restaurantes'})
    
    fig = px.bar(df_aux, x = 'country_code', y = 'quantidade de restaurantes',title = 'Países x Quantidade de Restaurantes que fazem entregas',
                 text = 'quantidade de restaurantes', hover_data = ['quantidade de restaurantes'], color = 'quantidade de restaurantes')
    
    fig.update_xaxes(title = 'Países')
    fig.update_yaxes(title = 'Restaurantes - Entregas')
    
    
    fig.update_layout(
    autosize=False,
    width=1000,
    height=500)
    
    return fig



def Restaurant_Table_Booking(df1):    
    
    #Vamos considerar o valor da coluna 0 para False e 1 para True
    
    #A coluna (has table booking) como a coluna que fornece a informação sobre se o restaurante realiza a entrega
    
    #Organizei um dataframe que possui o nome do pais e do restaurante pertencente ao pais
    df_aux = df1.loc[(df1['has_table_booking'] == 1)].groupby(by = ['country_code', 
                               'restaurant_name']).count().reset_index()[['country_code','restaurant_name']]
    
    df_aux['quantities'] = 1
    
    df_aux = df_aux.groupby(by = ['country_code']).sum().sort_values(by = ['quantities'],
    ascending = False).reset_index()[['country_code', 'quantities']]
    
    df_aux = df_aux.rename(columns = {'quantities':'quantidade de restaurantes'})
    
    fig = px.bar(df_aux, x = 'country_code', y = 'quantidade de restaurantes',title = 'País x Quantidade de Restaurantes que fazem reservas',
                 text = 'quantidade de restaurantes', hover_data = ['quantidade de restaurantes'], color = 'quantidade de restaurantes')
    
    fig.update_xaxes(title = 'Países')
    fig.update_yaxes(title = 'Restaurantes - Reservas')
    
        
    fig.update_layout(
    autosize=False,
    width=1000,
    height=500)
    
    return fig



def Mean_Rating_per_Country(df1):
    
    #Função para calcular as notas medias atribuidas aos restaurantes dos diferentes paises

    
    df_aux = df1.groupby(by =['country_code']).mean().sort_values(by = ['aggregate_rating'],
    ascending = False).reset_index()[['country_code','aggregate_rating']]
    
    df_aux['aggregate_rating'] = list(map(lambda x: round(x,2), df_aux['aggregate_rating']))
    
    df_aux = df_aux.rename(columns = {'aggregate_rating':'média das avaliações'})
    
    
    fig = px.bar(df_aux, x = 'country_code', y = 'média das avaliações', 
                 title = 'País x Média das Notas',
                 text = 'média das avaliações', hover_data = ['média das avaliações'],
                 color = 'média das avaliações')
    
    fig.update_xaxes(title = 'Países')
    fig.update_yaxes(title = 'Média das Notas')
    
       
    fig.update_layout(
    autosize=False,
    width=1000,
    height=500)
    
    return fig

def Avg_Cost_Two_Country(df1):
    
    #Função criada para retornar a media do preco de um prato para dois nos diferentes paises
    
    df_aux = df1.groupby(by =['country_code']).mean().sort_values(by = ['average_cost_for_two'],
                         ascending = False).reset_index()[['country_code','average_cost_for_two']]

    df_aux['average_cost_for_two'] = list(map(lambda x: round(x,1), df_aux['average_cost_for_two']))
    
    df_aux = df_aux.rename(columns = {'average_cost_for_two':'media de prato para dois'})
    
    fig = px.bar(df_aux, x = 'country_code', y = 'media de prato para dois', 
                 title = 'País x Média de Preço de um Prato para Dois',
                 text = 'media de prato para dois', hover_data = ['media de prato para dois'], color = 'media de prato para dois')
    
    fig.update_xaxes(title = 'Países')
    fig.update_yaxes(title = 'Média de Preço de um Prato para Dois')
    
    
    
    fig.update_layout(
    autosize=False,
    width=1000,
    height=500)
    
    
    return fig





#Construindo as barras laterais

st.sidebar.markdown('# Fome Zero')

countries = df1['country_code'].unique()

default_countries = ['India','United States of America','England','South Africa','United Arab Emirates']

country_options = st.sidebar.multiselect(
'Quais os países que deseja incluir da seleção', 
countries,
default = default_countries
)          

st.sidebar.markdown("Powered by Alessandro Kaloupis")

#Indicando para que o filtro de data pegue todas as datas anteriores às que eu filtrei

linhas_selecionadas = df1['country_code'].isin(country_options)

df1 = df1.loc[linhas_selecionadas, :]




st.title("🗺️Visão Países")

tab1, tab2, tab3, tab4 = st.tabs(['Visão Geral','Avaliações','Restaurantes', 'Outras Informações'])

with tab1: 

    with st.container():
        fig = City_Restaurant(df1)
        st.plotly_chart(fig, use_containter_width = True)

    with st.container():
        fig = Country_Restaurant(df1)
        st.plotly_chart(fig, use_containter_width = True)
    
    with st.container():
        fig = Country_Distinct_Cuisines(df1)
        st.plotly_chart(fig, use_containter_width = True)
        
        
    
with tab2: 
    
    with st.container():
        fig = Sum_Votes_per_Country(df1)
        st.plotly_chart(fig, use_containter_width = True)
        
    with st.container():
        fig = Country_Mean_Votes(df1)
        st.plotly_chart(fig, use_containter_width = True)
        
   
with tab3: 
    
    with st.container(): 
        fig = Gourmet_Restaurant_Country(df1)
        st.plotly_chart(fig, use_containter_width=True)
    
    with st.container():
        fig = Restaurant_Quantity_Delivering_Country(df1)
        st.plotly_chart(fig, use_containter_width=True)
    
    with st.container():
        fig = Restaurant_Table_Booking(df1)
        st.plotly_chart(fig, use_containter_width=True)    

with tab4: 
    
    with st.container():
        fig = Mean_Rating_per_Country(df1)
        st.plotly_chart(fig, use_containter_width=True)
    
    with st.container():
        fig = Avg_Cost_Two_Country(df1)
        st.plotly_chart(fig, use_containter_width= True)
       
       
