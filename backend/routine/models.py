from datetime import datetime

from django.db import models
from django.db.models import IntegerField, CharField
from django_mysql.models import ListTextField


# Create your models here.


class Routine(models.Model):
    create_date = models.DateTimeField(default=datetime.now())
    log_repeat = models.IntegerField()
    # event_repeat = models.IntegerField()
    priority = models.IntegerField()
    grade = models.IntegerField()
    contents = models.TextField()
    location = models.TextField()
    cron = ListTextField(base_field=CharField())
    days = ListTextField(base_field=CharField())
    hours = ListTextField(base_field=CharField())
    # event_id = models.IntegerField()
    log_id = ListTextField(base_field=IntegerField())      # fk
    user_id = models.IntegerField()     # fk

    class Meta:
        db_table = 'routine'

    def __str__(self):
        return f'{self.pk}'