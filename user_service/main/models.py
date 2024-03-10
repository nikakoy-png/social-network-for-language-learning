from asgiref.sync import sync_to_async
from django.db import models
from django.db.models import Q
from django.db.models import Prefetch


class Language(models.Model):
    title = models.CharField(max_length=255, null=False, unique=True)

    def __str__(self):
        return self.title


class LevelLanguageENUM(models.TextChoices):
    A1 = 'a1', 'A1'
    A2 = 'a2', 'A2'
    B1 = 'b1', 'B1'
    B2 = 'b2', 'B2'
    C1 = 'c1', 'C1'
    C2 = 'c2', 'C2'

    @classmethod
    def get_all_levels(cls):
        return [choice for choice in cls.values]


class UserLanguages(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    proficiency_level = models.CharField(choices=LevelLanguageENUM.choices, null=False, default=LevelLanguageENUM.A1)
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
        proficient_languages = user.languages.exclude(
            userlanguages__is_learning=False,
            # ~Q(userlanguages__proficiency_level__in=[LevelLanguageENUM.а1, LevelLanguageENUM.а2, LevelLanguageENUM.b1]) \
            # einfach Test
            #     &
            # Q(languages__in=list_language_levels[list_language_levels.index(
            #     proficient_languages.values('userlanguages__proficiency_level', flat=True)
            # ):])
        )
        # list_language_levels = LevelLanguageENUM.get_all_levels()
        prefetch_proficient_languages = Prefetch('languages', queryset=proficient_languages)
        users_suitable = self.filter(Q(languages__in=proficient_languages) &
                                     ~Q(pk=user.pk)
                                     ).prefetch_related(prefetch_proficient_languages).order_by(
            '-userlanguages__proficiency_level'
        ).distinct()
        return users_suitable


class UserManager(models.Manager):
    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)

    def get_list_suitable_users(self, user):
        return self.get_queryset().sort_by_skills_user(user)


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
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [
        'email',
        'first_name',
        'last_name',
        'password',
        'password_confirm',
        'phone',
        'gender',
        'photo',
        'birth_date'
    ]

    objects = models.Manager()
    func = UserManager()


    """Dies ist für "Einstellungen", weil es AUTH_USER_MODEL braucht, um gut zu funktionieren.
    Aber ich verwende JWT anstelle von Django Session, also brauche ich dieses Attribut nicht. 
     Es hat keinen Einfluss auf die Gesamtleistung, es ist lediglich ein Hinweis auf Migrationsfehler."""
    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
