from datetime import datetime

from django.db import models

# Create your models here.


class Diary(models.Model):
    diary_date = models.DateTimeField(default=datetime.now())
    weather = models.TextField()
    location = models.TextField()
    drawing = models.TextField()
    contents = models.TextField()
    memo = models.TextField()
    log_id = models.ForeignKey("userlog.UserLog", on_delete=models.CASCADE, db_column='log_id')     # fk
    user_id = models.IntegerField()         # fk

    class Meta:
        db_table = 'diary'

    def __str__(self):
        return f'[{self.pk}] ' \
               f'일기 생성 날짜 : {self.diary_date},' \
               f'날씨 : {self.weather},' \
               f'위치 : {self.location},' \
               f'그림 : {self.drawing},' \
               f'내용 : {self.contents},' \
               f'메모 : {self.memo},' \
               f'수행한 히스토리 : {self.log_id},' \
               f'사용자 : {self.user_id}'