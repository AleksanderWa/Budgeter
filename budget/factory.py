import random

import factory
from faker import Faker

from budget.models import Budget, BudgetCategory, BudgetRecord

faker = Faker()


class BudgetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Budget

    name = factory.Faker("name")

    @factory.post_generation
    def records(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for budget_record in extracted:
                self.records.add(budget_record)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BudgetCategory

    name = random.choice(["Food", "Car", "Hobby", "Other"])


class IncomeBudgetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BudgetRecord

    amount = factory.LazyAttribute(lambda o: faker.pyint(min_value=2, max_value=10000, step=1))


class ExpenseBudgetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BudgetRecord

    amount = factory.LazyAttribute(lambda o: faker.pyint(min_value=-10000, max_value=-2, step=-1))
