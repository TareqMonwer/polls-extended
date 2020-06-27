from rest_framework import viewsets
from rest_framework.response import Response

from .api_auth import AdminOnlyAuth
from .serializers import QuestionSerializer, ChoiceSerializer
from .models import Question, Choice



class QuestionViewSet(viewsets.ModelViewSet):
    authentication_classes = (AdminOnlyAuth, )
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

