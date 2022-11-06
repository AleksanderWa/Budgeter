from django.contrib.auth.models import User
from django.db.models import Count, Q
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from budget.models import Budget, BudgetRecord
from budget.serializers import BudgetRecordCreateSerializer, BudgetRecordSerializer, BudgetSerializer, UserSerializer
from budget.utils import MultiSerializerViewSetMixin


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class RowCountMixin:
    @staticmethod
    def _annotate_items_count(queryset, field):
        return queryset.annotate(items_count=Count(field))


class BudgetRecordViewSet(MultiSerializerViewSetMixin, viewsets.ModelViewSet):
    queryset = BudgetRecord.objects.all().select_related("budget").prefetch_related("category")
    serializer_class = BudgetRecordSerializer
    serializer_action_classes = {
        "create": BudgetRecordCreateSerializer,
    }
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset().filter(budget__owners__in=(user,))
        filters = Q()
        budget = self.request.query_params.get("budget")
        categories = self.request.query_params.getlist("category")
        if categories:
            filters |= Q(**{"category__in": [int(category) for category in categories]})
        if budget:
            filters |= Q(**{"budget": budget})
        return queryset.filter(filters)


class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all().prefetch_related("records__category", "owners")
    serializer_class = BudgetSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset().filter(owners__in=(user,))
        filters = Q()
        categories = self.request.query_params.getlist("category")
        if categories:
            filters |= Q(**{"records__category__in": [int(category) for category in categories]})
        return queryset.filter(filters).distinct()

    @staticmethod
    def _annotate_records_count(queryset):
        return queryset.annotate(records_count=Count("records"))
