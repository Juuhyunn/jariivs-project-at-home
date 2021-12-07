from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from icecream import ic
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

from diary.models import Diary
from diary.models_data import DbUploader
from diary.serializers import DiarySerializer


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def process(request):
    return JsonResponse({'process': 'SUCCESS'})


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def upload(request):
    ic("********** upload START **********")
    DbUploader().insert_data()
    return JsonResponse({'process': 'SUCCESS'})


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def find(request, year, month, day):
    ic("********** find START **********")
    ic(f'date : {year}-{month}-{day}')
    diary = Diary.objects.filter(diary_date__year= year, diary_date__month=month, diary_date__day=day)
    serializer = DiarySerializer(diary, many=True)
    ic(serializer.data)
    return JsonResponse(data=serializer.data, safe=False)


@api_view(['PUT'])
@parser_classes([JSONParser])
def modify(request):
    ic("********** modify START **********")
    edit = request.data
    # ic(edit)
    diary = Diary.objects.get(pk=edit['id'])
    db = Diary.objects.filter(pk=edit['id']).values()[0]
    # ic(diary)
    db['memo'] = edit['memo']
    db['diary_date'] = edit['diary_date']
    db['log_id'] = edit['log_id']
    serializer = DiarySerializer(data=db)
    if serializer.is_valid():
        serializer.update(diary, db)
        return JsonResponse(data=serializer.data, safe=False)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
