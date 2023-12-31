from django.shortcuts import render
import random
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect

from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login
from django.contrib.auth import login as login_django, logout as logout_django
import json
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
    # page = HttpResponse(template.render(questions, request))
    # return page


def index(request):
    context = Question.Qmanager.all().order_by('create_date').values()
    profile = Profile.objects.get(user=request.user)
    tags = Tag.objects.all()
    return render(request, "index.html", {
        "questions": paginate(context, request),
        'tags': tags,
        'profile': profile
    })


def hot(request):
    profile = Profile.objects.get(user=request.user)
    context = Question.Qmanager.all().order_by('rate').values()
    tags = Tag.objects.all()
    return render(request, "index.html", {
        "questions": paginate(context, request),
        'tags': tags,
        'profile': profile
    })


def tag(request, id):
    tags = Tag.objects.all()
    profile = Profile.objects.get(user=request.user)
    context = Question.Qmanager.get_by_tag(id)
    return render(request, "index.html", {
        "questions": paginate(context, request),
        "tags": tags,
        'profile': profile
    })


def question(request, id):
    context = Question.Qmanager.get(pk=id)
    profile = Profile.objects.get(user=request.user)
    likes = Like.objects.all().filter(question=context)
    context.rate = likes.count()
    context.save()
    is_show_like = True
    if Like.objects.filter(user=request.user, question=context).count() != 0 or context.author == request.user:
        is_show_like = False
    answers = Answer.objects.filter(question=context).order_by("create_date")
    form = AddAnswerForm(user=request.user, question=context)
    if request.method == "GET":
        if not context:
            return HttpResponseNotFound(f"Not found question with id {id}")
        return render(request, "question.html", {
            "question": context,
            'likes': likes,
            'profile': profile,
            'AddQuestionForm': form,
            'answers': answers,
            'is_show_like': is_show_like
        })
    if request.method == "POST":
        form = AddAnswerForm(request.POST, user=request.user, question=context)
        if form.is_valid():
            return redirect(f'/question/{context.pk}#answer-'+str(form.save().pk))
        else:
            return render(request, "question.html", {
                "question": context,
                'likes': likes,
                'profile': profile,
                'AddQuestionForm': form,
                'answers': answers,
                'is_show_like': is_show_like
            })

    # return HttpResponse(template.render(context, request))


def login(request):
    if request.method == 'GET':
        loginForm = LoginForm()
        continueUrl = request.GET.get('continue')
        if continueUrl is None:
            continueUrl = "index"
        return render(request, "login.html", {
            "loginForm": loginForm,
            "continueUrl": continueUrl
        })
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        continueUrl = request.POST['continueUrl']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login_django(request, user)
            return redirect(continueUrl)
        else:
            loginForm = LoginForm()
            return render(request, "login.html", {
                "loginForm": loginForm,
                "continueUrl": "index",
                'error': "Неверный логин или пароль"
            })


def signup(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, "signup.html", {
            "RegisterForm": form,
        })
    if request.method == "POST":

        form = RegisterForm(request.POST, request.FILES)

        if form.is_valid():
            form.create_user()
            return redirect('index')
        else:
            print(form.errors)
            return render(request, "signup.html", {
                "RegisterForm": form
            })


def logout(request):
    logout_django(request)
    return redirect('index')


def settings(request):
    if not request.user.is_authenticated:
        redirect("index")
    if request.method == 'GET':
        profile = Profile.objects.get(user=request.user)
        form = EditProfileForm(initial={'username': request.user.username, 'email': request.user.email }, user=request.user)
        return render(request, "settings.html", {'profile': profile, 'EditProfileForm':form})
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('settings')
        else:
            profile = Profile.objects.get(user=request.user)
            return render(request, "settings.html", {
                "EditProfileForm": form,
                'profile': profile
            })


def ask(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'GET':
        form = AddQuestionForm(user=request.user)
        return render(request, "ask.html", {
            "AddQuestionForm": form,
            'profile': profile
        })
    if request.method == "POST":

        form = AddQuestionForm(request.POST,user=request.user)

        if form.is_valid():
            return redirect('question', id=form.save().pk)
        else:
            return render(request, "ask.html", {
                "AddQuestionForm": form,
                'profile': profile
            })


def like(request):
    if not request.user.is_authenticated:
        return HttpResponse(
            json.dumps({"error": True, "error_text": "you are not authenticated"}),
            content_type="application/json"
        )
    q_id = request.POST.get('question')
    q = Question.Qmanager.get(pk=q_id)
    check_like =  Like.objects.filter(question=q, user=request.user)
    if check_like.count() != 0:
        return HttpResponse(
            json.dumps({"error": True, "error_text": "You just like this question"}),
            content_type="application/json"
        )

    Like.objects.create(
        user=request.user,
        question=q
    )
    likes = Like.objects.filter(question=q)
    return HttpResponse(
        json.dumps({"error": False, "new_like_count": likes.count()}),
        content_type="application/json"
    )


def set_right(request):
    if not request.user.is_authenticated:
        return HttpResponse(
            json.dumps({"error": True, "error_text": "you are not authenticated"}),
            content_type="application/json"
        )
    q_id = request.POST.get('question')
    a_id = request.POST.get('answer')
    q = Question.Qmanager.get(pk=q_id)

    if q.author != request.user:
        return HttpResponse(
            json.dumps({"error": True, "error_text": "you are not author"}),
            content_type="application/json"
        )
    ans = Answer.objects.get(pk=a_id)
    ans.is_right = True
    ans.save()
    return HttpResponse(
        json.dumps({"error": False}),
        content_type="application/json"
    )

