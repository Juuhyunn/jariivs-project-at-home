import os
import random
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")
import django
django.setup()
from common.models import ValueObject, Reader, Printer
from diary.models import Diary
from drawing.models import Drawing
from userlog.models import UserLog
from writing.models import Writing


class DbUploader:
    def __init__(self):
        self.vo = ValueObject()
        self.write_path = 'machine/m_dev_happy'
        self.draw_path = 'img'

    def insert_data(self):
        self.insert_userlog(3, '1')

    def insert_userlog(self, achieve_log, user_id):
        topic_w = ['냠냠', '남자친구', '배불러']
        topic_d = ["face", "computer", "bear"]
        log = UserLog.objects.get(pk=achieve_log)
        self.vo.context = self.write_path
        w = Writing(self.vo)
        writing = ''.join(w.process(i) for i in topic_w)
        self.vo.context = self.draw_path
        drawing = Drawing(self.vo).process(topic_d)
        writing = f'오늘은 {log.location} 갔다!' + writing if random.randint(0, 1) == 0 else writing
        print(writing)
        # Diary.objects.create(weather=log.weather,
        #                      location=log.location,
        #                      drawing=drawing,
        #                      contents=writing,
        #                      memo='사용자가 작성하는 메모',
        #                      log_id=achieve_log,      # 이거 어떡하지
        #                      user_id=user_id)
        print('Diary DATA UPLOADED SUCCESSFULY!')

if __name__ == '__main__':
    d = DbUploader()
    d.insert_data()