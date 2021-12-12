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

    def process(self, user_id):
        # Getting ALL of today logs
        # today = datetime.now().date()
        # all_today = list(UserLog.objects.filter(log_date__year=today.year,
        #                                         log_date__month=today.month,
        #                                         log_date__day=today.day,
        #                                         user_id=user_id).values())
        # 임시 데이터
        all_today = list(UserLog.objects.filter(log_date__year=2021,
                                                log_date__month=12,
                                                log_date__day=12,
                                                user_id=user_id).values())
        print(all_today)
        '''
            {
            'id': 6,
            'location': '비트캠프',
            'address': '서울 강남구 강남대로94길 20',
            'x': '127.029037792462',
            'y': '37.4994078625536',
            'log_date': datetime.datetime(2021, 12, 12, 17, 4, 1, 85772, tzinfo=<UTC>),
            'weather': '맑음',
            'log_type': 'study',
            'contents': '열심히 파이썬 개발 공부를 했다.',
            'user_id': 1
            }
        '''
        # Getting ALL of Routines
        # all_routine = list(UserLog.objects.filter(user_id=user_id).values())
        # 임시 데이터
        all_routine = [{'log_repeat' : 0,
                        'priority': 0,
                        'grade': 0,
                        'location': '비트캠프',
                        # 'contents': "맛있게 점심 약속",
                        # 'contents': "파이썬 개발 공부",
                        'contents': "열심히 파이썬 공부",
                        'cron': ["", "", "10", "", "", "fri"],
                        'days': ["fri","sun"],
                        'hours': ["10"],
                        'log_id': [],
                        'user_id': 1
                        }]
        days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        # Checking log
        for log in all_today:
            ic('***** Checking log *****')
            log_id = log['id']
            location = log['location']
            day = days[log['log_date'].weekday()]
            time = log['log_date'].hour
            full_texts = log['contents']
            contents = []
            # cron = [0, 0, log['log_date'].hour, 0, 0, {days[log['log_date'].weekday()]: 1}]
            # grade = 0
            for i in Okt().pos(full_texts):
                if i[1] == 'Noun':
                    contents.append(i[0])
            ic(f'log_id : {log_id}')
            ic(f'location : {location}')
            ic(f'day : {day}')
            ic(f'time : {time}')
            # ic(f'cron : {cron}')
            ic(f'full_texts : {full_texts}')
            ic(f'contents : {contents}')
            # Comparing Routine
            for routine in all_routine:
                grade = 0
                # Comparing Contents
                routine_contents = routine['contents'].split(' ')
                new_contents = []
                ic(f' rotine_contents :: {routine_contents}')
                [[new_contents.append(lc) for rc in routine_contents if lc == rc] for lc in contents]
                ic(f'new_contents :: {new_contents}')
                # Perfect Matching
                if len(new_contents) == len(routine_contents) or len(new_contents) >= len(routine_contents)/2:
                    grade += 2
                    # Comparing location
                    # [case 1] contents + location + cron
                    if location == routine['location']:
                        grade += 1
                        # grade = self.checking_cron(routine, day, grade, time, days, log)
                        # cron_time = int(routine['cron'][2])
                        # Comparing day
                        if routine['cron'][5].find(day) > -1:
                            grade += 1
                        # Comparing time
                        if time == int(routine['cron'][2]):
                            grade += 2
                        elif int(routine['cron'][2]) - 1 <= time <= int(routine['cron'][2]) + 1:
                            grade += 1
                        elif int(routine['cron'][2]) == 23:
                            if routine['cron'].find(days[log['log_date'].weekday() + 1]) > -1 and time == 0:
                                grade += 1
                        elif int(routine['cron'][2]) == 0:
                            if routine['cron'].find(days[log['log_date'].weekday() - 1]) > -1 and time == 23:
                                grade += 1
                        ic('***** 변경 전 *****')
                        ic(routine)
                        routine['log_repeat'] += 1
                        routine['grade'] += grade
                        routine['days'].append(day)
                        routine['hours'].append(time)
                        routine['log_id'].append(log_id)
                        print(f"routine['grade'] :: {routine['grade']}")
                        print(f"routine['log_repeat'] :: {routine['log_repeat']}")
                        routine['priority'] = routine['grade'] + routine['log_repeat']
                        # routine['cron'] = ["", "", "", "", "", ""]
                        for t in set(routine['hours']):
                            if routine['cron'][2].find(str(t)) == -1:
                                if routine['hours'].count(t) >= routine['hours'].count(max(routine['days'], key=routine['days'].count)):
                                    routine['cron'][2] = f"{routine['cron'][2]},{t}"
                        for t in set(routine['days']):
                            if routine['cron'][2].find(str(t)) == -1:
                                if routine['days'].count(t) >= routine['days'].count(max(routine['days'], key=routine['days'].count)):
                                    routine['cron'][5] = f"{routine['cron'][5]},{t}"
                        ic('***** 변경 후 *****')
                        ic(routine)
                        # update routine
                else:
                    # new routine
                    pass
                #
                # # Halfway Matching
                # elif len(new_contents) >= len(routine_contents)/2:
                #     grade += 1
                #     # Comparing location
                #     # [case 2] contents(반 이상) + location + cron
                #     if location == routine['location']:
                #         grade += 1
                #         grade = self.checking_cron(routine, day, grade, time, days, log)
                #         ic('***** 변경 전 *****')
                #         ic(routine)
                #         routine['log_repeat'] += 1
                #         routine['grade'] += grade
                #         routine['days'].append(day)
                #         routine['hours'].append(time)
                #         routine['log_id'].append(log_id)
                #         print(f"routine['grade'] :: {routine['grade']}")
                #         print(f"routine['log_repeat'] :: {routine['log_repeat']}")
                #         routine['priority'] = routine['grade'] + routine['log_repeat']
                #         # routine['cron'] = ["", "", "", "", "", ""]
                #         for t in set(routine['hours']):
                #             if routine['cron'][2].find(str(t)) == -1:
                #                 if routine['hours'].count(t) >= routine['hours'].count(
                #                         max(routine['days'], key=routine['days'].count)):
                #                     routine['cron'][2] = f"{routine['cron'][2]},{t}"
                #         for t in set(routine['days']):
                #             if routine['cron'][2].find(str(t)) == -1:
                #                 if routine['days'].count(t) >= routine['days'].count(
                #                         max(routine['days'], key=routine['days'].count)):
                #                     routine['cron'][5] = f"{routine['cron'][5]},{t}"
                #         ic('***** 변경 후 *****')
                #         ic(routine)
                # # Not Matching
                # else:
                #     # Comparing location
                #     if location == routine['location']:
                #         grade += 1
                #         # Comparing day
                #         if routine['cron'][5].find(day) > -1:
                #             grade += 1
                #         # Comparing time
                #         if time == routine['cron'][2]:
                #             grade += 2
                #         elif routine['cron'][2] - 3 < time < routine['cron'][2] + 3:
                #             grade += 1







                # Nothing to Matching





    def checking_cron(self, routine, day, grade, time, days, log):
        time = int(time)
        cron_time = int(routine['cron'][2])
        # Comparing day
        if routine['cron'][5].find(day) > -1:
            grade += 1
        # Comparing time
        if time == cron_time:
            grade += 2
        elif cron_time - 1 <= time <= cron_time + 1:
            grade += 1
        elif cron_time == 23:
            if routine['cron'].find(days[log['log_date'].weekday() + 1]) > -1 and time == 0:
                grade += 1
        elif cron_time == 0:
            if routine['cron'].find(days[log['log_date'].weekday() - 1]) > -1 and time == 23:
                grade += 1
        return grade




    def process_old(self):
        today = datetime.now().date()
        today_log = list(UserLog.objects.filter(log_date__year=today.year,
                                          log_date__month=today.month,
                                          log_date__day=today.day).values())
        days = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
        # checking similar routine
        for log in today_log:
            location = log['location']
            # day = log['log_date'].weekday()
            # time = log['log_date'].hour
            full_texts = log['contents']
            contents = []
            cron = [0, 0, log['log_date'].hour, 0, 0, {days[log['log_date'].weekday()]:1}]
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
                    test_cron = [0, 0, test['log_date'].hour, 0, 0, days[test['log_date'].weekday()]]
                    if i == j:
                        print('*'*100)
                        print(f'======================== i : {i} == j : {j} ===============================')
                        grade = grade + 1
                        # 시간 확인
                        if test_cron[2] == cron[2]:
                            # [[case 1]] contents + location + cron == 3
                            grade = grade + 2
                            print('[[case 1]] contents + location + cron')
                            print(f'cron : {cron}')
                            print(f'test_cron : {test_cron}')
                            # checking weekday
                            cron, grade = self.checking_days(cron, test_cron, grade)

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

    def checking_days(self, cron, test_cron, grade):
        print("************* checking_days *************")
        new_cron = cron[5]
        for i in cron[5]:
            print('?!!!!?!?!?!?!?!?')
            print(f' i = {i}, type = {type(i)}')
            if test_cron[5] == i:
                print('요일 같음!!!!')
                grade = grade + 1
                print(f' 변경 전 : {new_cron}')
                new_cron[i] += 1
                print(f' 변경 후 : {new_cron}')
            else:
                print('요일 다름!!!!')
                print(f'test_cron[5] :: {test_cron[5]}, i : {i}')
                print(f' 변경 전 : {new_cron}')
                new_cron[test_cron[5]] = 1
                print(f' 변경 후 : {new_cron}')
        return new_cron, grade


if __name__ == '__main__':
    r = RoutineTest()
    r.process(1)

