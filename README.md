Prueba Backend 
======
Backend developer position challenge

We require to develop an API for e-learning courses to integrate in our system. The purpose
of this tool is for us, as professors to manage courses configuration and performance
reviews and, for our students, to take courses when using our frontend.
Our PM is a very busy person, so we don’t have detailed tasks but only the business rules to
work with. Here they are:
1. We have courses that contain lessons and lessons that contain questions
2. The courses are correlative with previous ones
3. The lessons are correlative with previous ones
4. The questions for each lesson have no correlation
5. All questions for a lesson are mandatory
6. Each question has a score
7. Each lesson has an approval score that has to be met by the sum of correctly
answered questions to approve it
8. A course is approved when all lessons are passed.
9. There’s no restriction on accessing approved courses
10. Only professors can create and manage courses, lessons and questions
11. Any student can take a course
12. Initially, we’ll need to support these types of questions:
	
	* Boolean
	* Multiple choice where only one answer is correct
	* Multiple choice where more than one answer is correct
	* Multiple choice where more than one answer is correct and all of them must
	be answered correctly

13. Frontend guys specifically asked for these endpoints for the students to use:
	* Get a list of all courses, telling which ones the student can access
	* Get lessons for a course, telling which ones the student can access
	* Get lesson details for answering its questions
	* Take a lesson (to avoid several requests, they asked to send all answers in
	one go)
	* Basic CRUD for courses, lessons and questions

Codebase rules:
1. The API must be developed using Python
2. There must be a readme file documenting installation and usage.
3. You can use any frameworks and libraries you want, but they must be included in the
readme file documenting its purpose and a brief explanation with the reasoning for
your choice.


## Requerimientos
* Python 2.7
* Django 1.11
* Django Rest Framework

## Modulos usados
* [drf-generators](https://github.com/Brobin/drf-generators) 
    * Automatización de la generación del API
* JWT para autentificación
## Instalación


## Correr proyecto

Descargar repositorio:
```bash
https://github.com/hartas17/API_courses.git
```

### DB
Crear DB en MySQL llamada Neximo y posterior

```bash
python manage.py makemigrations
python manage.py migrate
```

O cambia la siguiente linea de código en settings:

````python
DATABASES = {   
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'neximo',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
````
### Montar servidor
Correr django:
```bash
python manage.py runserver
```

El proyecto se correrá en la dirección:
```bash
localhost:8000
```


## Reglas:
El sistema al registrar un usuario se le asigna un TOKEN:
* Existen 2 token, estudiante y profesor, cada uno con sus permisos correspondientes

Para el sistema CRUD, existen endpoint que requieren permiso de Profesor y algunos son para ambos

## Proceso para subir preguntas:
Primero se sube la pregunta al endpoint
```bash
/api/questions/ 
```
Los tipos(valor Type) de preguntas son:

BO = Boolean

MC1C = Multiple choice one correct

MCWC = Multiple choice more than one is correct

MCAC = Multiple choice more than one answer is correct all of them mustbe answered correctly

#### Agregar respuesta

Posterior, se procede a agregar las respuestas a dicha pregunta con el siguiente enpoint.

```
/api/answers/
```
Los parámetros son:

````
question= id de la pregunta
values= array con las respuestas posibles, si el tipo de pregunta es Boolean entonces este campo puede ir vacio
correct= array con los elementos correctos del array values, si el tipo de pregunta es Boolean entonces
solo pueden haber 2 valores [0] para cuando la respuesta es False y [1] para cuando la respuesta es True
````

ejemplo tipo pregunta BO y como respuesta Verdadero:
````
question= 1
values= []
correct=[1]
````
ejemplo tipo pregunta MC1C, respuesta correcta es values[3]=respuesta3
````
question= 1
values= ["respuesta1","respuesta2","respuesta3"]
correct=[3]
````
ejemplo tipo pregunta MCWC, respuesta correcta es values[3]=respuesta3 o values[1]=respuesta1
````
question= 1
values= ["respuesta1","respuesta2","respuesta3"]
correct=[3,1]
````
ejemplo tipo pregunta MCAC, respuesta correcta es values[3]=respuesta3 y values[1]=respuesta1
````
question= 1
values= ["respuesta1","respuesta2","respuesta3"]
correct=[3,1]
````

El enpoint elimina las respuestas actuales y agrega las que se estén enviando

No se tiene un límite de respuestas posibles tampoco de respuestas correctas


### Responder todas las preguntas de una lección:
````bash
{{url}}/api/all_answer_in_one_go/
````

Los parámetros son:
````
questions_answers = dict con la forma {id_pregunta:[id_respuestas_seleccionadas]}
studen = id_estudiante
lesson = id_leccion
````

ejemplo contestada la lección 3 enviando id_respuestas[2,3,4] para id_preguna=1 y id_respuesta{3] para id_pregunta=2:

````
questions_answers = [{1:[2,3,4]},{2:[3]}]
student = 12
lesson = 3
````


## Proceso para responder preguntas por el estudiante:

El API está diseñado de tal manera que solo se usen 2 enpoint para esta acción

Para obtener la pregunta:
````
{{url}}/api/question_for_user/<id_estudiante>
````
Este Endpoint hace las siguientes validaciones:
* Si existe el usuario
* Si quedan preguntas por contestar
* Si ya terminaste una lección
* Si ya se terminó un curso
* Si quedan cursos por tomar
* Si tienes suficientes puntos para pasar de lección
* Asigna el curso siguiente en caso de terminar uno
* Asigna la lección siguiente en caso de terminar una

Para responder la pregunta:
````
{{url}}/api/answer_question/
````

parámetros:
````
student = id_estudiante
question =  id_pregunta
response = [id_respuestas]
````
Solo se debe envíar una lista con los id de las respuestas que el usuario haya seleccionado


## API
Total: 37 Enpoints

4 enpoints especificos:
````
{{url}}/api/all_answer_in_one_go/
{{url}}/api/lesson_user_can_access/<id_lesson>
{{url}}/api/courses_user_can_access/<id_course>
{{url}}/api/lesson_detail_answering_question/<id_lesson>
````

y los restantes 34 para el CRUD y para acciones propias de las reglas propuestas


## Acceso a la API:

# [API documentation](https://documenter.getpostman.com/view/2930473/RWMLL6oi)

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/44926694f78c9cd93737)
# COLLECTION
[descargar la collection](https://www.getpostman.com/collections/44926694f78c9cd93737) funciona en [POSTMAN](https://www.getpostman.com/postman)

Una vez descargada la collection se agrega el enviroment:

_La collection está hecha para automatizar el llenado del enviroment_
````json
{
  "id": "47e38430-9583-431a-a2ba-a2384fd2f8b2",
  "name": "Neximo",
  "values": [
    {
      "description": {
        "content": "",
        "type": "text/plain"
      },
      "value": "http://localhost:8000",
      "key": "url",
      "enabled": true
    },
    {
      "value": 6,
      "key": "professor_id",
      "enabled": true
    },
    {
      "value": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im1hbnVlbCIsInVzZXJfaWQiOjYsImVtYWlsIjoibWFudWVsQGNhbi5jb20iLCJleHAiOjE1NjQzMjk4OTJ9.F4zymoVWqxTuMuGAMXNuizN0RntD3_0rNz7vsrx9Ke0",
      "key": "token_professor",
      "enabled": true
    },
    {
      "value": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFsdW1ub3MiLCJ1c2VyX2lkIjoxMCwiZW1haWwiOiJhbHVtbm9zQG5leGltby5jb20iLCJleHAiOjE1NjQ0NTU3NDl9.XObESP4tOvsw4JoOA_LCYiFsQATrExiATcCJZyXh5lo",
      "key": "token_student",
      "enabled": true
    },
    {
      "value": 10,
      "key": "student_id",
      "enabled": true
    },
    {
      "value": 11,
      "key": "id_question",
      "enabled": true
    }
  ],
  "_postman_variable_scope": "environment",
  "_postman_exported_at": "2018-07-30T03:16:15.550Z",
  "_postman_exported_using": "Postman/6.2.2"
}
````

# TO DO list

* Poder editar los datos de los profesores(Agregar is_owner para profesores)
* No se puede contestar pregunta que ya ha sido contestada
* Agregar estudiantes sin existencia de cursos, lecciones ni preguntas
* Poder agregar cursos en posición intermedia
* Poder agregar lecciones en posición intermedia
* Validar que al agregar respuestas a una pregunta, dependiendo del tipo de pregunta, valide si cumple
condición(condición referente a su tipo: BO,MC1C,etc)
* Limpiar historial cuando se envío una cadena de preguntas y presentó algún error
* Documentar las posibles respuestas(Actualmente dice especificamente el error)