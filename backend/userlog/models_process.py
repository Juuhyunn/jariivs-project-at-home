import csv
import random

from common.models import ValueObject, Reader, Printer
from location.models import LocationData
from location.models_process import Location
from location.serializers import LocationSerializer
from weather.models import Weather


class LogData(object):
    def __init__(self):
        vo = ValueObject()
        vo.context = 'location/img/'
        vo.fname = 'location_data.csv'
        reader = Reader()
        # self.printer = Printer()
        self.csvfile = reader.new_file(vo)
        self.weather = Weather()

    def process(self):
        return self.create_log()

    def create_log(self):
        log = self.random_log()
        weather = self.weather.process()
        latlng = Location().getLatLng(log['address'])
        return {'location': log['location'],
                'address': log['address'],
                'x': latlng[0] if log['address'] != '' else '',
                'y': latlng[1] if log['address'] != '' else '',
                'weather': weather,
                'log_type': log['log_type'],
                'contents': log['contents'],
                # 'item': log['item']
                }

    def random_log(self):
        ls = self.dummy_from_db()
        num = random.randint(0 ,len(ls)-1)
        if random.randint(0, 5) == 0:
            return self.create_visit(ls, num)
        elif random.randint(0, 5) == 1:
            return self.create_payment(ls, num)
        else:
            return self.create_study()
        # return self.create_visit(ls, num) if random.randint(0, 1) == 0 else self.create_payment(ls, num)

    def create_visit(self, ls, num):
        return {'location': ls[num]['location'],
                'address': ls[num]['address'],
                'log_type': 'visit',
                'contents': f"{ls[num]['category']}-{ls[num]['location']}을 방문함.",
                # 'item': f"{ls[num]['location']} 방문"
                }

    def create_payment(self, ls, num):
        return {'location': ls[num]['location'],
                'address': ls[num]['address'],
                'log_type': 'payment',
                'contents': f"[{ls[num]['category']}] {ls[num]['location']}에서 {random.randint(0 ,1000 ) *100}원을 결제함.",
                # 'item': f"{random.randint(0 ,1000 ) *100}"
                }

    def create_study(self):
        test1 = ['진행', '운동', '노력', '코딩', '공부', '커밋', '작업', '개발']
        test2 = ['술술', '직접', '스스로', '열심히']
        return {'location': '비트캠프',
                'address': '',
                'log_type': 'study',
                'contents': f"{test2[random.randint(0 ,len(test2) -1)]} {test1[random.randint(0 ,len(test1) -1)]}했다."}

    def dummy_from_csv(self):
        ls = []
        with open(self.csvfile, newline='', encoding='utf8') as f:
            [ls.append(i) for i in csv.DictReader(f)]
        return ls

    def dummy_from_db(self):
        ls = []
        data = LocationData.objects.all()
        serializer = LocationSerializer(data, many=True)
        [ls.append(dict(i)) for i in serializer.data]
        return ls