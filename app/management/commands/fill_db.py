from django.core.management.base import BaseCommand, CommandError
from app.models import *
from random import randint
from django.core.files.images import ImageFile


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('ratio', nargs='+', type=int)

    def handle(self, *args, **options):
        for user_id in range(1,int(options['ratio'][0])+1):
           with open("uploads/avatar.jpg", "rb") as f:
               avatar_file = ImageFile(f)
               user = User.objects.create_user(
                   username=f'user_0_{user_id}',
                   password=f'user_pass_{user_id}',
                   is_superuser=False
                )
               profile = Profile.objects.create(avatar=avatar_file, age=randint(1,100), user=user)
               tag = Tag.objects.create(title=f"Tag #{user_id}")
           for q_i in range(10):
               question = Question.Qmanager.create(
                   title=f"Some title #{user_id}__{q_i}",
                   text=f"Some interesting text #{user_id}_{q_i}",
                   author=user,
                   rate=randint(1,100),
                   tag=tag
               )

        questions = Question.Qmanager.all().order_by("?")
        users = User.objects.all().order_by("?")
        for q in range(100):
            user_id = randint(0,int(options['ratio'][0])-1)
            ans = Answer.objects.create(
                text=f"Some text for answer #{user_id} for question #{questions[q].id}",
                author=users[user_id],
                question=questions[q]
            )
        for q in range(200):
            user_id = randint(0, int(options['ratio'][0]) - 1)
            like = Like.objects.create(
                user=users[user_id],
                question=questions[q]
            )
