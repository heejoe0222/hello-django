#from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
#from django.views import generic

from django.db.models import F
from .models import Question, Choice


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #template =loader.get_template('polls/index.html')
    context = { ## template 변수명과 python 객체 연결하는 dictionary
        'latest_question_list': latest_question_list,
    }
    #return HttpResponse(template.render(context,request))
    return render(request,'polls/index.html',context) ## HttpResponse, loader 안 써도 됨

def detail(request, question_id):
    '''
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    '''
    question = get_object_or_404(Question, pk=question_id)
    return render(request,'polls/detail.html', {'question':question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request,'polls/results.html', {'question':question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist): ## choice 없으면 request.post['choice']가 keyerror 발생시킴
        return render(request, 'polls/detail.html', {'question':question, 'error_message': "You didn't select a choice!",})
    else:
        #selected_choice.votes += 1
        selected_choice.votes = F('votes') + 1 ## Avoid race condition
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',args=(question.id,))) ## post 데이터 성공적으로 처리하면 리턴해주기
