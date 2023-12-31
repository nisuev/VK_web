from django.shortcuts import render
import random
from django.http import HttpResponse
from django.template import loader
from random import randint
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginate(objects_list, request, per_page=10):
    pag = Paginator(tuple(objects_list), per_page)
    page_number = request.GET.get('page')
    if page_number is not None:
        try:
            questions = pag.get_page(page_number)
        except PageNotAnInteger:
            questions = pag.get_page(1)
        except EmptyPage:
            questions = pag.get_page(pag.num_pages)
    else:
        questions = pag.get_page(1)
    return render(request, "index.html", {"questions": questions})
    #page = HttpResponse(template.render(questions, request))
    #return page

questions = []
tags = ["HTML", "PHP", "Python", "Javascript", "Суета"]
for i in range(1, 30):
    questions.append({
        'title': "title " + str(i),
        'id': i,
        'text': 'text' + str(i),
        'date': f"{randint(0, 59)}:{randint(0, 59)}:{randint(0, 23)} {randint(1, 31)}-{randint(1, 12)}-{randint(2018, 2022)}",
        'is_hot': (i % 2 == 0) and (i % 3 == 0),
        'rate': randint(0, 100),
        'tag': tags[randint(0, 4)]
    })


def index(request):
    context = sorted(questions, key=lambda x: x['date'])
    return paginate(context, request)


def hot(request):
    context = [i for i in questions if i['is_hot']]
    return paginate(context, request)


def tag(request, tag):
    context = [i for i in questions if i['tag'] == tag]
    return paginate(context, request)


def question(request, id):
    template = loader.get_template('question.html')
    context = {
        'question': questions[i - 1],
    }
    return HttpResponse(template.render(context, request))


def login(request):
    template = loader.get_template('login.html')
    context = {}
    return HttpResponse(template.render(context, request))


def signup(request):
    template = loader.get_template('index.html')
    context = {
        'JSevent': "openQuestionForm()"
    }
    return HttpResponse(template.render(context, request))
