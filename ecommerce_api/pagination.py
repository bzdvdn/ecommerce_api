import graphene
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def paginate(model_type):

    structure = {
        "total": graphene.Int(),
        "size": graphene.Int(),
        "current": graphene.Int(),
        "has_next": graphene.Boolean(),
        "has_prev": graphene.Boolean(),
        "results": graphene.List(model_type),
    }

    return type(f"{model_type}Paginated", (graphene.ObjectType,), structure)


def resolve_paginated(query_data, info, page, page_size):
    def get_paginated_data(qs, paginated_type, page, page_size=None):
        if not page_size:
            page_size = settings.GRAPHENE.get("PAGE_SIZE", 10)

        try:
            qs.exists()
        except:
            raise Exception(qs)

        p = Paginator(qs, page_size)

        try:
            page_obj = p.page(page)
        except PageNotAnInteger:
            page_obj = p.page(1)
        except EmptyPage:
            page_obj = p.page(p.num_pages)

        result = paginated_type.graphene_type(
            total=p.num_pages,
            size=qs.count(),
            current=page_obj.number,
            has_next=page_obj.has_next(),
            has_prev=page_obj.has_previous(),
            results=page_obj.object_list,
        )

        return result

    return get_paginated_data(query_data, info.return_type, page, page_size)
