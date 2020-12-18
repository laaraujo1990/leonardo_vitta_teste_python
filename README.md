# vitta-challenge
Desafio tecnico de programação - Versao 2.0 - Leonardo Araujo

# Enunciado
https://github.com/vitta-hiring/case-back-end/tree/master/challenges/2-SquareOfSquares

# App
Aplicacao: Python
Microservico: Flask
Banco de dados: Mongo
Container: Docker

# Para rodar a aplicacao
Comando para subir a aplicacao:
*sudo docker-compose up*

Comando para finalizar a aplicacao:
*sudo docker-compose down --volumes*

# Funcionalidades
Endereço localhost:5000
Rotas:
- / : Home (GET)
- /territories : Lista todos territorios (GET)
- /territories : Adiciona territorios (POST)
- /territories/<_id> : Deletar territorios (DELETE)
- /territories/<_id> : Listar territorios por id (GET)
- /territory/<_id> ? withpainted={false|true} : Listar todos quadrados pintados de um territorio
- /squares/<_x>/<_y> : Listar quadrado (GET)
- /squares/<_x>/<_y>/paint : Pintar quandrado (PATCH)
- /dashboard : Visualizar relatorio de resultado (GET)

# Relatorio final
localhost:5000/dashboard
- Lista de territorios ordenados pela área mais pintada.
- Lista de territorios ordenados por área pintada mais proporcional.
- Lista dos ultimos 5 quadrados pintados.
- Lista dos ultimos 5 erros.
- Area pintada / área total (de todas as areas e territorios)
