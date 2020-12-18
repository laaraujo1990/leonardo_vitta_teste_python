# Teste tecnico Vitta
# Square of Squares (BE2) Versao: 2.0
# Dezembro/2012
# Leonardo Almeida de Araujo

import datetime
import mongoengine as me

# Implementacao de cada quadrado
class Square(me.Document):

  x = me.IntField(required=True)
  y = me.IntField(required=True)
  painted = me.BooleanField(default=False)
  last_update = me.DateTimeField()

  @staticmethod
  def generate_squares(start, end):

    left  = min(start['x'], end['x'])
    right = max(start['x'], end['x'])
    down  = min(start['y'], end['y'])
    up    = max(start['y'], end['y'])

    squares = []

    for x in range(right-left+1):
      for y in range(up-down+1):
        s = Square(x=left+x, y=down+y, painted=False)
        s.save()
        squares.append(s)

    return squares

  def serialize(self):

    return {
      'x': self.x,
      'y': self.y,
      'painted': self.painted
    }

  # Seta tempo
  def clean(self):

    self.last_update = datetime.datetime.now()

# Retorna ultimos quadrados pintados
def last_painted_squares(n):

  return Square.objects(painted=True).order_by('-last_update')[0:n]
