# Teste tecnico Vitta
# Square of Squares (BE2) Versao: 2.0
# Dezembro/2012
# Leonardo Almeida de Araujo

from flask import Flask, request, jsonify, redirect, url_for
from domain import territory, square, app_error
import mongoengine as me
import view_helper as vh

app = Flask(__name__)

me.connect('vitta-challenge', host='mongodb://mongo', port=27017)

# Home
@app.route('/', methods=['GET'])
def root_get(): 
  html = '<html><head></head><body>'
  html += 'Teste tecnico Vitta <br />'
  html += 'Square of Squares (BE2) Versao: 2.0 <br />'
  html += 'Dezembro/2012 <br />'
  html += 'Leonardo Almeida de Araujo <br />'
  html += '<p> HOME </p> '
  html += '<p> Endereço localhost:5000 </p>'
  html += '/territories : Lista todos territorios (GET) <br />'
  html += '/territories : Adiciona territorios (POST) <br />'
  html += '/territories/<_id> : Deletar territorios (DELETE) <br />'
  html += '/territories/<_id> : Listar territorios por id (GET) <br />'
  html += '/territories/<_id> ? withpainted={false|true} : Listar todos quadrados pintados de um territorio (GET)<br />'
  html += '/squares/<_x>/<_y> : Listar quadrado (GET) <br />'
  html += '/squares/<_x>/<_y>/paint : Pintar quandrado (PATCH) <br />'
  html += '/dashboard : Visualizar relatorio de resultado (GET) <br />'
  html += '</body></html>'
  return html

# Cria territorios
@app.route('/territories', methods=['POST'])
def create_territory():
  try:
    data = request.get_json()
    name = data['name']
    start = data['start']
    end = data['end']
    t = territory.Territory(name=name, start=start, end=end)
    t.save()
    return jsonify(data=t.serialize(), error=False)

  except KeyError:
    e = app_error.AppError(type='territories/incomplete-data')
    e.save()
    return redirect(url_for('static', filename='territories/incomplete-data.html'))

  except me.ValidationError:
    e = app_error.AppError(type='territories/territory-overlay')
    e.save()
    return redirect(url_for('static', filename='territories/territory-overlay.html'))

# Lista territorios  
@app.route('/territories', methods=['GET'])
def list():
  tlist = territory.Territory.objects 
  return jsonify(count=len(tlist), data=[t.serialize() for t in tlist])

# Deleta territorio
@app.route('/territories/<_id>', methods=['DELETE'])
def delete(_id):
  try:
    obj = territory.Territory.objects(id=_id)[0]
    obj.delete()
    return jsonify(error=False)

  except IndexError:
    e = app_error.AppError(type='territories/not-found')
    e.save()
    return redirect(url_for('static', filename='territories/not-found.html'))

# Busca territorio
@app.route('/territories/<_id>', methods=['GET'])
def find(_id):
  try:
    withpainted = request.args.get('withpainted')
    if withpainted == 'true':
      include_squares = True
    else:
      include_squares = False
    obj = territory.Territory.objects(id=_id)[0].serialize(include_squares=include_squares)
    return jsonify(data=obj, error=False)

  except IndexError:
    e = app_error.AppError(type='territories/not-found')
    e.save()
    return redirect(url_for('static', filename='territories/not-found.html'))

# Busca quadrado
@app.route('/squares/<x>/<y>', methods=['GET'])
def find_square(x, y):
  try:
    obj = square.Square.objects(x=x, y=y)[0].serialize()
    return jsonify(data=obj, error=False)
  
  except IndexError:
    e = app_error.AppError(type='squares/not-found')
    e.save()
    return redirect(url_for('static', filename='squares/not-found.html'))

# Pinta quadrado
@app.route('/squares/<x>/<y>/paint', methods=['PATCH'])
def paint_square(x, y):
  try:
    obj = square.Square.objects(x=x, y=y)[0]
    obj.painted = True
    obj.save()
    return jsonify(data=obj.serialize(), error=False)

  except IndexError:
    e = app_error.AppError(type='squares/not-found')
    e.save()
    return redirect(url_for('static', filename='squares/not-found.html'))

# Apresenta relatorio final
@app.route('/dashboard', methods=['GET'])
def dashboard():
  html = '<html><head></head><body>'
  html += 'DASHBOARD - Relatorio Final'
  html += '<p> Lista de territorios ordenados pela área mais pintada: '
  html += vh.territories_by_painted_area()
  html += '</p>'
  html += '<p> Lista de territorios ordenados por área pintada mais proporcional: '
  html += vh.territories_by_proportional_painted_area()
  html += '</p>'
  html += '<p> Lista dos ultimos 5 quadrados pintados: '
  html += vh.last_painted_squares(5)
  html += '</p>'
  html += '<p> Lista dos ultimos 5 erros: '
  html += vh.last_errors(5)
  html += '</p>'
  html += '<p> Area pintada / área total : '
  html += '%.2f %%' % (territory.total_proportional_painted_area()*100)
  html += '</p>'
  html += '</body></html>'
  return html

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
