from .models import Question, Choice
from rest_framework import viewsets
from .serializers import QuestionSerializer, ChoiceSerializer

from rest_framework.response import Response


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by('-pub_date')
    serializer_class = QuestionSerializer


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer


class CustomQuestionView(viewsets.ViewSet):
    def list(self, request, format=None):
        questions = [question.question_text 
                    for question in Question.objects.all()]
        return Response(questions)

