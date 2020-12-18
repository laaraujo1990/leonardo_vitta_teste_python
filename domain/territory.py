# Teste tecnico Vitta
# Square of Squares (BE2) Versao: 2.0
# Dezembro/2012
# Leonardo Almeida de Araujo

import functools
import mongoengine as me
from mongoengine.queryset.visitor import Q
from domain import square as sq

# Implementaco de territorio
class Territory(me.Document):

  id = me.SequenceField(primary_key=True)
  name = me.StringField(required=True)
  start = me.DictField(required=True)
  end = me.DictField(required=True)
  area = me.FloatField(default=0.)
  painted_area = me.IntField(default=0)
  squares = me.ListField(me.ReferenceField(sq.Square))

  # Verifica sobreposicao do territorio
  # Calcula atributos da area
  def clean(self):

    if self.overlapping_territories():
      raise me.ValidationError('Overlapping territory')
    self.area = self.calculate_area()
    self.painted_area = self.calculate_painted_area()
    if len(self.squares) == 0:
      self.squares = sq.Square.generate_squares(self.start, self.end)

  def overlapping_territories(self):

    self_left  = min(self.start['x'], self.end['x'])
    self_right = max(self.start['x'], self.end['x'])
    self_down  = min(self.start['y'], self.end['y'])
    self_up    = max(self.start['y'], self.end['y'])

    for t in Territory.objects:

      t_left  = min(t.start['x'], t.end['x'])
      t_right = max(t.start['x'], t.end['x'])
      t_down  = min(t.start['y'], t.end['y'])
      t_up    = max(t.start['y'], t.end['y'])

      overlap = not ((self_left > t_right) or (self_right < t_left)
		  or (self_up   < t_down ) or (self_down  > t_up  ))

      if overlap:
        return True

    return False

  def calculate_area(self):

    delta_x = abs(self.start['x'] - self.end['x'])# + 1
    delta_y = abs(self.start['y'] - self.end['y'])# + 1
    return delta_x * delta_y

  def calculate_painted_area(self):
    
    return len(self.painted_squares())

  def painted_squares(self):
    
    return [s for s in self.squares if s.painted is True]

  def serialize(self, include_squares=False):

    _dict = {
	    'id': str(self.id),
	    'name': self.name,
	    'start': self.start,
	    'end': self.end,
	    'area': self.area,
	    'painted_area': self.calculate_painted_area()
	   }

    if include_squares:
      _dict['painted_squares'] = [{'x': s.x, 'y': s.y} for s in self.painted_squares()]

    return _dict

  @classmethod
  def post_delete(cls, sender, document, **kwargs):

    for s in document.squares:
      s.delete()

me.signals.post_delete.connect(Territory.post_delete, sender=Territory)

def territories_by_painted_area():

  territories = Territory.objects

  return sorted(territories, key=lambda x: x.calculate_painted_area(),
		reverse=True)

def territories_by_proportional_painted_area():

  territories = Territory.objects

  return sorted(territories, key=lambda x: x.calculate_painted_area() / x.area,
		reverse=True)

def total_proportional_painted_area():

  territories = Territory.objects
  painted_areas = [t.calculate_painted_area() for t in territories]
  total_painted = sum(painted_areas)
  total_area = sum([t.area for t in territories])
  if total_area == 0:
    total_area = 1

  return total_painted / total_area
