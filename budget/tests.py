from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from budget.factory import BudgetFactory, ExpenseBudgetFactory, IncomeBudgetFactory


class BaseTestCase(TestCase):
    def setUp(self):
        self.batman = User.objects.create(username="Batman")
        self.batman.set_password("password")
        self.batman.save()

        self.star_lord = User.objects.create(username="Star Lord")
        self.star_lord.set_password("galaxy")
        self.star_lord.save()

    def authorize(self, user):
        token, created = Token.objects.get_or_create(user=user)
        self.client = Client(HTTP_AUTHORIZATION="Token " + token.key)


class UserCreateTest(TestCase):
    def test_can_create(self):
        url = reverse("register")
        response = self.client.post(url, {"username": "Batman@gottham.com", "password": "abc321"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="Batman").exists())


class BudgetListTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.home_budget = BudgetFactory.create(owners=[self.batman])
        self.home_incomes = IncomeBudgetFactory.create_batch(2, budget=self.home_budget)
        self.home_expenses = ExpenseBudgetFactory.create_batch(2, budget=self.home_budget)

        self.business_budget = BudgetFactory.create(owners=[self.batman])
        self.business_incomes = IncomeBudgetFactory.create_batch(2, budget=self.business_budget)
        self.business_expenses = ExpenseBudgetFactory.create_batch(2, budget=self.business_budget)

        self.vacation_budget = BudgetFactory.create(owners=[self.batman, self.star_lord])
        self.vacation_incomes = IncomeBudgetFactory.create_batch(2, budget=self.vacation_budget)
        self.vacation_expenses = ExpenseBudgetFactory.create_batch(2, budget=self.vacation_budget)

    def test_unauthorized_cant_access(self):
        response = self.client.post(reverse("budget-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_simple_list_budgets(self):
        self.authorize(self.batman)
        response = self.client.get(reverse("budget-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_list_only_owners_budgets(self):
        self.authorize(self.star_lord)
        response = self.client.get(reverse("budget-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.vacation_budget.id)
