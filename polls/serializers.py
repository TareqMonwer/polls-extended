from .models import Question, Choice
from rest_framework import serializers


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('question', 'choice_text', 'votes')


class QuestionSerializer(serializers.ModelSerializer):
    choice_set = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('question_text', 'pub_date', 'choice_set')
