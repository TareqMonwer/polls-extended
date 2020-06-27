from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.views.generic.base import TemplateResponseMixin
from django.db.models import F
from django.utils import timezone

from .models import Question, Choice
from .mixins import RequireLoginMixin


class IndexView(RequireLoginMixin, generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_questions'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    template_name = 'polls/detail.html'
    context_object_name = 'question'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultslView(TemplateResponseMixin, generic.View):

    template_name = 'polls/results.html'

    def get_queryset(self, question_id):
        return Question.objects.get(pk=question_id)
    
    def get(self, request, pk):
        qs = self.get_queryset(pk)
        context = {'question': qs}
        return self.render_to_response(context)


class DeleteView(generic.DeleteView):
    model = Question
    template_name = "polls/delete.html"
    success_url = "/"


# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         return render(request, 'polls/detail.html', 
#             {'question': question, 'error_message': 'Please select an answere.'})
#     else:
#         selected_choice.votes = F('votes') + 1
#         selected_choice.save()
#         return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


class VoteView(generic.View):

    def get_queryset(self, choice_id):
        return Choice.objects.get(pk=choice_id)
    
    def post(self, request, pk):
        question_id = pk
        choice_id = request.POST.get('choice', None)
        try:
            qs = self.get_queryset(choice_id)
        except (KeyError, Choice.DoesNotExist):
            return redirect('polls:detail', pk=question_id)
        else:
            qs.votes += 1
            qs.save()
            return redirect('polls:vote_result', pk=question_id)



class SwitchboardView(generic.View):
    def get(self, request, pk):
        view = ResultslView.as_view()
        return view(request, pk)
    
    def post(self, request, pk):
        view = VoteView.as_view()
        return view(request, pk)