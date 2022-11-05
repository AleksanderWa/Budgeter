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
    class Meta:
        model = BudgetRecord
        fields = "__all__"


class BudgetSerializer(serializers.ModelSerializer):
    records = BudgetRecordSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = Budget
        fields = ("id", "name", "owners", "records", "created_at", "updated_at")

    def create(self, validated_data):
        records = validated_data.pop("records", None)
        budget = super().create(validated_data)
        if records:
            for record in records:
                BudgetRecord.objects.create(budget=budget, **record)
        return budget
