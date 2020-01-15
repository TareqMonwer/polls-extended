import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
# from django.test import Client

from .models import Question


def create_question(q_text, days):
    ''' creates a question with q_text,
    positive number for future days and negative for past.
    '''
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=q_text, pub_date=time)


class QuestionModelTests(TestCase):

    def test_question_was_published_recently_future_check(self):
        time = timezone.now() + datetime.timedelta(days=10)
        future_qestion = Question(pub_date=time)
        self.assertIs(future_qestion.was_published_recently(), False)
    
    def test_question_was_published_recently_old_check(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)
    
    def test_question_was_published_recently_recent_check(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):

    def test_no_question(self):
        res = self.client.get(reverse('polls:index'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'No polls are available.')
        self.assertQuerysetEqual(res.context['latest_questions'], [])
    
    def test_past_question(self):
        create_question(q_text="Past question.", days=-30)
        res = self.client.get(reverse('polls:index'))
        self.assertEqual(res.status_code, 200)
        self.assertQuerysetEqual(res.context['latest_questions'], ['<Question: Past question.>'])
    
    def test_future_question(self):
        create_question(q_text="Future question.", days=30)
        res = self.client.get(reverse('polls:index'))
        self.assertEqual(res.status_code, 200)
        self.assertQuerysetEqual(res.context['latest_questions'], [])


class QuestionDetailVeiwTests(TestCase):

    def test_past_question(self):
        pq = create_question(q_text="Past question.", days=-30)
        res = self.client.get(reverse('polls:detail', args=(pq.id, )))
        self.assertContains(res, pq.question_text)
    
    def test_future_question(self):
        pq = create_question(q_text="Future question.", days=30)
        res = self.client.get(reverse('polls:detail', args=(pq.id, )))
        self.assertEqual(res.status_code, 404)