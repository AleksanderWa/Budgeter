from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimestampModel(models.Model):
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("modified at"), auto_now=True)

    class Meta:
        abstract = True


class BudgetCategory(TimestampModel):
    name = models.CharField(verbose_name="name", max_length=30)

    class Meta:
        verbose_name = _("budget category")
        verbose_name_plural = _("budget categories")


class Budget(TimestampModel):
    name = models.CharField(verbose_name="name", max_length=30)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("budget")
        verbose_name_plural = _("budgets")


class BudgetRecord(TimestampModel):
    income = models.DecimalField(verbose_name="income", default=0, decimal_places=2, max_digits=6)
    expense = models.DecimalField(verbose_name="expense", default=0, decimal_places=2, max_digits=6)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    category = models.ForeignKey(BudgetCategory, null=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = _("budget record")
        verbose_name_plural = _("budget records")

    def __str__(self):
        return f"+{self.income} -{self.expense}"
