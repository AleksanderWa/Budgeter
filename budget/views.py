from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from budget.models import Budget
from budget.serializers import BudgetSerializer, UserSerializer


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        filters = Q()
        categories = self.request.query_params.getlist("category")
        if categories:
            filters |= Q(**{"records__category__in": [int(category) for category in categories]})
        return user.budgets.filter(filters).distinct()
