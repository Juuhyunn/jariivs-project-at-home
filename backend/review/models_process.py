from datetime import datetime

import requests
from icecream import ic
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")
import django
django.setup()
from userlog.models import UserLog


class Review:
    def __init__(self):
        pass

    def process(self):
        pass

    def load_data(self, log_id):
        today = datetime.now().date()
        log = list(UserLog.objects.filter(log_date__year=today.year,
                                     log_date__month=today.month,
                                     log_date__day=today.day).values())
        # server = '혬띠 서버랑 포트를 넣어보쟈'
        # url = 'api/event/detail/list/'
        # params = '뀨?'
        # event = requests.get(url, params=params)
        event = [{"event_id":1,
                 "user" : "fk",
                 "created" : "20211120",
                 "update " : "20211121",
                 "Classification": "DEV",
                 "type":"suggestion",
                 "title" : "일정11111",
                 "start" : "2021-11-23",
                 "end" : "2021-11-25",
                 "location" : "서울",
                 "description":"test333"
                 },{"event_id":1,
                 "user" : "fk",
                 "created" : "20211120",
                 "update " : "20211121",
                 "Classification": "DEV",
                 "type":"suggestion",
                 "title" : "일정11111",
                 "start" : "2021-11-23",
                 "end" : "2021-11-25",
                 "location" : "서울",
                 "description":"test333"
                 }]
        # log = list(UserLog.objects.filter(log_date__year=2021,
        #                                   log_date__month=11,
        #                                   log_date__day=19).values())

        ic(log)
        ic(event)

    def extract_keyword(self):
        pass

    def check_complete(self):
        pass


    def check_grade(self):
        pass

    def make_cron(self):
        pass


if __name__ == '__main__':
    r = Review()
    r.load_data(5)