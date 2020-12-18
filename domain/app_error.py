# Teste tecnico Vitta
# Square of Squares (BE2) Versao: 2.0
# Dezembro/2012
# Leonardo Almeida de Araujo

import datetime
import mongoengine as me

# Implementa avisos de erros
class AppError(me.Document):

  type = me.StringField(required=True)
  timestamp = me.DateTimeField()

  # Seta tempo
  def clean(self):

    self.timestamp = datetime.datetime.now()

  def serialize(self):

    return str(self.type)

# Retorna ultimos erros
def last_errors(n):

  return AppError.objects.order_by('-timestamp')[0:n]
