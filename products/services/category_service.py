from typing import Optional
from django.db.models import QuerySet, Q

from ..models import Category


def get_categories(name: Optional[str] = None) -> QuerySet:
    qs = Category.objects.prefetch_related('product_categories')
    if name:
        qs.filter(Q(name__icontains=name) | Q(name__iexact=name)).distinct()
    return qs
