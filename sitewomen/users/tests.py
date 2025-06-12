from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class RegisterUserTestCase(TestCase):
    fixtures = ["users_permissions.json"]

    def setUp(self):
        self.data = {
            'username': 'user_1',
            'email': 'user1@sitewomen.ru',
            'first_name': 'Sergey',
            'last_name': 'Balakirev',
            'password1': '12345678Aa',
            'password2': '12345678Aa',
        }

    def test_form_registration_get(self):
        path = reverse("users:registration")
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/registration.html")

    def test_form_registration_success(self):
        user_model = get_user_model()
        path = reverse('users:registration')
        response = self.client.post(path, self.data)
        self.assertRedirects(response, reverse('users:registration_done'), HTTPStatus.FOUND, HTTPStatus.OK)
        self.assertTrue(user_model.objects.filter(username=self.data['username']).exists())

    def test_user_registration_password_error(self):
        self.data["password2"] = '12345678A'
        path = reverse("users:registration")
        response = self.client.post(path, self.data)
        form = response.context['form']
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("Введенные пароли не совпадают.", form.errors["password2"])

    def test_user_registration_username_error(self):
        path = reverse("users:registration")
        user_model = get_user_model()
        user_model.objects.create(username=self.data["username"])
        response = self.client.post(path, self.data)
        form = response.context['form']
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("Пользователь с таким именем уже существует.", form.errors["username"])