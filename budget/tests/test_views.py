import json

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from budget.factory import BudgetFactory, CategoryFactory, ExpenseBudgetFactory, IncomeBudgetFactory
from budget.models import Budget, BudgetCategory


class BaseTestCase(TestCase):
    def setUp(self):
        self.batman = User.objects.create(username="Batman")
        self.batman.set_password("password")
        self.batman.save()

        self.star_lord = User.objects.create(username="Star Lord")
        self.star_lord.set_password("galaxy")
        self.star_lord.save()

        self.work_category = CategoryFactory(name="work")
        self.food_category = CategoryFactory(name="food")
        self.transport_category = CategoryFactory(name="transport")
        self.furniture_category = CategoryFactory(name="furniture")

    def authorize(self, user):
        token, created = Token.objects.get_or_create(user=user)
        self.client = Client(HTTP_AUTHORIZATION="Token " + token.key)


class UserCreateTest(TestCase):
    def test_can_create(self):
        url = reverse("register")
        response = self.client.post(url, {"username": "Batman", "password": "abc321"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="Batman").exists())


class BudgetListTest(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.home_budget = BudgetFactory.create(name="home", owners=[self.batman])
        self.home_incomes = IncomeBudgetFactory.create_batch(2, budget=self.home_budget, category=self.work_category)
        self.home_expenses = ExpenseBudgetFactory.create_batch(
            2, budget=self.home_budget, category=self.furniture_category
        )

        self.business_budget = BudgetFactory.create(name="business", owners=[self.batman])
        self.business_incomes = IncomeBudgetFactory.create_batch(
            2, budget=self.business_budget, category=self.work_category
        )
        self.business_expenses = ExpenseBudgetFactory.create_batch(
            2, budget=self.business_budget, category=self.food_category
        )

        self.vacation_budget = BudgetFactory.create(name="vacation", owners=[self.batman, self.star_lord])
        self.vacation_incomes = IncomeBudgetFactory.create_batch(
            2, budget=self.vacation_budget, category=self.work_category
        )

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

    def test_list_by_categories(self):
        expected_budget_ids = (self.business_budget.id, self.home_budget.id)
        self.authorize(self.batman)
        response = self.client.get(
            reverse("budget-list"), {"category": [self.food_category.id, self.furniture_category.id]}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(expected_budget_ids))
        for budget in response.data:
            self.assertIn(budget["id"], expected_budget_ids)


class BudgetCreateTest(BaseTestCase):
    def setUp(self):
        super().setUp()

    def test_can_create_empty_budget(self):
        self.authorize(self.batman)
        name = "empty budget"
        response = self.client.post(reverse("budget-list"), {"name": name, "owners": self.batman.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], name)
        self.assertEqual(Budget.objects.count(), 1)

    def test_can_create_budget_with_records(self):
        self.authorize(self.batman)
        name = "Batman's budget"

        data = {
            "name": name,
            "owners": [self.batman.id],
            "records": [{"amount": "25.05"}, {"amount": "-20.12"}, {"amount": "15.00"}, {"amount": "-20.21"}],
        }
        response = self.client.post(
            reverse("budget-list"),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], name)
        self.assertEqual(Budget.objects.count(), 1)

        self.assertEqual(Budget.objects.get(name=name).records.count(), 4)

    def test_budget_not_created_wrong_record_data(self):
        self.authorize(self.batman)
        name = "Batman's budget"

        data = {"name": name, "owners": [self.batman.id], "records": [{"amount": "xxxx"}]}
        response = self.client.post(
            reverse("budget-list"),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_can_create_budget_with_records_and_categories(self):
        self.authorize(self.batman)
        name = "Batman's category budget"

        records = [
            {"amount": "25.05", "category": {"name": "food"}},
            {"amount": "-20.12", "category": {"name": "transport"}},
        ]
        data = {"name": name, "owners": [self.batman.id], "records": records}
        response = self.client.post(
            reverse("budget-list"),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], name)
        self.assertEqual(Budget.objects.count(), 1)

        self.assertEqual(BudgetCategory.objects.filter(name__in=["food", "transport"]).count(), 2)
        self.assertEqual(Budget.objects.get(name=name).records.count(), 2)

    def test_not_creating_category_duplicates(self):
        self.authorize(self.batman)
        name = "Batman's category budget"

        records_food_category = [
            {"amount": "25.05", "category": {"name": "food"}},
            {"amount": "-20.12", "category": {"name": "food"}},
        ]
        data = {"name": name, "owners": [self.batman.id], "records": records_food_category}
        response = self.client.post(
            reverse("budget-list"),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], name)
        self.assertEqual(Budget.objects.count(), 1)

        self.assertEqual(BudgetCategory.objects.filter(name="food").count(), 1)
        self.assertEqual(Budget.objects.get(name=name).records.count(), 2)


class BudgetUpdateTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.home_budget = BudgetFactory.create(name="home", owners=[self.batman])

    def test_only_owner_can_edit(self):
        self.authorize(self.star_lord)
        new_name = "new budget name"
        data = {"name": new_name}
        response = self.client.patch(
            reverse("budget-detail", args=(self.home_budget.id,)),
            data=json.dumps(data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.home_budget.refresh_from_db()
        self.assertEqual(self.home_budget.name, "home")

    def test_can_edit_name(self):
        self.authorize(self.batman)
        new_name = "new budget name"
        data = {"name": new_name}
        response = self.client.patch(
            reverse("budget-detail", args=(self.home_budget.id,)),
            data=json.dumps(data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.home_budget.refresh_from_db()
        self.assertEqual(self.home_budget.name, new_name)

    def test_can_add_another_owner(self):
        self.authorize(self.batman)
        data = {"owners": [self.batman.id, self.star_lord.id]}
        response = self.client.patch(
            reverse("budget-detail", args=(self.home_budget.id,)),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.home_budget.refresh_from_db()
        self.assertEqual(set(self.home_budget.owners.values_list("id", flat=True)), {self.batman.id, self.star_lord.id})


class BudgetRecordListTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.home_budget = BudgetFactory.create(name="home", owners=[self.batman, self.star_lord])
        self.home_incomes = IncomeBudgetFactory.create_batch(2, budget=self.home_budget, category=self.work_category)
        self.home_expenses = ExpenseBudgetFactory.create_batch(
            2, budget=self.home_budget, category=self.furniture_category
        )

        self.business_budget = BudgetFactory.create(name="business", owners=[self.batman])
        self.business_incomes = IncomeBudgetFactory.create_batch(
            2, budget=self.business_budget, category=self.work_category
        )
        self.business_expenses = ExpenseBudgetFactory.create_batch(
            2, budget=self.business_budget, category=self.food_category
        )

    def test_unauthorized_cant_access(self):
        response = self.client.get(reverse("budgetrecord-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_simple_list_all_users_records(self):
        expected_records = [*self.home_incomes, *self.home_expenses, *self.business_expenses, *self.business_incomes]
        self.authorize(self.batman)
        response = self.client.get(reverse("budgetrecord-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), len(expected_records))
        response_ids = [record["id"] for record in response.data]
        expected_ids = [record.id for record in expected_records]
        self.assertEqual(set(response_ids), set(expected_ids))

    def test_list_by_categories(self):
        expected_records = [*self.business_expenses, *self.home_expenses]
        self.authorize(self.batman)
        response = self.client.get(
            reverse("budgetrecord-list"), {"category": [self.food_category.id, self.furniture_category.id]}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_ids = [record.id for record in expected_records]
        response_ids = [record["id"] for record in response.data]
        self.assertEqual(len(response.data), len(expected_ids))
        self.assertEqual(set(response_ids), set(expected_ids))
