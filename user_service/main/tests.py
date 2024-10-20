from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from main.models import User, Language, UserLanguages


class TestViews(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password': 'password123',
            'username': 'johndoe',
            'phone': '1234567890',
            'gender': 'male',
            'birth_date': '1990-01-01',
            'status': 'online',
        }
        self.user = User.objects.create(**self.user_data)
        self.language = Language.objects.create(title='English')
        self.user_languages = UserLanguages.objects.create(user=self.user, language=self.language,
                                                           proficiency_level='B1')

    def test_create_user(self):
        url = reverse('register')
        data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane@example.com',
            'password': 'janepassword123',
            "password_confirm": 'janepassword123',
            'username': 'janedoe',
            'phone': '9876543210',
            'gender': 'female',
            'birth_date': '1995-05-05',
            'status': 'offline',
            'photo': 'media/user_photos/das-gewisse-etwas.jpg'
        }
        response = self.client.post(url, data)
        if response.status_code != status.HTTP_201_CREATED:
            self.fail(
                f"Failed to create user. Got status code {response.status_code}, expected {status.HTTP_201_CREATED}. Response content: {response.content.decode('utf-8')}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_login_user(self):
    #     url = reverse('login')
    #     data = {
    #         'username': self.user_data['username'],
    #         'password': self.user_data['password'],
    #     }
    #     response = self.client.post(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) # 232132132132132132132132121321321321321wrwerwq

    def test_get_profile(self):
        url = reverse('get_self_user_profile')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_profile(self):
        url = reverse('update_profile')
        self.client.force_authenticate(user=self.user)
        data = {
            'first_name': 'Updated Name',
            'last_name': 'Updated Last Name',
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated Name')
        self.assertEqual(self.user.last_name, 'Updated Last Name')

    def test_get_user_by_id(self):
        url = reverse('get_user_by_id', kwargs={'user_id': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_languages(self):
        url = reverse('get_list_languages')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_language(self):
        url = reverse('add_language_to_user')
        self.client.force_authenticate(user=self.user)
        data = {'language_id': self.language.id}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.languages.filter(id=self.language.id).exists())

    def test_delete_language(self):
        self.user.languages.add(self.language)
        url = reverse('delete_languages_from_user')
        self.client.force_authenticate(user=self.user)
        data = {'language_id': 21}
        response = self.client.delete(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.user.refresh_from_db()
        self.assertTrue(self.user.languages.filter(id=self.language.id).exists())

    def test_get_suitable_users(self):
        url = reverse('get_suitable_users')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


import datetime
from django.test import TestCase
from .models import Language, LevelLanguageENUM, UserLanguages, GenderENUM, OnlineStatusENUM, User


class LanguageModelTest(TestCase):
    def test_title_label(self):
        language = Language.objects.create(title='English')
        field_label = language._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_title_max_length(self):
        language = Language.objects.create(title='English')
        max_length = language._meta.get_field('title').max_length
        self.assertEqual(max_length, 255)

    def test_str_method(self):
        language = Language.objects.create(title='English')
        self.assertEqual(str(language), 'English')


class UserLanguagesModelTest(TestCase):
    def test_language_label(self):
        language = Language.objects.create(title='English')
        user = User.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            password='password123',
            username='johndoe',
            phone='1234567890',
            birth_date=datetime.date(1990, 1, 1),
            gender=GenderENUM.male,
            status=OnlineStatusENUM.online
        )
        user_language = UserLanguages.objects.create(language=language, user=user)
        field_label = user_language._meta.get_field('language').verbose_name
        self.assertEqual(field_label, 'language')

    def test_user_label(self):
        language = Language.objects.create(title='English')
        user = User.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            password='password123',
            username='johndoe',
            phone='1234567890',
            birth_date=datetime.date(1990, 1, 1),
            gender=GenderENUM.male,
            status=OnlineStatusENUM.online
        )
        user_language = UserLanguages.objects.create(language=language, user=user)
        field_label = user_language._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')

    def test_proficiency_level_default(self):
        language = Language.objects.create(title='English')
        user = User.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            password='password123',
            username='johndoe',
            phone='1234567890',
            birth_date=datetime.date(1990, 1, 1),
            gender=GenderENUM.male,
            status=OnlineStatusENUM.online
        )
        user_language = UserLanguages.objects.create(language=language, user=user)
        self.assertEqual(user_language.proficiency_level, LevelLanguageENUM.A1)

    def test_is_learning_default(self):
        language = Language.objects.create(title='English')
        user = User.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            password='password123',
            username='johndoe',
            phone='1234567890',
            birth_date=datetime.date(1990, 1, 1),
            gender=GenderENUM.male,
            status=OnlineStatusENUM.online
        )
        user_language = UserLanguages.objects.create(language=language, user=user)
        self.assertTrue(user_language.is_learning)

    def test_unique_together_constraint(self):
        language = Language.objects.create(title='English')
        user = User.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            password='password123',
            username='johndoe',
            phone='1234567890',
            birth_date=datetime.date(1990, 1, 1),
            gender=GenderENUM.male,
            status=OnlineStatusENUM.online
        )
        UserLanguages.objects.create(language=language, user=user)
        with self.assertRaises(Exception) as context:
            UserLanguages.objects.create(language=language, user=user)
        self.assertFalse('UNIQUE constraint' in str(context.exception))


class UserModelTest(TestCase):
    def test_first_name_label(self):
        user = User.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            password='password123',
            username='johndoe',
            phone='1234567890',
            birth_date=datetime.date(1990, 1, 1),
            gender=GenderENUM.male,
            status=OnlineStatusENUM.online
        )
        field_label = user._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    # Тесты для остальных полей аналогично

    def test_username_unique(self):
        User.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            password='password123',
            username='johndoe',
            phone='1234567890',
            birth_date=datetime.date(1990, 1, 1),
            gender=GenderENUM.male,
            status=OnlineStatusENUM.online
        )
        with self.assertRaises(Exception) as context:
            User.objects.create(
                first_name='Jane',
                last_name='Doe',
                email='jane@example.com',
                password='password123',
                username='johndoe',  # Повторяющееся имя пользователя
                phone='1234567890',
                birth_date=datetime.date(1990, 1, 1),
                gender=GenderENUM.female,
                status=OnlineStatusENUM.online
            )
        self.assertFalse('UNIQUE constraint' in str(context.exception))

    def test_str_method(self):
        user = User.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            password='password123',
            username='johndoe',
            phone='1234567890',
            birth_date=datetime.date(1990, 1, 1),
            gender=GenderENUM.male,
            status=OnlineStatusENUM.online
        )
        self.assertEqual(str(user), 'John Doe')