from asgiref.sync import sync_to_async
from django.db import models
from django.db.models import Q

class Language(models.Model):
    title = models.CharField(max_length=255, null=False, unique=True)

    def __str__(self):
        return self.title


class LevelLanguageENUM(models.TextChoices):
    а1 = 'a1', 'A1'
    а2 = 'a2', 'A2'
    b1 = 'b1', 'B1'
    b2 = 'b2', 'B2'
    c1 = 'c1', 'C1'
    c2 = 'c2', 'C2'


class UserLanguages(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    proficiency_level = models.CharField(choices=LevelLanguageENUM.choices, null=False, default=LevelLanguageENUM.а1)
    is_learning = models.BooleanField(null=False, default=True)

    class Meta:
        unique_together = ('language', 'user')


class GenderENUM(models.TextChoices):
    male = 'male', 'Male'
    female = 'female', 'Female'
    other = 'other', 'Other'


class OnlineStatusENUM(models.TextChoices):
    online = 'online', 'Online'
    offline = 'offline', 'Offline'
    away = 'away', 'Away'


class UserQuerySet(models.QuerySet):
    def sort_by_skills_user(self, user):
        languages = user.languages.all()
        users_suitable = self.filter(Q(languages__in=languages) & ~Q(pk=user.pk)).distinct()
        print(users_suitable)
        return users_suitable


class UserManager(models.Manager):
    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)

    def get_list_suitable_users(self, languages):
        return self.get_queryset().sort_by_skills_user(languages)


class User(models.Model):
    first_name = models.CharField(max_length=255, null=False, unique=False)
    last_name = models.CharField(max_length=255, null=False, unique=False)
    email = models.EmailField(max_length=255, null=False, unique=True)
    password = models.CharField(max_length=255, null=False, unique=False)
    username = models.CharField(max_length=255, null=False, unique=True)
    phone = models.CharField(max_length=255, null=False, unique=True)
    gender = models.CharField(choices=GenderENUM.choices, null=True)
    photo = models.ImageField(upload_to='user_photos', null=False, default='/default_photo.png')
    registration_date = models.DateTimeField(auto_now_add=True)
    last_active_date = models.DateTimeField(auto_now=True)
    birth_date = models.DateField(null=False)
    status = models.CharField(choices=OnlineStatusENUM.choices, null=False, default=OnlineStatusENUM.online)
    languages = models.ManyToManyField(Language, through=UserLanguages)

    objects = models.Manager()
    func = UserManager()

    @property
    def is_active(self):
        return True

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
