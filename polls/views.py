from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db.models import F
from django.utils import timezone

from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_questions'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    # model = Question
    template_name = 'polls/detail.html'
    context_object_name = 'question'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultslView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    context_object_name = 'question'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', 
            {'question': question, 'error_message': 'Please select an answere.'})
    else:
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
