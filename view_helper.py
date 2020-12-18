# Teste tecnico Vitta
# Square of Squares (BE2) Versao: 2.0
# Dezembro/2012
# Leonardo Almeida de Araujo

from domain import territory, square, app_error

# Lista de territorios ordenados pela área mais pintada
def territories_by_painted_area():
  sorted_territories = territory.territories_by_painted_area()
  html = '<ol>'
  for t in sorted_territories:
    html += '<li>' + str(t.serialize()) + '</li>'
  html += '</ol>'
  return html 

# Lista de territorios ordenados por área pintada mais proporcional
def territories_by_proportional_painted_area():
  sorted_territories = territory.territories_by_proportional_painted_area()
  html = '<ol>'
  for t in sorted_territories:
    html += '<li>' + str(t.serialize()) + '</li>'
  html += '</ol>'
  return html 

# Lista dos ultimos 5 quadrados pintados
def last_painted_squares(n):
  squares = square.last_painted_squares(n)
  html = '<ol>'
  for s in squares:
    html += '<li>' + str(s.serialize()) + '</li>'
  html += '</ol>'
  return html

# Lista dos ultimos 5 erros
def last_errors(n):
  errors = app_error.last_errors(n)
  html = '<ol>'
  for e in errors:
    html += '<li>' + str(e.serialize()) + '</li>'
  html += '</ol>'
  return html
