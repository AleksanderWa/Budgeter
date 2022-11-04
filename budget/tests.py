from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token


class UserCreateTest(TestCase):
    def test_can_create(self):
        url = reverse("register")
        response = self.client.post(url, {"username": "Batman", "password": "abc321"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="Batman").exists())


class BudgetListTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="Batman", password="password")
        # self.client.login(username='username', password='Pas$w0rd')

    def authorize(self):
        token, created = Token.objects.get_or_create(user=self.user)
        self.client = Client(HTTP_AUTHORIZATION="Token " + token.key)

    def test_unauthorized_cant_access(self):
        response = self.client.post(reverse("budget-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_simple_list_budgets(self):
        self.authorize()
        response = self.client.post(reverse("budget-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
