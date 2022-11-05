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
    owners = models.ManyToManyField(User, related_name="budgets")

    class Meta:
        verbose_name = _("budget")
        verbose_name_plural = _("budgets")


class BudgetRecord(TimestampModel):
    amount = models.DecimalField(verbose_name="amount", default=0, decimal_places=2, max_digits=6)

    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, null=True, related_name="records")
    category = models.ForeignKey(BudgetCategory, null=True, on_delete=models.PROTECT, related_name="records")

    class Meta:
        verbose_name = _("budget record")
        verbose_name_plural = _("budget records")

    def __str__(self):
        return f"+{self.amount}"
