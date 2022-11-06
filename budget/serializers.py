from django.contrib.auth.models import User
from rest_framework import serializers

from budget.models import Budget, BudgetCategory, BudgetRecord


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class BudgetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetCategory
        fields = "__all__"


class BudgetRecordSerializer(serializers.ModelSerializer):
    category = BudgetCategorySerializer(required=False, allow_null=True)

    class Meta:
        model = BudgetRecord
        fields = "__all__"


class BudgetRecordCreateSerializer(serializers.ModelSerializer):
    category = BudgetCategorySerializer(required=False, allow_null=True)
    budget = serializers.PrimaryKeyRelatedField(queryset=Budget.objects.all(), required=True)

    class Meta:
        model = BudgetRecord
        fields = "__all__"


class BudgetSerializer(serializers.ModelSerializer):
    records = BudgetRecordSerializer(many=True, required=False, allow_null=True)
    records_count = serializers.ReadOnlyField()

    class Meta:
        model = Budget
        fields = ("id", "name", "owners", "records_count", "records", "created_at", "updated_at")

    def create(self, validated_data):
        records = validated_data.pop("records", None)
        budget = super().create(validated_data)
        if records:
            for record in records:
                budget_category = None
                if category := record.pop("category", None):
                    budget_category = BudgetCategory.objects.get_or_create(**category)[0]

                BudgetRecord.objects.create(budget=budget, category=budget_category, **record)

        return budget
