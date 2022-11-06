import logging

from django.contrib.auth.models import User
from django.core.management import BaseCommand

from budget.factory import BudgetFactory, CategoryFactory, ExpenseBudgetFactory, IncomeBudgetFactory

logger = logging.getLogger(__name__)


class Command(
    BaseCommand,
):
    help = "Create fixtures"

    def handle(self, *args, **options):
        self.create_users()
        self.create_categories()
        self.create_budgets()
        self.create_records()

        logger.info("Fixtures successfully created!")

    def create_users(self):
        self.batman = User.objects.create(username="Batman")
        self.batman.set_password("password")
        self.batman.save()

        self.star_lord = User.objects.create(username="Star Lord")
        self.star_lord.set_password("galaxy")
        self.star_lord.save()

        logger.info("Users created!")

    def create_categories(self):
        self.work_category = CategoryFactory(name="work")
        self.food_category = CategoryFactory(name="food")
        self.transport_category = CategoryFactory(name="transport")
        self.furniture_category = CategoryFactory(name="furniture")

        logger.info("Categories created!")

    def create_budgets(self):
        self.home_budget = BudgetFactory.create(name="home", owners=[self.batman])
        self.business_budget = BudgetFactory.create(name="business", owners=[self.batman])
        self.vacation_budget = BudgetFactory.create(name="vacation", owners=[self.batman, self.star_lord])

        logger.info("Budgets created!")

    def create_records(self):
        IncomeBudgetFactory.create_batch(2, budget=self.home_budget, category=self.work_category)
        ExpenseBudgetFactory.create_batch(2, budget=self.home_budget, category=self.furniture_category)

        IncomeBudgetFactory.create_batch(2, budget=self.business_budget, category=self.work_category)
        ExpenseBudgetFactory.create_batch(2, budget=self.business_budget, category=self.food_category)

        IncomeBudgetFactory.create_batch(2, budget=self.vacation_budget, category=self.work_category)

        logger.info("Budgets created!")
