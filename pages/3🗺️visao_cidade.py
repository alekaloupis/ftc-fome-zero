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

#Escrevendo as funções

def City_More_Restaurants(df1):
    
    #Função para retornar as cidades com maior numero de restaurantes registrados
 

    df_aux = df1.groupby(['country_code', 'city']).size().reset_index(name='restaurant_count')
    df_aux = df_aux.sort_values(['country_code', 'restaurant_count'], ascending=[True, False])

# Filtrar as três cidades com o maior número de restaurantes para cada país
    df_top_cities = df_aux.groupby('country_code').head(3)
    
    df_top_cities = df_top_cities.rename(columns = {'country_code': 'países', 'restaurant_count':'quantidade de restaurantes',
                                      'city':'cidades' })


    fig = px.bar(df_top_cities, x="cidades", y="quantidade de restaurantes", color='países', barmode='group',
                 title = 'Quantidade de Restaurantes por Cidade', text = 'quantidade de restaurantes')
        
    
       
    fig.update_traces(width=0.7)

    fig.update_layout(
    autosize=False,
    width=1000,
    height=500
    )

    return fig



def City_Restaurant_Agg_Rating_4_More(df1):
    
    #Função para retornar as cidades com maior numero de restaurantes com 
    #nota media acima de 4
    
    df_aux = df1.loc[(df1['aggregate_rating'] > 4.0)].groupby(by = ['country_code','city']).size().reset_index(name = 'quantidade de restaurantes')
    
    df_aux = df_aux.sort_values(['country_code','city'], ascending = [True, False])
    
    #Filtrar as três cidades com maior numero de restaurantes com notas acima de 4
    
    df_top_cities = df_aux.groupby('country_code').head(3)
    
    df_top_cities = df_top_cities.rename(columns = {'country_code':'países','restaurant_count':'quantidade de restaurantes', 'city':'cidades'})
    
    fig = px.bar(df_top_cities, x="cidades", y="quantidade de restaurantes", color='países', barmode='group',
                 title = 'Quantidade de Restaurantes Com Nota Média Acima de 4 por Cidade', text = 'quantidade de restaurantes')
    

    fig.update_traces(width=0.7)

    fig.update_layout(
    autosize=False,
    width=1000,
    height=500
    )

    return fig

def City_Restaurant_Agg_Rating_Less_2_5(df1):
    
    #Função para retornar as cidades com maior numero de restaurantes com nota media abaixo de 2.5
    
    df_aux = df1.loc[(df1['aggregate_rating'] < 2.5)].groupby(by = ['country_code', 'city']).size().reset_index(
    name = 'quantidade de restaurantes')
    
    df_aux = df_aux.sort_values(['country_code', 'city'], ascending = [True, False])
    
    df_top_cities = df_aux.groupby(by = ['country_code']).head(3)
    
    df_top_cities = df_top_cities.rename(columns = {'country_code':'países', 'city':'cidades'})
    
    fig = px.bar(df_top_cities, x = 'cidades', y = 'quantidade de restaurantes', color = 'países', barmode = 'group',
                title = 'Quantidade de Restaurantes com Nota Média Abaixo de 2.5', text = 'quantidade de restaurantes')
    
    fig.update_traces(width = 0.7)
    
    fig.update_layout(
    autosize = False,
    width = 1000,
    height = 500    
     )
    
    return fig


def City_Most_Expensive_Avg_Cost_Two(df1):
    
    #Função para retornar as cidades com maior valor medio de um prato para 2
    df_aux = df1.sort_values(by = ['country_code','average_cost_for_two','restaurant_id',
     'city'], ascending = [True, False, True, True ]).reset_index()[['country_code','average_cost_for_two','restaurant_id',
     'city']]
    
    df_aux2 = df_aux.groupby(by =['country_code']).head(1)
    
    df_aux2 = df_aux2.rename(columns = {'country_code':'países','city':'cidades',
                                        'average_cost_for_two':'valor médio de um prato para 2'})
    
    fig = px.bar(df_aux2,  x = 'cidades', y = 'valor médio de um prato para 2', color = 'países', barmode = 'group',
                title = 'Cidades com Maior Valor Médio de um Prato para 2', text = 'valor médio de um prato para 2')
    
    fig.update_traces(width = 0.7)
    
    fig.update_layout(
    autosize = False,
    width = 1000,
    height = 500
    )    
    
    return fig


def City_Different_Cuisines(df1):  
    df_aux = df1.groupby(by = ['country_code','city', 'cuisines']).count().reset_index()[
         ['country_code','city', 'cuisines',  'restaurant_id']]
   
    #Para cada tipo de culinaria atribuimos o valor 1
    df_aux['restaurant_id'] = 1
   
    #Agrupamos novamente por cidade e contamos as quantidades de culinarias,
    #sorteando da maior até a menor quantidade de culinarias distintas
    df_aux = df_aux.groupby(by = ['country_code','city']).count().sort_values(by =
    ['restaurant_id'], ascending = False).reset_index()[['country_code','city','restaurant_id']]


    df_aux2 = df_aux.sort_values(by = ['country_code','restaurant_id','city'], ascending=  [True,False,True ])

    df_aux2 = df_aux2.groupby(by =['country_code']).head(3)
    
    df_aux2 = df_aux2.rename(columns = {'country_code':'países','city':'cidades',
                                        'restaurant_id':'quantidade de restaurantes'})

    fig = px.bar(df_aux2,  x = 'cidades', y = 'quantidade de restaurantes', color = 'países', barmode = 'group',
                title = 'Cidades com Maior Quantidade de Culinárias Distintas', text = 'quantidade de restaurantes' )
    
    fig.update_traces(width = 0.7)
    
    fig.update_layout(
    autosize = False,
    width = 1000,
    height = 500
    )    
    
    return fig


def City_Has_Table_Booking(df1):
    #Função para retornar as cidades com maior volume de restaurantes que realizam reservas
    
    #A coluna has_table_booking informa se o restaurante realiza reservas

    #O para False e 1 para True

    df_aux = df1.loc[(df1['has_table_booking'] == 1)].groupby(['country_code', 'city']).size().reset_index(
    name = 'quantidade de restaurantes')
    
    df_aux2 = df_aux.sort_values(['country_code', 'quantidade de restaurantes'], ascending=[True, False])

# Filtrar as três cidades com o maior número de restaurantes para cada país
    df_top_cities = df_aux2.groupby('country_code').head(3)
    
    df_top_cities = df_top_cities.rename(columns = {'country_code': 'países','city':'cidades'})


    fig = px.bar(df_top_cities, x="cidades", y="quantidade de restaurantes", color='países', barmode='group',
                 title = 'Quantidade de Restaurantes que Realizam Reservas por Cidade', text = 'quantidade de restaurantes')
        
    
       
    fig.update_traces(width=0.7)

    fig.update_layout(
    autosize=False,
    width=1000,
    height=500
    )

    return fig



def Cities_Most_Restaurant_Delivery(df1):
    
    #Função que retorna as cidades com a maior quantidade de restaurantes que realizam entregas

    #A coluna is delivering now retorna 0 para False e 1 para True
    
    df_aux = df1.loc[(df1['is_delivering_now'] == 1)].groupby(['country_code', 'city']).size().reset_index(
    name = 'quantidade de restaurantes')
    
    df_aux2 = df_aux.sort_values(['country_code', 'quantidade de restaurantes'], ascending=[True, False])

# Filtrar as três cidades com o maior número de restaurantes para cada país
    df_top_cities = df_aux2.groupby('country_code').head(3)
    
    df_top_cities = df_top_cities.rename(columns = {'country_code': 'países','city':'cidades'})



    fig = px.bar(df_top_cities, x="cidades", y="quantidade de restaurantes", color='países', barmode='group',
                 title = 'Quantidade de Restaurantes que Fazem Entregas', text = 'quantidade de restaurantes')
        
    
       
    fig.update_traces(width=0.7)

    fig.update_layout(
    autosize=False,
    width=1000,
    height=500
    )

    return fig
    

def Cities_Most_Online_Delivery(df1):
#Função que retorna as cidades com a maior quantidade de restaurantes que aceitam pedidos online

#A coluna is delivering now retorna 0 para False e 1 para True
    
    df_aux = df1.loc[(df1['has_online_delivery'] == 1)].groupby(['country_code', 'city']).size().reset_index(
    name = 'quantidade de restaurantes')
    
    df_aux2 = df_aux.sort_values(['country_code', 'quantidade de restaurantes'], ascending=[True, False])

# Filtrar as três cidades com o maior número de restaurantes para cada país
    df_top_cities = df_aux2.groupby('country_code').head(3)
    
    df_top_cities = df_top_cities.rename(columns = {'country_code': 'países','city':'cidades'})



    fig = px.bar(df_top_cities, x="cidades", y="quantidade de restaurantes", color='países', barmode='group',
                 title = 'Quantidade de Restaurantes que Atendem Pedidos Online por Cidade', text = 'quantidade de restaurantes')
        
    
       
    fig.update_traces(width=0.7)

    fig.update_layout(
    autosize=False,
    width=1000,
    height=500
    )

    return fig
    


#Construindo as barras laterais

st.sidebar.markdown('# Fome Zero')

countries = df1['country_code'].unique()

#Definimos esses paises como default pois são os paises nos quais há maior numero de ocorrencias
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


#Plotando as informações

st.title("🗺️Visão Cidades")

tab1, tab2, tab3 = st.tabs(['Visão Geral', 'Visão Especifica','Quantidades de Restaurantes'])

with tab1: 

    with st.container():
        fig = City_More_Restaurants (df1)
        st.plotly_chart(fig, use_container_width = True)
        
    with st.container():
        fig = City_Different_Cuisines(df1)
        st.plotly_chart(fig, use_container_width=True) 
       
        
with tab2:
    
    with st.container():
        fig = City_Restaurant_Agg_Rating_4_More(df1)
        st.plotly_chart(fig, use_container_width = True)
      
    with st.container():
        fig = City_Restaurant_Agg_Rating_Less_2_5(df1)
        st.plotly_chart(fig, use_container_width=True)
        
    with st.container():
        fig = City_Most_Expensive_Avg_Cost_Two(df1)
        st.plotly_chart(fig, use_container_width = True)   
    
  
        

with tab3: 
    
    with st.container():
        fig = City_Has_Table_Booking(df1)
        st.plotly_chart(fig, use_container_width=True)
    
    with st.container():
        fig = Cities_Most_Restaurant_Delivery(df1)
        st.plotly_chart(fig, use_container_width=True)    
        
    with st.container():
        fig = Cities_Most_Online_Delivery(df1)
        st.plotly_chart(fig, use_container_width=True)    
        
        