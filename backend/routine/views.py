from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from icecream import ic
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser


# Create your views here.
from routine.models import Routine
from routine.models_process import RoutineMaker
from routine.serializers import RoutineSerializer


@api_view(['GET'])
@parser_classes([JSONParser])
def test(request):
    return JsonResponse({'Routine Test': 'SUCCESS'})


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def find_all(request):
    ic("********** find ALL **********")
    routines = Routine.objects.all()
    serializer = RoutineSerializer(routines, many=True)
    ic(serializer.data)
    return JsonResponse(data=serializer.data, safe=False)


@api_view(['GET'])
@parser_classes([JSONParser])
def upload(request):
    Routine.objects.create(log_repeat=0,
                           priority=0,
                           grade=0,
                           contents="열심히 파이썬 공부",
                           location='비트캠프',
                           cron=["0", "0", "10", "0", "0", "fri"],
                           days=["fri", "sun"],
                           hours=["10"],
                           log_id=[],
                           user_id=1
                           )
    return JsonResponse({'Routine Upload': 'SUCCESS'})


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def make_routine(request, user_id):
    ic("********** make_routine **********")
    RoutineMaker().process(user_id)
    return JsonResponse({'Routine Making': 'SUCCESS'})


@api_view(['DELETE'])
@parser_classes([JSONParser])
def remove(request, pk):
    ic("********** remove **********")
    ic(f'pk : {pk}')
    db = Routine.objects.get(pk=pk)
    db.delete()
    return JsonResponse({'Routine DELETE': 'SUCCESS'})


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def today_top10(request, user_id):
    ic("********** today_top10 **********")
    days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    today = days[datetime.now().weekday()]
    ic(f"********** today : {today} **********")
    routines = list(Routine.objects.filter(user_id=user_id).order_by('-priority').values())
    result = []
    [result.append(i) for i in routines if i['cron'][5].find(today) > -1]
    return JsonResponse(data=result[0:10], safe=False)