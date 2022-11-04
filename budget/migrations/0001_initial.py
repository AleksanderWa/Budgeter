# Generated by Django 4.0 on 2022-11-04 21:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='modified at')),
                ('name', models.CharField(max_length=30, verbose_name='name')),
                ('owner', models.ManyToManyField(related_name='budgets', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'budget',
                'verbose_name_plural': 'budgets',
            },
        ),
        migrations.CreateModel(
            name='BudgetCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='modified at')),
                ('name', models.CharField(max_length=30, verbose_name='name')),
            ],
            options={
                'verbose_name': 'budget category',
                'verbose_name_plural': 'budget categories',
            },
        ),
        migrations.CreateModel(
            name='BudgetRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='modified at')),
                ('income', models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='income')),
                ('expense', models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='expense')),
                ('budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budget.budget')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='budget.budgetcategory')),
            ],
            options={
                'verbose_name': 'budget record',
                'verbose_name_plural': 'budget records',
            },
        ),
    ]
