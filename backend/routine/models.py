from datetime import datetime

from django.db import models
from django.db.models import IntegerField
from django_mysql.models import ListTextField


# Create your models here.


class Routine(models.Model):
    create_date = models.DateTimeField(default=datetime.now())
    log_repeat = models.IntegerField()
    # event_repeat = models.IntegerField()
    priority = models.IntegerField()
    grade = models.IntegerField()
    contents = ListTextField(base_field=IntegerField(), size=100,)
    cron = ListTextField(base_field=IntegerField(), size=100,)
    # event_id = models.IntegerField()
    log_id = ListTextField(base_field=IntegerField(), size=100,)      # fk
    user_id = models.IntegerField()     # fk

    class Meta:
        db_table = 'routine'

    def __str__(self):
        return f'{self.pk}'