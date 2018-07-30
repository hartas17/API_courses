# -*- coding: utf-8 -*-

from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.auth_middleware import is_proffesor, login_required
from api.models import Courses, LogScoreStudent, ScoreStudent
from api.serializers import CoursesSerializer, AddLessonsSerializer


def order_course(id):
    """ Metodo para agregar cursos, considerando la estuctura 'Lista' con elementos subsecuentes"""
    pass


@login_required
@api_view(['GET', 'POST'])
def courses_list(request):
    if request.method == 'GET':
        items = Courses.objects.all()
        serializer = CoursesSerializer(items, many=True)
        return Response({'success': True, 'data': serializer.data})

    elif request.method == 'POST':
        return add_courses(request)


@is_proffesor
def add_courses(request):
    serializer = AddLessonsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        return Response({'success': True, 'data': serializer.data}, status=201)
    return Response({'success': False, 'errors': serializer.errors}, status=400)


@login_required
@api_view(['GET', 'PUT', 'DELETE'])
def courses_detail(request, pk):
    try:
        item = Courses.objects.get(pk=pk)
    except Courses.DoesNotExist:
        return Response(dict(success=False, errors=['No existe ese Curso']), status=400)

    if request.method == 'GET':
        serializer = CoursesSerializer(item)
        return Response(dict(success=True, data=serializer.data))

    else:
        return edit_course(request, item)


@is_proffesor
def edit_course(request, item):
    if request.method == 'PUT':
        serializer = CoursesSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(dict(success=True, data=serializer.data))
        return Response(dict(success=False, errors=[serializer.errors]), status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)


@login_required
@is_proffesor
@api_view(['GET'])
def courses_user_can_access(request, course):
    students_pass_course = set(LogScoreStudent.objects.filter(course=course).values_list('student', flat=True))
    student_actualy_course = set(ScoreStudent.objects.filter(course=course).values_list('student', flat=True))
    resp = (students_pass_course | student_actualy_course)
    return Response(dict(success=True, data=resp), status=200)
