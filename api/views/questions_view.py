from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Questions
from api.serializers import QuestionsSerializer


@api_view(['GET', 'POST'])
def questions_list(request):
    if request.method == 'GET':
        items = Questions.objects.all()
        serializer = QuestionsSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = QuestionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def questions_detail(request, pk):
    try:
        item = Questions.objects.get(pk=pk)
    except Questions.DoesNotExist:
        return Response(status=400)

    if request.method == 'GET':
        serializer = QuestionsSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = QuestionsSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)
