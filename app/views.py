from django.shortcuts import render
import random
from django.http import HttpResponse, HttpResponseNotFound

from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from .forms import *


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
    return questions
    #page = HttpResponse(template.render(questions, request))
    #return page


def index(request):
    context = Question.Qmanager.all().order_by('create_date').values()
    tags = Tag.objects.all()
    return render(request, "index.html", {
        "questions": paginate(context, request),
        'tags':tags
    })


def hot(request):
    context = Question.Qmanager.all().order_by('rate').values()
    tags = Tag.objects.all()
    return render(request, "index.html", {
        "questions": paginate(context, request),
        'tags': tags
    })


def tag(request, id):
    tags = Tag.objects.all()
    context = Question.Qmanager.get_by_tag(id)
    return render(request, "index.html", {
        "questions": paginate(context, request),
        "tags": tags
    })


def question(request, id):
    template = loader.get_template('question.html')
    context = Question.Qmanager.get(pk=id)
    likes = Like.objects.all().filter(question=context)
    if not context :
        return HttpResponseNotFound(f"Not found question with id {id}")
    return render(request, "question.html", {"question": context, 'likes': likes})
    #return HttpResponse(template.render(context, request))


def login(request):
    if request.method == 'GET':
        loginForm = LoginForm()
        continueUrl = request.GET.get('continue')
        if continueUrl is None:
            continueUrl = "index"
        return render(request, "index.html", {
            "loginForm":loginForm,

        })


def signup(request):
    template = loader.get_template('index.html')
    context = {
        'JSevent': "openQuestionForm()"
    }
    return HttpResponse(template.render(context, request))
