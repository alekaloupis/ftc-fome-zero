#Libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import folium
from streamlit_folium import folium_static
import inflection
import numpy as np

st.set_page_config(page_title = 'Fome Zero', page_icon = '🥩', layout = 'wide')


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

#Ajustando os valores das colunas has_table_booking, has_online_delivery, is_delivering_now

df1['has_table_booking'] = df1['has_table_booking'].replace({0: 'No', 1: 'Yes'})

df1['has_online_delivery'] = df1['has_online_delivery'].replace({0: 'No', 1: 'Yes'})

df1['is_delivering_now'] = df1['is_delivering_now'].replace({0: 'No', 1: 'Yes'})


#Escrevendo as funções

def Restaurant_More_Votes(df1):
    
#Função que retorna os restaurantes e a quantidade de avaliações que eles possuem

    df_aux = df1.sort_values(by = ['votes'],ascending = False).reset_index()[['votes','restaurant_id','restaurant_name', 'country_code','cuisines', 'has_table_booking', 'has_online_delivery','is_delivering_now']]
    
       
    return df_aux.head(10)
                              

def Restaurant_Most_Aggregate_Rating(df1):  
    
#Função que retorna o restaurante com a maior nota de avaliação média

#A maior nota na avaliação foi de 4.9, tendo diversos restaurantes com essa nota. 

#Segundo orientações do exercicio, o criterio de desempate é o id do restaurante
    df_aux = df1.sort_values(by =['aggregate_rating','restaurant_id'], ascending = [False, 
    True]).reset_index()[['aggregate_rating','restaurant_id','restaurant_name', 'country_code', 'cuisines', 'has_table_booking', 'has_online_delivery','is_delivering_now']]
       
    
    return df_aux.head(10)
    
def Restaurant_Most_Average_Cost(df1):    
    
#Função que retorna o restaurante que posseui o maior valor de um prato para duas pessoas    
    
    df_aux = df1.sort_values(by =['average_cost_for_two','restaurant_id'], ascending = [False, 
    True]).reset_index()[['average_cost_for_two','restaurant_id','restaurant_name', 'cuisines',
                          'has_table_booking', 'has_online_delivery','is_delivering_now']]                          
           
    return df_aux.head(10)



def Cuisines_Agg_Rating(df1):
    
    df_aux = pd.DataFrame(df1.groupby(by = ['cuisines']).apply(lambda x: round(np.mean(x['aggregate_rating'],0))).reset_index())
    
    df_aux = df_aux.rename(columns = {0: 'média das avaliações'})
  
    return df_aux


def Cuisines_Mean_Avg_Cost_for_Two(df1):
    
    df_aux = df1.groupby(by = ['cuisines']).mean().sort_values(by = ['average_cost_for_two'], ascending = False).reset_index()[
        ['cuisines','average_cost_for_two']]
    
    df_aux['average_cost_for_two'] = list(map(lambda x: round(x,1), df_aux['average_cost_for_two']))
  
    return df_aux



def Cuisines_Conditions_Count(df1):
    
    #Função para contar e concatenar os restaurantes que aceitam pedidos_online, fazem entregas e fazem reservas
    
    
    df_aux1 = df1.groupby(by = ['cuisines']).count().reset_index()[['cuisines','restaurant_id']]
    
    df_aux1 = df_aux1.rename(columns = {'restaurant_id': 'has_table_booking'})
    
    df_aux2 = df1.groupby(by = ['cuisines']).count().reset_index()[['cuisines','restaurant_id']]    
  
    df_aux2 = df_aux2.rename(columns = {'restaurant_id': 'has_online_delivery'})
   
    df_aux3 = df1.groupby(by = ['cuisines']).count().reset_index()[['cuisines','restaurant_id']]    
    
    df_aux3 = df_aux3.rename(columns = {'restaurant_id': 'is_delivering_now'})
   
    df_aux = pd.merge(df_aux1, df_aux2, on = 'cuisines', how = 'outer')
    
    df_aux_final = pd.merge(df_aux, df_aux3, on = 'cuisines', how = 'outer')
    
    return df_aux_final

    
    

#Construindo as barras laterais

st.sidebar.markdown('# Filtros')

countries = df1['country_code'].unique()

#Definimos esses paises como default pois são os paises nos quais há maior numero de ocorrencias
default_countries = ['India','United States of America','England','South Africa','United Arab Emirates']

country_options = st.sidebar.multiselect(
'Quais os países que deseja incluir da seleção', 
countries,
default = default_countries
)          

#Definimos as opções abaixo como as opções de culinaria padrão
default_cuisines = ['BBQ','American','Italian','Japanese','Brazilian']

cuisines = df1['cuisines'].unique()

cuisines_options = st.sidebar.multiselect(
'Quais os tipos de culinária que deseja incluir na seleção',
cuisines,
default = default_cuisines
   
)

reservas = st.sidebar.radio(
'Os restaurantes realizam reservas (has_table_booking)',
('Ambos','Sim', 'Não') )

pedidos_online = st.sidebar.radio(
'Os restaurantes atendem pedidos online (has_online_delivery)',
('Ambos','Sim', 'Não') )

entregas = st.sidebar.radio(
'Os restaurantes realizam entregas (is_delivering_now)',
('Ambos','Sim', 'Não') )

st.sidebar.markdown("Powered by Alessandro Kaloupis")

#Seleção dos paises da base de dados
linhas_selecionadas = df1['country_code'].isin(country_options)

df1 = df1.loc[linhas_selecionadas, :]

#Seleção dos tipos de culinária da base de dados
linhas_selecionadas = df1['cuisines'].isin(cuisines_options)

df1 = df1.loc[linhas_selecionadas, :]

#Seleção se os restaurantes realizam reservas

if  (reservas == 'Sim'):
    linhas_selecionadas = (df1['has_table_booking'] == 'Yes')
    df1 = df1.loc[linhas_selecionadas, :]
    
elif (reservas == 'Não'):
    linhas_selecionadas = (df1['has_table_booking'] == 'No')
    df1 = df1.loc[linhas_selecionadas, :]
    
#Seleção se os restaurantes atendem pedidos online    
    
if  (pedidos_online == 'Sim'):
    linhas_selecionadas = (df1['has_online_delivery'] == 'Yes')
    df1 = df1.loc[linhas_selecionadas, :]
    
elif (pedidos_online == 'Não'):
    linhas_selecionadas = (df1['has_online_delivery'] == 'No')
    df1 = df1.loc[linhas_selecionadas, :]

#Seleção se os restaurantes realizam entregas    

if  (entregas == 'Sim'):
    linhas_selecionadas = (df1['is_delivering_now'] == 'Yes')
    df1 = df1.loc[linhas_selecionadas, :] 
    
elif(entregas == 'Não'):
    linhas_selecionadas = (df1['is_delivering_now'] == 'No')
    df1 = df1.loc[linhas_selecionadas, :] 





#Plotando as informações

st.title("🥩Visão Restaurantes / Culinárias")

tab1, tab2, tab3 = st.tabs(['Restaurantes1', 'Restaurantes2','Culinárias'])

with tab1:
    with st.container():
        st.markdown("### Restaurantes com maior quantidade de avaliações feitas")
        restaurant_more_votes = Restaurant_More_Votes(df1)
        st.dataframe(restaurant_more_votes)   
        
    with st.container():
        st.markdown("### Restaurantes com maior nota média de avaliação")
        restaurant_most_agg_rating = Restaurant_Most_Aggregate_Rating(df1)
        st.dataframe(restaurant_most_agg_rating)
   
   

with tab2: 
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1: 
            col1.metric('Quantidade de Avaliações',df1['votes'].sum())
        with col2:
            col2.metric('Média do Valor de um Prato para 2 pessoas',round(df1['average_cost_for_two'].mean(),1))
        with col3:
            col3.metric('Quantidade de restaurantes', len(df1))
            
            
    with st.container():
        st.markdown("### Restaurantes com maior valor de prato para 2")
        restaurant_most_average_cost = Restaurant_Most_Average_Cost(df1)
        st.dataframe(restaurant_most_average_cost)        
        
with tab3:   
    
    with st.container():
        st.markdown("### Tipo de Culinária x Nota Média")
        cuisines_agg_rating = Cuisines_Agg_Rating(df1)
        st.dataframe(cuisines_agg_rating)
    
    with st.container():
        st.markdown("### Tipos de Culinaria x Valor Médio de Prato para 2 pessoas")
        cuisines_mean = Cuisines_Mean_Avg_Cost_for_Two(df1)
        st.dataframe(cuisines_mean)

        
