from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token


class BaseTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="Batman")
        self.user.set_password("password")
        self.user.save()

    def authorize(self):
        token, created = Token.objects.get_or_create(user=self.user)
        self.client = Client(HTTP_AUTHORIZATION="Token " + token.key)


class UserCreateTest(TestCase):
    def test_can_create(self):
        url = reverse("register")
        response = self.client.post(url, {"username": "Batman@gottham.com", "password": "abc321"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="Batman").exists())


class BudgetListTest(BaseTestCase):
    def test_unauthorized_cant_access(self):
        response = self.client.post(reverse("budget-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_simple_list_budgets(self):
        self.authorize()
        response = self.client.post(reverse("budget-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
