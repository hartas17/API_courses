from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import ScoreStudent
from api.serializers import ScoreStudentSerializer


@api_view(['GET', 'POST'])
def scorestudent_list(request):
    if request.method == 'GET':
        items = ScoreStudent.objects.all()
        serializer = ScoreStudentSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ScoreStudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def scorestudent_detail(request, pk):
    try:
        item = ScoreStudent.objects.get(pk=pk)
    except ScoreStudent.DoesNotExist:
        return Response(status=400)

    if request.method == 'GET':
        serializer = ScoreStudentSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ScoreStudentSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)