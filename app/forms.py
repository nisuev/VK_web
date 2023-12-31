from django import forms
from app.models import *
from django.shortcuts import get_object_or_404

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)
    email = forms.EmailField()
    confirm_password = forms.CharField(max_length=255, widget=forms.PasswordInput)
    age = forms.IntegerField()
    avatar = forms.ImageField()

    def create_user(self):
        new_user =  User.objects.create_user(
                   username=self.cleaned_data['username'],
                   password=self.cleaned_data['password'],
                   email=self.cleaned_data['email'],
                   is_superuser=False
                        )
        new_profile = Profile.objects.create(avatar=self.cleaned_data['avatar'], age=self.cleaned_data['age'], user=new_user)

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if confirm_password != password:
            msg = "Password and Confirm Passwords must match."
            self.add_error('confirm_password', msg)


class EditProfileForm(forms.Form):

    username = forms.CharField(max_length=255)
    email = forms.EmailField()
    avatar = forms.ImageField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(EditProfileForm, self).__init__(*args, **kwargs)

    def save(self):
        self.user.username = self.cleaned_data.get('username')
        self.user.email = self.cleaned_data.get('email')
        user_profile = Profile.objects.get(user=self.user)
        user_profile.avatar = self.cleaned_data.get('avatar')
        self.user.save()
        user_profile.save()

    def clean_username(self):
        check_user = User.objects.filter(username=self.cleaned_data.get('username'))
        if check_user.count() and check_user[0] != self.user:
            raise forms.ValidationError(
                u'Пользователь с таким username уже существует'
            )
        return self.cleaned_data.get('username')

    def clean_email(self):
        check_user = User.objects.filter(email=self.cleaned_data.get('email'))
        if check_user.count()  and check_user[0] != self.user:
            raise forms.ValidationError(
                u'Пользователь с таким email уже существует'
            )
        return self.cleaned_data.get('email')


class AddQuestionForm(forms.Form):
    title = forms.CharField(max_length=500)
    text = forms.CharField(widget=forms.Textarea)
    tag = forms.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AddQuestionForm, self).__init__(*args, **kwargs)

    def save(self):
        check_tag = Tag.objects.filter(title=self.cleaned_data.get('tag'))
        if check_tag.count() == 0:
            new_tag = Tag.objects.create(title=self.cleaned_data.get('tag'))
            set_tag = new_tag
        else:
            set_tag = check_tag[0]

        q_n = Question.Qmanager.create(
            title=self.cleaned_data.get('title'),
            text=self.cleaned_data.get('text'),
            author=self.user,
            rate=0,
            tag=set_tag
        )
        return q_n


class AddAnswerForm(forms.Form):
    text = forms.CharField(max_length=255)
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.question = kwargs.pop('question', None)
        super(AddAnswerForm, self).__init__(*args, **kwargs)
        
    def save(self):
        
        a_n = Answer.objects.create(
            text = self.cleaned_data.get("text"),
            author = self.user,
            question = self.question
        )
        
        return a_n