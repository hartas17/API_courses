from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.auth_middleware import login_required, is_proffesor
from api.models import Answers
from api.serializers import AnswersSerializer


@login_required
@api_view(['GET', 'POST'])
def answers_list(request):
    if request.method == 'GET':
        items = Answers.objects.all()
        serializer = AnswersSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        add_answer(request)


@is_proffesor
def add_answer(request):
    serializer = AnswersSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@login_required
@api_view(['GET', 'PUT', 'DELETE'])
def answers_detail(request, pk):
    try:
        item = Answers.objects.get(pk=pk)
    except Answers.DoesNotExist:
        return Response(status=400)

    if request.method == 'GET':
        serializer = AnswersSerializer(item)
        return Response(serializer.data)
    else:
        update_anser(request, item)


@is_proffesor
def update_anser(request, item):
    if request.method == 'PUT':
        serializer = AnswersSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)
