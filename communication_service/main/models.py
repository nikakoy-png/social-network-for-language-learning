from asgiref.sync import sync_to_async
from django.db import models
from django.db.models import Q


class DialogStatusENUM(models.TextChoices):
    active = 'active', 'Active'
    inactive = 'inactive', 'Inactive'


class Dialog(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    end_date = models.DateTimeField(null=True)
    last_activity = models.DateTimeField(auto_now=True, null=False)
    status = models.CharField(choices=DialogStatusENUM.choices, default=DialogStatusENUM.active, null=False)

    @classmethod
    async def create_dialog(cls, user_id_1, user_id_2):
        try:
            if await sync_to_async(cls.dialog_exists)(user_id_1, user_id_2):
                raise ValueError("Dialog already exists between these users")

            # Создание нового диалога
            dialog = await cls.objects.acreate()

            await UserDialog.objects.acreate(user_id=user_id_1, dialog=dialog)
            await UserDialog.objects.acreate(user_id=user_id_2, dialog=dialog)

            return dialog
        except Exception as e:
            print(e)

    @staticmethod
    def dialog_exists(user_id_1, user_id_2):
        try:
            return Dialog.objects.filter(
                userdialog__user_id=user_id_1
            ).filter(
                userdialog__user_id=user_id_2
            ).exists()
        except Exception as e:
            print(e)


class UserDialogQuerySet(models.QuerySet):
    def is_user_in_dialog(self, user_id) -> bool:
        return self.filter(user_id=user_id).exists()


class UserDialog(models.Manager):
    def get_queryset(self):
        return UserDialogQuerySet(self.model, using=self._db)

    def is_user_in_dialog(self, user_id) -> bool:
        return self.get_queryset().is_user_in_dialog(user_id)


class UserDialog(models.Model):
    user_id = models.IntegerField(null=False)
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE, null=False)
    unread_messages = models.IntegerField(default=0, null=False)
    is_deleted = models.BooleanField(default=False, null=False)

    objects = models.Manager()
    func = UserDialog()

    def increment_unread_messages(self):
        self.unread_messages += 1
        self.save()

    def decrement_unread_messages(self):
        self.unread_messages -= 1
        self.save()

    @classmethod
    async def get_dialog_by_id(cls, dialog_id, user_id):
        try:
            return await sync_to_async(cls.objects.filter(Q(dialog__id=dialog_id) & Q(user_id=user_id)).first)()
        except cls.DoesNotExist:
            raise cls.DoesNotExist()

    @classmethod
    async def get_companion_dialog_by_id(cls, dialog_id, user_id):
        try:
            return await sync_to_async(cls.objects.filter(Q(dialog__pk=dialog_id) & ~Q(user_id=user_id)).first)()
        except cls.DoesNotExist:
            raise cls.DoesNotExist()


class Feedback(models.Model):
    user_id = models.IntegerField(null=False)
    correction_text = models.TextField(null=False)
    description = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)


class Message(models.Model):
    feedback = models.ForeignKey(Feedback, default=None, on_delete=models.CASCADE, null=True, related_name='feedback')
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE, null=False)
    sender_id = models.IntegerField(null=False)
    text = models.TextField(null=False)
    send_date = models.DateTimeField(auto_now_add=True, null=False)
    is_read = models.BooleanField(default=False, null=False)
    is_deleted = models.BooleanField(default=False, null=False)


class ComplaintStatusENUM(models.TextChoices):
    processing = 'processing', 'Processing'
    done = 'done', 'Done'


class Complaint(models.Model):
    admin_id = models.IntegerField(null=True)
    user_id = models.IntegerField(null=False)
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    description = models.TextField(null=False)
    status = models.CharField(choices=ComplaintStatusENUM.choices, default=ComplaintStatusENUM.processing,
                              null=False)
    resolution = models.TextField(null=True)


class GenderENUM(models.TextChoices):
    male = 'male', 'Male'
    female = 'female', 'Female'
    other = 'other', 'Other'


class OnlineStatusENUM(models.TextChoices):
    online = 'online', 'Online'
    offline = 'offline', 'Offline'
    away = 'away', 'Away'


#############################################

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
    is_active = models.BooleanField(default=True)

###################################
