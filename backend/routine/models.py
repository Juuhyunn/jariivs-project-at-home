from datetime import datetime

from django.db import models

# Create your models here.


class Routine(models.Model):
    create_date = models.DateTimeField(default=datetime.now())
    log_repeat = models.IntegerField()
    event_repeat = models.IntegerField()
    priority = models.IntegerField()
    grade = models.IntegerField()
    contents = models.TextField()
    cron = models.TextField()
    event_id = models.IntegerField()
    log_id = models.ForeignKey("userlog.UserLog", on_delete=models.CASCADE, db_column='log_id')      # fk
    user_id = models.IntegerField()     # fk

    class Meta:
        db_table = 'routine'

    def __str__(self):
        return f'{self.pk}'