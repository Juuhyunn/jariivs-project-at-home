from icecream import ic
import os
from datetime import datetime
from konlpy.tag import Okt


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")
import django
django.setup()
from userlog.models import UserLog
from routine.models import Routine

class Flower:
    def __init__(self):
        pass

    def process(self, user_id):
        # Getting ALL of today logs
        today = datetime.now().date()
        today_routines = list(Routine.objects.filter(create_date__year=today.year,
                                                 create_date__month=today.month,
                                                 create_date__day=today.day,
                                                 user_id=user_id).values())
        for routine in today_routines:
            create_date = models.DateTimeField(auto_now_add=True)
            update_date = models.DateTimeField(auto_now=True)
            title = models.TextField()
            grade = models.IntegerField()
            step = models.IntegerField()
            shape = models.TextField()
            log_id = ListTextField(base_field=IntegerField(), null=True)
            event_id = ListTextField(base_field=IntegerField(), null=True)
            user_id





    def create_flower(self):
        pass

    def update_flower(self):
        pass

    def upgrade(self):
        pass

    def counting_step(self):
        pass