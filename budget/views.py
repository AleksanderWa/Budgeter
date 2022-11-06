from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from budget.models import Budget, BudgetRecord
from budget.serializers import BudgetRecordSerializer, BudgetSerializer, UserSerializer


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class BudgetRecordViewSet(viewsets.ModelViewSet):
    queryset = BudgetRecord.objects.all().prefetch_related("budget__owners")
    serializer_class = BudgetRecordSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset().filter(budget_owners__in=(user,))
        # filters = Q()
        # categories = self.request.query_params.getlist("category")
        # if categories:
        #     filters |= Q(**{"records__category__in": [int(category) for category in categories]})
        return queryset


class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all().prefetch_related("records")
    serializer_class = BudgetSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        filters = Q()
        categories = self.request.query_params.getlist("category")
        if categories:
            filters |= Q(**{"records__category__in": [int(category) for category in categories]})
        return user.budgets.filter(filters).distinct()

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data.copy())
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
