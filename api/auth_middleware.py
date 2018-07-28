# -*- coding: utf-8 -*-

from django.http import JsonResponse
from api.models import Students, Professors


class AuthMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.neximo_student = get_student_from_request(request)
        request.neximo_professors = get_professors_request(request)
        return self.get_response(request)


def get_student_from_request(request):
    """Returns the user associated with a request or None.

    Obtains the user from the token that comes in the HTTP header
    "AUTHORIZATION"
    """
    token = request.META.get("HTTP_AUTHORIZATION", "")
    return Students.get_user_from_token(token)


def get_professors_request(request):
    """Returns the user associated with a request or None.

    Obtains the user from the token that comes in the HTTP header
    "AUTHORIZATION"
    """
    token = request.META.get("HTTP_AUTHORIZATION", "")
    return Professors.get_user_from_token(token)


def login_required(func):
    """Decorator that makes sure that there is a user logged in to the
    system. Otherwise returns a json message with a 401 status_code"""

    def wrapped_func(request, *args, **kwargs):
        if request.neximo_student is None and request.neximo_professors is None:
            response = {'success': False,
                        'errors': ["Se necesita iniciar sesion " +
                                   "para usar este metodo"],
                        'status': 401}
            return JsonResponse(response, status=401, safe=False)
        else:
            return func(request, *args, **kwargs)

    # return the actual function
    return wrapped_func


def login_and_is_owner(func):
    """Decorator that makes sure that there is a user logged in to the
    system. Otherwise returns a json message with a 401 status_code"""

    def wrapped_func(request, *args, **kwargs):
        if request.neximo_student is not None:
            try:
                if int(kwargs["pk"]) == int(request.neximo_student.pk):
                    pass
                else:
                    response = {'success': False,
                                'errors': ["No eres propietario de estos datos"],
                                'status': 401}
                    return JsonResponse(response, status=401, safe=False)
            except Exception as e:
                print e
        if request.neximo_student is None and request.neximo_professors is None:
            response = {'success': False,
                        'errors': ["Se necesita iniciar sesion " +
                                   "para usar este metodo"],
                        'status': 401}
            return JsonResponse(response, status=401, safe=False)
        else:
            return func(request, *args, **kwargs)

    # return the actual function
    return wrapped_func


#Check if user is owner
def isOwner(func):
    def wrapped_func(request, *args, **kwargs):
        if request.neximo_student is None or request.neximo_professors is None:
            response = {'success': False,
                        'errors': ["Se necesita iniciar sesion " +
                                   "para usar este metodo"],
                        'status': 401}
            return JsonResponse(response, status=401, safe=False)
        else:
            return func(request, *args, **kwargs)

    # return the actual function
    return wrapped_func


def is_proffesor(func):
    def wrapped_func(request, *args, **kwargs):
        if request.neximo_professors is not None:
            return func(request, *args, **kwargs)
        else:
            response = {'success': False,
                        'errors': ["Solo los profesores pueden " +
                                   "acceder a este metodo"],
                        'status': 401}
            return JsonResponse(response, status=401, safe=False)

    return wrapped_func
