from rest_framework.serializers import ModelSerializer
from api.models import Students, Professors, Courses, Lessons, Questions, Answers, ScoreStudent


class StudentsSerializer(ModelSerializer):

    class Meta:
        model = Students
        depth = 2
        fields = '__all__'


class ProfessorsSerializer(ModelSerializer):

    class Meta:
        model = Professors
        depth = 2
        fields = '__all__'


class CoursesSerializer(ModelSerializer):

    class Meta:
        model = Courses
        exclude = ('created_by',)
        depth = 1


class LessonsSerializer(ModelSerializer):

    class Meta:
        model = Lessons
        depth = 2
        fields = '__all__'


class QuestionsSerializer(ModelSerializer):

    class Meta:
        model = Questions
        depth = 2
        fields = '__all__'


class AnswersSerializer(ModelSerializer):

    class Meta:
        model = Answers
        depth = 2
        fields = '__all__'


class ScoreStudentSerializer(ModelSerializer):

    class Meta:
        model = ScoreStudent
        depth = 2
        fields = '__all__'
