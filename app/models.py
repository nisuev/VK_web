from django.db import models
from django.contrib.auth.models import User


def generate_user_directory(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Profile(models.Model):
    avatar = models.ImageField(upload_to=generate_user_directory)
    age = models.IntegerField(blank=True)
    last_online = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )


class QuestionManager(models.Manager):
    def get_by_tag(self, tag):
        tag_m = Tag.objects.get(pk=tag)
        return super().get_queryset().filter(tag=tag_m)


class Question(models.Model):
    title = models.CharField(max_length=500)
    text = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.IntegerField()
    tag = models.ForeignKey(
        'Tag',
        on_delete=models.CASCADE,
    )
    Qmanager = QuestionManager()


class Answer(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE,
    )
    create_date = models.DateTimeField(auto_now_add=True, blank=True)


class Tag(models.Model):
    title = models.CharField(max_length=255)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE,
    )
    create_date = models.DateTimeField(auto_now_add=True, blank=True)

