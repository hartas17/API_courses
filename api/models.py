# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime as times
from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from rest_framework_jwt import utils
from rest_framework_jwt.settings import api_settings


# Create your models here.

class Users(models.Model):
    username = models.CharField(unique=True, max_length=255)
    firstname = models.CharField(max_length=124)
    lastname = models.CharField(max_length=45, blank=True, null=True)
    email = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=128)
    token = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(db_column='created', auto_now_add=True)
    updated = models.DateTimeField(db_column='updated', auto_now=True)

    class Meta:
        managed = True
        db_table = 'Users'

    def set_password(self, password):
        self.password = make_password(password)
        self.save()

    def check_password(self, password):
        """Returns true if this is the user's password, false
        otherwise """
        return check_password(password, self.password)

    def create_token(self):
        """Creates a signed token that identifies the current user and
        expires in an hour
        """
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        api_settings.JWT_EXPIRATION_DELTA = times.timedelta(days=365)
        token = ""
        try:
            user = self
            payload = jwt_payload_handler(user)
            print payload
            token = jwt_encode_handler(payload)

        except Exception as e:
            print e
        return token


class Students(Users):
    last_course = models.ForeignKey("Courses", on_delete=models.SET_NULL, blank=True, null=True )


    class Meta:
        managed = True
        db_table = 'students'

    def if_professor(self):
        return False

    def details_dict(self):
        self.token = self.create_token()
        self.save()
        return {'id': self.pk,
                'username': self.username,
                'firstname': self.firstname,
                'email': self.email,
                'token': self.token,
                'last_course_id':self.last_course,
                }

    @classmethod
    def get_user_from_token(self, Token):
        userid = -1
        # get user id
        try:
            token = utils.jwt_decode_handler(Token)
            item = Students.objects.get(pk=token['user_id'])
            if item.email == token['email']:
                if item.token == Token:
                    userid = token['user_id']
                else:
                    userid = -1
            else:
                userid = -1
        except:
            pass

        # get user
        # if userid != -1:
        user = Students.objects.filter(id=userid).first()

        return user


class Professors(Users):

    class Meta:
        managed = True
        db_table = 'professors'

    def if_professor(self):
        return True

    def details_dict(self):
        self.token = self.create_token()
        self.save()
        return {'id': self.pk,
                'username': self.username,
                'firstname': self.firstname,
                'email': self.email,
                'token': self.token}

    @classmethod
    def get_user_from_token(self, Token):
        userid = -1
        # get user id
        try:
            token = utils.jwt_decode_handler(Token)
            item = Professors.objects.get(pk=token['user_id'])
            if item.email == token['email']:
                if item.token == Token:
                    userid = token['user_id']
                else:
                    userid = -1
            else:
                userid = -1
        except:
            pass

        # get user
        # if userid != -1:
        user = Professors.objects.filter(id=userid).first()

        return user


class Courses(models.Model):
    title = models.CharField(max_length=128)
    previous_one = models.ForeignKey("Courses", related_name="previousOne", blank=True, null=True)
    next_one = models.ForeignKey("Courses", related_name="nextOne", blank=True, null=True)
    created_by = models.ForeignKey(Professors, blank=True, null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(db_column='created', auto_now_add=True)
    updated = models.DateTimeField(db_column='updated', auto_now=True)

    class Meta:
        managed = True
        db_table = 'courses'

    def save(self, *args, **kwargs):
        try:
            previous_course = Courses.objects.get(next_one=None)
            self.previous_one = previous_course
            super(Courses, self).save(*args, **kwargs)
            previous_course.next_one = self
            previous_course.save()
        except:
            super(Courses, self).save(*args, **kwargs)


class Lessons(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, blank=True, null=True)
    previous_one = models.ForeignKey("self", related_name="previousOne", blank=True, null=True)
    next_one = models.ForeignKey("self", related_name="nextOne", blank=True, null=True)
    approval_score = models.IntegerField()
    created_by = models.ForeignKey(Professors, blank=True, null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(db_column='created', auto_now_add=True)
    updated = models.DateTimeField(db_column='updated', auto_now=True)

    class Meta:
        managed = True
        db_table = 'lessons'

    def save(self, *args, **kwargs):
        try:
            previous_lesson = Lessons.objects.get(next_one=None)
            self.previous_one = previous_lesson
            super(Lessons, self).save(*args, **kwargs)
            previous_lesson.next_one = self
            previous_lesson.save()
        except:
            super(Lessons, self).save(*args, **kwargs)


class Questions(models.Model):
    A = "BO"
    B = "MC1C"
    C = "MCWC"
    D = "MCAC"
    TYPE_ANSWER_CHOICE = (
        (A, 'Boolean'),
        (B, 'Multiple choice one correct'),
        (C, 'Multiple choice more than one is correct'),
        (D, 'Multiple choice more than one answer is correct all of them mustbe answered correctly'),
    )
    question = models.TextField()
    number = models.IntegerField()
    lessons = models.ForeignKey(Lessons, on_delete=models.CASCADE, blank=True, null=True)
    type = models.CharField(max_length=4, choices=TYPE_ANSWER_CHOICE)
    created_by = models.ForeignKey(Professors, blank=True, null=True, on_delete=models.SET_NULL)
    score = models.IntegerField()
    created = models.DateTimeField(db_column='created', auto_now_add=True)
    updated = models.DateTimeField(db_column='updated', auto_now=True)

    class Meta:
        managed = True
        db_table = 'questions'


class Answers(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, blank=True, null=True)
    value = models.TextField()
    correct = models.BooleanField()
    created = models.DateTimeField(db_column='created', auto_now_add=True)
    updated = models.DateTimeField(db_column='updated', auto_now=True)

    class Meta:
        managed = True
        db_table = 'answers'


class ScoreStudent(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.SET_NULL, null=True)
    score = models.IntegerField(default=0)
    created = models.DateTimeField(db_column='created', auto_now_add=True)
    updated = models.DateTimeField(db_column='updated', auto_now=True)

    class Meta:
        managed = True
        db_table = 'scoreStudent'
