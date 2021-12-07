from datetime import datetime

from icecream import ic
import os

from konlpy.tag import Okt

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")
import django
django.setup()
from userlog.models import UserLog


class Routine:
    def __init__(self):
        pass

    def process(self):
        log = self.load_data()[1]
        location, day, time, contents = self.extract_keyword(log)
        # self.check_location(location)
        # self.check_day(day)
        self.check_time(time)

    def load_data(self):
        today = datetime.now().date()
        log = list(UserLog.objects.filter(log_date__year=today.year,
                                          log_date__month=today.month,
                                          log_date__day=today.day).values())
        # print(log)
        return log

    def extract_keyword(self, log):
        week = ['월', '화', '수', '목', '금', '토', '일']
        location = log['location']
        day = week[log['log_date'].weekday()]
        time = log['log_date'].hour
        full_texts = log['contents']
        contents = []
        for i in Okt().pos(full_texts):
            if i[1] == 'Noun':
                contents.append(i[0])
        return location, day, time, contents

    def check_location(self, location):
        ls = []
        all = UserLog.objects.all().filter(location=location).values()
        [ls.append(i['id']) for i in all]
        print(ls)
        return ls

    def check_day(self, day):
        week = ['월', '화', '수', '목', '금', '토', '일']
        ls = []
        all = UserLog.objects.all().values()
        [ls.append(i['id']) for i in all if week[i['log_date'].weekday()] == day]
        print(ls)
        return ls

    def check_time(self, time):
        # 이건 좀더 정확도를 위해
        ls = []
        all = UserLog.objects.all().filter(log_date__hour=time).values()
        [ls.append(i['id']) for i in all]
        print(ls)
        return ls

    def check_contents(self, contents):
        ls = []
        all = [UserLog.objects.all().filter(contents__in=i).values() for i in contents]
        [ls.append(i['id']) for i in all]
        # 컨텐츠 만들기

    def make_routine(self):
        pass



if __name__ == '__main__':
    r = Routine()
    r.process()