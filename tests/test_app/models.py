from django.db import models
from datetime import datetime

class TestModel(models.Model):
    date = models.DateField(default=datetime.today())
