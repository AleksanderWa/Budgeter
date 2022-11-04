from django.contrib.auth.models import User
from rest_framework import serializers

from budget.models import Budget, BudgetRecord


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


class BudgetRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetRecord
        fields = "__all__"


class BudgetSerializer(serializers.ModelSerializer):
    records = BudgetRecordSerializer(many=True)

    class Meta:
        model = Budget
        fields = "__all__"
