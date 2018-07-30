from rest_framework.serializers import ModelSerializer
from api.models import Students, Professors, Courses, Lessons, Questions, Answers, ScoreStudent


class GetStudentsSerializer(ModelSerializer):
    class Meta:
        model = Students
        exclude = ('password', 'token', 'created', 'updated')
        depth = 2


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
        depth = 0


class LessonsSerializer(ModelSerializer):
    class Meta:
        model = Lessons
        exclude = ('created_by',)
        depth = 0


class AddLessonsSerializer(ModelSerializer):
    class Meta:
        model = Lessons
        depth = 0
        fields = '__all__'


class QuestionsSerializer(ModelSerializer):
    class Meta:
        model = Questions
        depth = 0
        fields = '__all__'


class SpecificQuestionSerializer(ModelSerializer):
    class Meta:
        model = Questions
        exclude = ('created', 'updated','created_by','lessons')
        depth = 0


class GetQuestionsSerializer(ModelSerializer):
    class Meta:
        model = Questions
        depth = 1
        fields = '__all__'


class AnswersSerializer(ModelSerializer):
    class Meta:
        model = Answers
        depth = 0
        fields = '__all__'


class GetAnswersSerializer(ModelSerializer):
    class Meta:
        model = Answers
        exclude = ('created', 'updated')
        depth = 0


class ScoreStudentSerializer(ModelSerializer):
    student = GetStudentsSerializer()

    class Meta:
        model = ScoreStudent
        depth = 1
        fields = '__all__'


class PutScoreStudentSerializer(ModelSerializer):
    class Meta:
        model = ScoreStudent
        depth = 0
        fields = '__all__'
