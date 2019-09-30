#from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.db.models import F

from .models import Question, Choice

class IndexView(generic.ListView):  # ListView -> objct 목록 표시
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        now = timezone.localtime()
        return Question.objects.filter(pub_date__lte = now).order_by('-pub_date')[:5]
        # gt: greater than, gte:greater than or equal to, lt: less than, lte: Less than or equal to


class DetailView(generic.DetailView):  # DetailView -> 특정 object에 대한 세부 정보 페이지 표시
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        now = timezone.localtime()
        return Question.objects.filter(pub_date__lte=now)


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):  # choice 없으면 request.post['choice']가 keyerror 발생시킴
        return render(request, 'polls/detail.html', {'question':question, 'error_message': "You didn't select a choice!",})
    else:
        # selected_choice.votes += 1
        selected_choice.votes = F('votes') + 1  # Avoid race condition
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))  # post 데이터 성공적으로 처리하면 리턴해주기
