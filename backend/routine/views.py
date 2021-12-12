from django.http import JsonResponse
from django.shortcuts import render
from icecream import ic
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser


# Create your views here.
from routine.models import Routine
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


@api_view(['PUT'])
@parser_classes([JSONParser])
def modify(request):
    ic("********** modify **********")
    edit = request.data
    ic(edit)
    routine = Routine.objects.get(pk=edit['id'])
    db = Routine.objects.all().filter(id=edit['id']).values()[0]
    print(f' 변경 전 : {db}')
    db['log_repeat'] = edit['log_repeat']
    db['create_date'] = edit['create_date']
    db['priority'] = edit['priority']
    db['grade'] = edit['grade']
    db['contents'] = edit['contents']
    db['location'] = edit['location']
    db['cron'] = edit['cron']
    db['days'] = edit['days']
    db['hours'] = edit['hours']
    db['log_id'] = edit['log_id']
    print(f' 변경 후 : {db}')
    serializer = RoutineSerializer(data=db)
    # print(f'db type : {type(db)}  // serializer type : {type(serializer)}')
    if serializer.is_valid():
        serializer.update(routine, db)
        return JsonResponse(data=serializer.data, safe=False)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@parser_classes([JSONParser])
def remove(request, pk):
    ic("********** remove **********")
    ic(f'pk : {pk}')
    db = Routine.objects.get(pk=pk)
    db.delete()
    return JsonResponse({'Routine DELETE': 'SUCCESS'})