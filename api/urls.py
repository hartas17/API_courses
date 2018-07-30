from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import students_view, professors_view, courses_view, lessons_view, questions_view, answers_view, \
    scoreStudent_view

urlpatterns = [

    #Register
    url(r'^register_professors/$', professors_view.register_professors),
    url(r'^register_students/$', students_view.register_students),

    #Login
    url(r'^login_professor/$', professors_view.login),
    url(r'^login_student/$', students_view.login),

    #Studens CRUD
    url(r'^students/(?P<pk>[0-9]+)$', students_view.students_detail),
    url(r'^students/$', students_view.students_list),

    #Profesores CRUD
    url(r'^professors/(?P<pk>[0-9]+)$', professors_view.professors_detail),
    url(r'^professors/$', professors_view.professors_list),

    #Cursos
    url(r'^courses/(?P<pk>[0-9]+)$', courses_view.courses_detail),
    url(r'^courses/$', courses_view.courses_list),
    url(r'^courses_user_can_access/(?P<course>[0-9]+)$', courses_view.courses_user_can_access),

    #Lecciones
    url(r'^lessons/(?P<pk>[0-9]+)$', lessons_view.lessons_detail),
    url(r'^lessons/$', lessons_view.lessons_list),
    url(r'^lessons_by_course/(?P<course>[0-9]+)$', lessons_view.lessons_by_course),
    url(r'^lesson_user_can_access/(?P<lesson>[0-9]+)$', lessons_view.lesson_user_can_access),
    url(r'^all_answer_in_one_go/$', lessons_view.all_answer_in_one_go),
    url(r'^lesson_detail_answering_question/(?P<lesson>[0-9]+)$',lessons_view.lesson_detail_answering_question),

    #Preguntas
    url(r'^questions/(?P<pk>[0-9]+)$', questions_view.questions_detail),
    url(r'^questions/$', questions_view.questions_list),
    url(r'^questions_by_lesson/(?P<lesson>[0-9]+)$', questions_view.questions_by_lesson),
    url(r'^answer_question/$', questions_view.answer_question),
    url(r'^question_for_user/(?P<student>[0-9]+)$', questions_view.question_for_user),

    #Respuestas
    url(r'^answers_question/(?P<question>[0-9]+)$', answers_view.answers_detail),
    url(r'^answers/$', answers_view.answers_list),

    #Estadisticas actuales de estudiantes
    url(r'^scorestudent/(?P<pk>[0-9]+)$', scoreStudent_view.scorestudent_detail),
    url(r'^scorestudent/$', scoreStudent_view.scorestudent_list),


]

urlpatterns = format_suffix_patterns(urlpatterns)
