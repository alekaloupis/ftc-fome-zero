# ftc-fome-zero
This repository contains files and scripts to build a company strategy dashboard

Projeto desenvolvido para a conclusão da disciplina de FTC - Analisando Dados com Python da Comunidade DS

# 1.	Problema de negócio 

A empresa Fome Zero é uma marketplace de restaurantes. Ou seja, seu core business é facilitar o encontro e negociações de clientes e restaurantes. Os restaurantes fazem o cadastro dentro da plataforma da Fome Zero, que disponibiliza informações como endereço, tipo de culinária servida, se possui reservas, se faz entregas e, também, uma nota de avaliação dos serviços e produtos do restaurante, dentre outras informações.
O CEO Guerra também foi recém-contratado e precisa entender melhor o negócio para conseguir tomar as melhores decisões estratégicas e alavancar ainda mais a Fome Zero e, para isso, ele precisa que seja feita uma análise nos dados da empresa e que sejam gerados dashboards, a partir dessas análises, para responder às seguintes perguntas:

## Geral

1. Quantos restaurantes únicos estão registrados?
2. Quantos países únicos estão registrados?
3. Quantas cidades únicas estão registradas?
4. Qual o total de avaliações feitas?
5. Qual o total de tipos de culinária registrados?

## País

1. Qual o nome do país que possui mais cidades registradas?
2. Qual o nome do país que possui mais restaurantes registrados?
3. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4 registrados?
4. Qual o nome do país que possui a maior quantidade de tipos de culinária distintos?
5. Qual o nome do país que possui a maior quantidade de avaliações feitas?
6. Qual o nome do país que possui a maior quantidade de restaurantes que fazem entrega?
7. Qual o nome do país que possui a maior quantidade de restaurantes que aceitam reservas?
8. Qual o nome do país que possui, na média, a maior quantidade de avaliações registrada?
9. Qual o nome do país que possui, na média, a maior nota média registrada?
10. Qual o nome do país que possui, na média, a menor nota média registrada?
11. Qual a média de preço de um prato para dois por país?

## Cidade

1. Qual o nome da cidade que possui mais restaurantes registrados?
2. Qual o nome da cidade que possui mais restaurantes com nota média acima de 4?
3. Qual o nome da cidade que possui mais restaurantes com nota média abaixo de 2.5?
4. Qual o nome da cidade que possui o maior valor médio de um prato para dois?
5. Qual o nome da cidade que possui a maior quantidade de tipos de culinárias distintas?
6. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem reservas?
7. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem entregas?
8. Qual o nome da cidade que possui a maior quantidade de restaurantes que aceitam pedidos online?

## Restaurantes

1. Qual o nome do restaurante que possui a maior quantidade de avaliações?
2. Qual o nome do restaurante com a maior nota média?
3. Qual o nome do restaurante que possui o maior valor de um prato para duas pessoas?
4. Qual o nome do restaurante de tipo de culinária brasileira que possui a menor
média de avaliação?
5. Qual o nome do restaurante de tipo de culinária brasileira, e que é do Brasil, que possui a maior média de avaliação?
6. Os restaurantes que aceitam pedido online são também, na média, os restaurantes que mais possuem avaliações registradas?
7. Os restaurantes que fazem reservas são também, na média, os restaurantes que possuem o maior valor médio de um prato para duas pessoas?
8. Os restaurantes do tipo de culinária japonesa dos Estados Unidos da América
possuem um valor médio de prato para duas pessoas maior que as churrascarias
americanas (BBQ)?

## Tipos de Culinária

1. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a maior média de avaliação?
2. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a menor média de avaliação?
3. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a maior média de avaliação?
4. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a menor média de avaliação?
5. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do restaurante com a maior média de avaliação?
6. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do restaurante com a menor média de avaliação?
7. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do restaurante com a maior média de avaliação?
8. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do
restaurante com a menor média de avaliação?
9. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do
restaurante com a maior média de avaliação?
10. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do
restaurante com a menor média de avaliação?
11. Qual o tipo de culinária que possui o maior valor médio de um prato para duas pessoas?
12. Qual o tipo de culinária que possui a maior nota média?
13. Qual o tipo de culinária que possui mais restaurantes que aceitam pedidos
online e fazem entregas?

# 2.	Premissas assumidas para a análise

O Marketplace foi o modelo de negócio assumido

A partir das perguntas levantadas pelo CEO, as análises foram segmentadas em: a) visão geral; b) visão países; c) visão cidade; d) visão restaurantes/culinárias.

A última atualização da base é do ano de 2019

# 3.	Estratégia da solução

A manipulação das análises e métricas presentes no painel possibilitam uma resposta a todas as perguntas levantadas pelo CEO.

O painel estratégico foi desenvolvido utilizando as métricas que refletem as 4 principais visões do modelo de negócio da empresa: 

## Visão Geral
## Visão Países
## Visão Cidades
## Visão Restaurantes/Culinárias

### Cada visão é representada pelo seguinte conjunto de métricas:


## Visão Geral

a)	Quantidade de restaurantes únicos cadastrados;

b)	Quantidade de países únicos;

c)	Quantidade de cidades únicas;

d)	Quantidade de tipo de culinárias oferecidas;

e)	Quantidade de avaliações feitas na plataforma;

## Visão Países

a)	Quantidade de cidades por país;

b)	Quantidade de restaurantes por país;

c)	Quantidade de tipos de culinária por país;

d)	Quantidade de avaliações feitas por país;

e)	Média das quantidades de avaliações por país;

f)	Quantidade de restaurantes gourmet por país;

g)	Quantidade de restaurantes que fazem entregas por país;

h)	Quantidade de restaurantes que fazem reservas por país;

i)	Média das avaliações por país;

j)	Média de preço de um prato para dois por país

## Visão Cidades

a)	Quantidade de restaurantes por cidade;

b)	Quantidade de cidades com maior quantidade de culinárias distintas;

c)	Quantidade de restaurantes com nota média acima de 4 por cidade;

d)	Quantidade de restaurantes com nota média abaixo de 2,5 por cidade;

e)	Cidades com maior valor médio de um prato para 2;

f)	Quantidade de restaurantes que realizam reservas por cidade;

g)	Quantidade de restaurantes que fazem entregas por cidade;

h)	Quantidade de restaurantes que atendem pedidos online por cidade

## Visão Restaurantes/Culinárias

a)	Restaurantes com maior quantidade de avaliações feitas;

b)	Restaurantes com maior nota média de avaliação; 

c)	Restaurantes com maior valor médio de um prato para 2; 

d)	Quantidade de avaliações filtrados a partir de países, tipos de culinária, realizam reservas (sim ou não), realizam entregas (sim ou não), atendem pedidos online (sim ou não);

e)	Média do valor de um prato para 2 pessoas filtrados a partir de países, tipos de culinária, realizam reservas (sim ou não), realizam entregas (sim ou não), atendem pedidos online (sim ou não);

f)	Quantidade de restaurantes filtrados a partir de países, tipos de culinária, realizam reservas (sim ou não), realizam entregas (sim ou não), atendem pedidos online (sim ou não);

g)	Tipos de culinária e nota média de avaliação; 

h)	Tipos de culinária e valor médio de um prato para duas pessoas; 

# 4.	O produto final do projeto

Painel online, hospedado em um Cloud e disponível para acesso em qualquer dispositivo conectado à internet.
O painel pode ser acesso através desse link: https://alekaloupis-ftc-fome-zero-home-4luhgr.streamlit.app/

# 5.	Conclusão

O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas que exibam essas métricas da melhor forma possível para o CEO. 
Enquanto visão geral e inicial, o produto de dados aqui produzido cumprirá o objetivo de introduzir/familiarizar a liderança empresarial com o negócio a ser liderado.

