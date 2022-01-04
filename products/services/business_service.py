from django.contrib.auth import get_user_model

from ..models import Business

User = get_user_model()


def create_business(name: str, user_id: int) -> Business:
    business = Business.objects.create(name=name, user_id=user_id)
    return business


def update_business(name: str, user: User) -> Business:
    try:
        business = user.user_business
        business.name = name
        business.save()
        return business
    except User.user_business.RelatedObjectDoesNotExist:
        raise Exception('User has no user_business')


def delete_business(user_id: int):
    Business.objects.filter(user_id=user_id).delete()
