from django.http.response import Http404
from django.shortcuts import render

from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Question, Choice

def index(request):
    latest_question_list=Question.objects.order_by('-pub_date')[:5]
    context={'latest_question_list':latest_question_list}
    return render(request, 'index.html',context)
def detail(request,question_id):
    try:
        question=Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404('Данного вопроса не существует')
    return render(request, 'detail.html', {'question':question})

def results(request, question_id):
    question=get_object_or_404(Question, pk=question_id)
    return render(request, 'results.html', {'question':question})
@login_required
def vote(request, question_id):
    question=get_object_or_404(Question, pk=question_id)
    try:
        selected_choice=question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'detail.html', {
    'question':question,
    'error_message':"Вы не сделали выбор"        
        })
    else:
        selected_choice.votes+=1
        selected_choice.save()
        return HttpResponseRedirect(reverse('results', args=(question.id,)))
    


