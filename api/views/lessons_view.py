from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Lessons
from api.serializers import LessonsSerializer


@api_view(['GET', 'POST'])
def lessons_list(request):
    if request.method == 'GET':
        items = Lessons.objects.all()
        serializer = LessonsSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = LessonsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def lessons_detail(request, pk):
    try:
        item = Lessons.objects.get(pk=pk)
    except Lessons.DoesNotExist:
        return Response(status=400)

    if request.method == 'GET':
        serializer = LessonsSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = LessonsSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)