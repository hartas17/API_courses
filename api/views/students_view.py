# -*- coding: utf-8 -*-
import logging

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Students, ScoreStudent, Courses, Lessons
from api.serializers import StudentsSerializer, GetStudentsSerializer
from api.auth_middleware import login_required, is_proffesor, login_and_is_owner
from django.core.validators import validate_email
from django.http import JsonResponse

logger = logging.getLogger(__name__)


def check_errors_password(password):
    """Revisa las condiciones de una buena contraseña y devuelve una
    lista de errores."""
    errors = []
    if len(password) < 6:
        errors.append("La contraseña debe tener al menos 6 caracteres")
    return errors


def check_errors_email(email, errors):
    """Checks that a given email is a valid email

    email - email to validate
    errors (out)
    """
    result = True
    try:
        validate_email(email)
    except:
        errors.append("El email que se uso no es valido")
        result = False
    return result


def check_errors_create_account(username, firstname, email, password):
    errors = []
    username_query = Students.objects.filter(username=username)
    email_query = Students.objects.filter(email=email)

    if not username and (username_query.count() >= 1):
        errors.append("Ese usuario ya está vinculado a otra cuenta")

    if not email:
        errors.append("Se necesita proporcionar un correo electrónico")

    if email and (email_query.count() >= 1):
        errors.append("Ese correo ya está vinculado a otra cuenta")

    if (not errors) and email:
        check_errors_email(email, errors)

    errors.extend(check_errors_password(password))

    return errors


def create_student_score(new_user):
    item_course = None
    item_lesson = None
    try:
        item_course = Courses.objects.get(previous_one=None)
        item_lesson = Lessons.objects.get(previous_one=None, course=item_course.pk)
    except Exception as e:
        print e
    ScoreStudent(student=new_user, course=item_course, lesson=item_lesson, score=0).save()
    pass


@api_view(['POST'])
def register_students(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        firstname = request.POST.get('firstname', '')
        lastname = request.POST.get('lastname', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        errors = check_errors_create_account(username, firstname, email, password)

        status = 400
        response = {'success': (len(errors) == 0),
                    'errors': errors}

        if response['success']:
            # successs
            status = 200
            new_user = Students(username=username, firstname=firstname, lastname=lastname, email=email)
            new_user.set_password(password)
            response['data'] = new_user.details_dict()
        else:
            logger.error(errors)

            # We return the response
            # We need to use unsafe mode to return a list of errors
        create_student_score(new_user)
        return JsonResponse(response, safe=False, status=status, content_type='application/json')


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        errors = check_errors_login(username, password)
        user = Students.objects.filter(username=username).first()
        status = 200
        # check that that the account exists
        if (not errors) and (user is None):
            # username does not exist
            errors.append("Usuario no encontrado")

        # check password matches
        if not errors:

            if not user.check_password(password):
                errors.append("Contraseña incorrecta")

        # check that the email has been confirmed
        #    if not errors and user.email == "":
        #        errors.append("Se necesita confirmar el email" +
        #                      " de la cuenta para iniciar sesión")
        if not errors:
            # Success
            response = {'success': True,
                        'data': user.details_dict()}
        else:
            # Error
            status = 400
            response = {'success': False,
                        'errors': errors}

        return JsonResponse(response, safe=False, status=status)
    return None


def check_errors_login(username, password):
    errors = []

    if not username:
        errors.append("No se especifico el nombre de usuario")

    if not password:
        errors.append(u"No se especifico la contraseña")

    return errors


@is_proffesor
@login_and_is_owner
@api_view(['GET'])
def students_list(request):
    if request.method == 'GET':
        items = Students.objects.all()
        serializer = GetStudentsSerializer(items, many=True)
        return Response({'success': True, 'data': serializer.data})


@csrf_exempt
@login_required
@api_view(['GET', 'PUT', 'DELETE'])
def students_detail(request, pk):
    try:
        item = Students.objects.get(pk=pk)
    except Students.DoesNotExist:
        return Response({'success': False, 'errors': ['No existe ese usuario']}, status=400)

    if request.method == 'GET':
        serializer = GetStudentsSerializer(item)
        return Response({'success': True, 'data': serializer.data})
    else:
        return manage_student_info(request, item)


@is_proffesor
def manage_student_info(request, item):
    if request.method == 'PUT':
        serializer = StudentsSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'data': serializer.data}, status=201)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)