from graphene_django import DjangoObjectType
import graphene

from .models import Choice, Question


class QuestionType(DjangoObjectType):
    class Meta:
        model = Question


class ChoiceType(DjangoObjectType):
    class Meta:
        model = Choice


class Query(graphene.ObjectType):
    all_questions = graphene.List(QuestionType)
    question = graphene.Field(QuestionType, 
                              id=graphene.Int())

    def resolve_all_questions(self, info):
        return Question.objects.all()
    
    def resolve_question(self, info, **kwargs):
        q_id = kwargs.get('id')

        if q_id is not None:
            return Question.objects.get(pk=q_id)
        return None

schema = graphene.Schema(query=Query)