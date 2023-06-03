import streamlit as st

st.set_page_config(    
page_title = 'Home',
layout = 'wide'
    
)

st.sidebar.markdown("# Fome Zero")
st.sidebar.markdown("___")
                    
st.write("# Fome Zero Dashboard")
                    
st.markdown(

"""
    Dashboard Fome Zero foi construído para acompanhar informações sobre restaurantes
    e as experiências de seus usuários.
    
    Seguem abaixo informações sobre a utilização desse Dashboard
    
    - Visão Geral:
    
        Aspectos gerais dos restaurantes cadastrados e mapa de localização dos mesmos
        
    - Visão Países: 
        
        Visão geral e específica sobre os países que possuem restaurantes cadastrados na base de dados.
        
        Constam informações como: quantidade de restaurantes, de cidades, de avaliações feitas, dentre outras
        
    - Visão Cidades: 
        
        Visão geral e específica sobre as cidades cadastradas na base de dados, tais como quantidade de restaurantes,
        de culinárias cadastradas por cidade.
        
        As informações são filtradas por avaliação feita, característica dos restaurantes, etc.
        
   - Visão Restaurantes/Culinárias:
   
       Visão geral e específica sobre os restaurantes e os tipos de culinárias cadastrados na base de dados
       
       As informações são filtradas por: características dos restaurantes, tipo de culinária, países cadastrados dentre outras
    
    
"""
)                    
                    