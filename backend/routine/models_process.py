from datetime import datetime

from icecream import ic
import os

from konlpy.tag import Okt


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")
import django
django.setup()
from userlog.models import UserLog
from routine.models import Routine
from routine.serializers import RoutineSerializer


class RoutineMaker:
    def __init__(self):
        pass

    def process(self, user_id):
        # Getting ALL of today logs
        today = datetime.now().date()
        all_today = list(UserLog.objects.filter(log_date__year=today.year,
                                                log_date__month=today.month,
                                                log_date__day=today.day,
                                                user_id=user_id).values())
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
        all_routine = list(Routine.objects.filter(user_id=user_id).values())
        days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        # Checking log
        for log in all_today:
            flag = 0
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
                if len(new_contents) == len(routine_contents) or len(new_contents) >= len(routine_contents) / 2:
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
                        routine['grade'] += grade
                        routine['days'].append(day)
                        routine['hours'].append(time)
                        routine['log_id'].append(log_id)
                        routine['log_repeat'] = len(routine['log_id'])
                        print(f"routine['grade'] :: {routine['grade']}")
                        print(f"routine['log_repeat'] :: {routine['log_repeat']}")
                        routine['priority'] = routine['grade'] * routine['log_repeat']
                        routine['cron'][2] = max(routine['hours'], key=routine['hours'].count)
                        cron_day = []
                        for t in set(routine['days']):
                            if routine['days'].count(t) >= routine['days'].count(max(routine['days'], key=routine['days'].count)):
                                cron_day.append(t)
                        routine['cron'][5] = '.'.join(cron_day)
                        routine['log_id'] = list(set(routine['log_id']))
                        ic('***** 변경 후 *****')
                        ic(routine)
                        db = Routine.objects.get(id=routine['id'])
                        db.log_repeat = routine['log_repeat']
                        db.save()
                        db.priority = routine['priority']
                        db.save()
                        db.grade = routine['grade']
                        db.save()
                        db.cron = routine['cron']
                        db.save()
                        db.days = routine['days']
                        db.save()
                        db.hours = routine['hours']
                        db.save()
                        db.log_id = routine['log_id']
                        db.save()
                        flag = 1
            # new routine
            if flag == 0:
                Routine.objects.create(log_repeat=1,
                                       priority=0,
                                       grade=0,
                                       contents=' '.join(contents),
                                       location=location,
                                       cron=["0", "0", time, "0", "0", day],
                                       days=[day],
                                       hours=[time],
                                       log_id=[log_id],
                                       user_id=user_id
                                       )