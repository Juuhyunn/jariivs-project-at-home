import os

from icecream import ic
from konlpy.tag import Okt

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")
import django
django.setup()
from datetime import datetime

from django.test import TestCase

# Create your tests here.
from userlog.models import UserLog


class RoutineTest:
    def __init__(self):
        pass

    def process(self):
        today = datetime.now().date()
        today_log = list(UserLog.objects.filter(log_date__year=today.year,
                                          log_date__month=today.month,
                                          log_date__day=today.day).values())
        # checking similar routine
        for log in today_log:
            location = log['location']
            # day = log['log_date'].weekday()
            # time = log['log_date'].hour
            full_texts = log['contents']
            contents = []
            cron = [0, 0, log['log_date'].hour, 0, 0, log['log_date'].weekday()]
            grade = 0
            for i in Okt().pos(full_texts):
                if i[1] == 'Noun':
                    contents.append(i[0])
            ic(f'location : {location}')
            # ic(f'day : {day}')
            # ic(f'time : {time}')
            ic(f'cron : {cron}')
            ic(f'full_texts : {full_texts}')
            ic(f'contents : {contents}')

            # checking similar contents
            similar_contents = []
            similar_contents_id = []
            for content in contents:
                similar_contents.append({content: list(UserLog.objects.filter(contents__icontains=content).values())})
                [similar_contents_id.append(i['id']) for i in UserLog.objects.filter(contents__icontains=content).values() if i['id'] != log['id']]
            print(f'***** similar_contents_id : {similar_contents_id}')
            # print(f'** similar_contents : ')
            # [print(i) for i in similar_contents]

            # checking similar location
            similar_location = {location: list(UserLog.objects.filter(location=location).values())}
            similar_location_id = []
            [similar_location_id.append(i["id"]) for i in similar_location[location] if i['id'] != log['id']]
            print(f'***** similar_location_id : {similar_location_id}')
            # print(f'** similar_location : ')
            # [print(i) for i in similar_location[location]]

            for i in similar_contents_id:
                for j in similar_location_id:
                    test = UserLog.objects.filter(pk=j).values()[0]
                    print(f'test : {test}')
                    test_date = test['log_date']
                    test_cron = [0, 0, test['log_date'].hour, 0, 0, test['log_date'].weekday()]
                    if i == j:
                        grade = grade + 1
                        if test_cron[2] == cron[2]:
                            # [[case 1]] contents + location + cron == 3
                            grade = grade + 2
                            print('[[case 1]] contents + location + cron')
                            print(f'cron : {cron}')
                            print(f'test_cron : {test_cron}')
                            # checking weekday
                            if test_cron[5] == cron[5]:
                                grade = grade + 1
                        elif cron[2]-2 < test_cron[2] < cron[2]+2:
                            # [[case 1]] contents + location + cron == 2
                            grade = grade + 1
                            print('[[case 1]] contents + location + cron (2시간 정도 여유)')
                            print(f'cron : {cron}')
                            print(f'test_cron : {test_cron}')
                            # checking weekday
                            if test_cron[5] == cron[5]:
                                grade = grade + 1
                        else:
                            # [[case 2]] contents + location == 1
                            print('[[case 2]] contents + location')
                            cron[2] = 0
                            print(f'cron : {cron}')
                            print(f'test_cron : {test_cron}')
                    else:
                        pass
                        # [[case 4]] location + cron == 1
                        # if test_cron[2] != cron[2]:
                        #     cron[2] = 0
                        # print(f'cron : {cron}')
                        # print(f'test_cron : {test_cron}')
                    # [[case 3]] contents + cron
                    pass

            print(f'grade : {grade}')
            # checking similar cron
            # similar_day = {location: list(UserLog.objects.filter(location=location).values())}
            # print(f'** similar_location : ')
            # [print(i) for i in similar_location[location]]


if __name__ == '__main__':
    r = RoutineTest()
    r.process()

