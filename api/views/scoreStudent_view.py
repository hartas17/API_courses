from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.auth_middleware import login_required, is_proffesor
from api.models import ScoreStudent
from api.serializers import ScoreStudentSerializer, PutScoreStudentSerializer


@login_required
@is_proffesor
@api_view(['GET'])
def scorestudent_list(request):
    if request.method == 'GET':
        items = ScoreStudent.objects.all()
        serializer = ScoreStudentSerializer(items, many=True)
        return Response(dict(success=True, data=serializer.data))

    elif request.method == 'POST':
        serializer = ScoreStudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(dict(success=True, data=serializer.data), status=201)
        return Response(dict(success=False, errors=[serializer.errors]), status=400)


@login_required
@is_proffesor
@api_view(['GET', 'PUT'])
def scorestudent_detail(request, pk):
    try:
        item = ScoreStudent.objects.get(student=pk)
    except ScoreStudent.DoesNotExist:
        return Response(status=400)

    if request.method == 'GET':
        serializer = ScoreStudentSerializer(item)
        return Response(dict(success=True, data=serializer.data))

    elif request.method == 'PUT':
        try:
            item_score = ScoreStudent.objects.get(student=pk)
            serializer = PutScoreStudentSerializer(item_score, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(dict(success=True, data=serializer.data))
            return Response(dict(success=False, erros=[serializer.errors]), status=400)
        except Exception as e:
            return Response(dict(success=False, erros=["No se encuentra ese usuario"]), status=400)
