from datetime import datetime
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from ecommerce_api.auth import TokenManager

from ..models import ImageUpload, UserProfile, UserAddress


User = get_user_model()


def create_user(email: str, password: str, **kwargs) -> User:
    user = User.objects.create_user(email, password, **kwargs)
    return user


def authenticate_user(email: str, password: str) -> tuple:
    user = authenticate(username=email, password=password)

    if not user:
        raise Exception("invalid credentials")

    user.last_login = datetime.now()
    user.save()

    access = TokenManager.get_access({"user_id": user.id})
    refresh = TokenManager.get_refresh({"user_id": user.id})
    return user, access, refresh


def get_access_token_from_refresh(refresh: str) -> str:
    token = TokenManager.decode_token(refresh)

    if not token or token["type"] != "refresh":
        raise Exception("Invalid token or has expired")

    access = TokenManager.get_access({"user_id": token["user_id"]})
    return access


def create_user_profile(user_id: int, profile_data: dict, **kwargs) -> UserProfile:
    user_profile = UserProfile.objects.create(user_id=user_id, **profile_data, **kwargs)
    return user_profile


def update_user_profile(user: User, profile_data: dict, **kwargs) -> UserProfile:
    try:
        user_profile = user.user_profile
    except Exception:
        raise Exception("You don't have a profile to update")

    UserProfile.objects.select_for_update().filter(user_profile.id).update(
        **profile_data, **kwargs
    )
    return UserProfile.objects.get(id=user_profile.id)


def create_user_address(
    user: User, address_data: dict, is_default: bool
) -> UserAddress:
    try:
        user_profile_id = user.user_profile.id
    except Exception:
        raise Exception("You need a profile to create an address")

    existing_addresses = UserAddress.objects.filter(
        user_profile_id=user_profile_id, **address_data, is_default=is_default
    ).exists()
    if existing_addresses:
        raise Exception('this address exist')

    address = UserAddress.objects.create(
        user_profile_id=user_profile_id, is_default=is_default, **address_data
    )
    return address


def update_user_address(
    user: User, address_id: int, address_data: dict, is_default: bool
) -> UserAddress:
    profile_id = user.user_profile.id

    UserAddress.objects.select_for_update().filter(
        user_profile_id=profile_id, id=address_id
    ).update(is_default=is_default, **address_data)

    if is_default:
        UserAddress.objects.filter(user_profile_id=profile_id).exclude(
            id=address_id
        ).update(is_default=False)
    return UserAddress.objects.get(id=address_id)


def delete_user_address(profile_id: id, address_id: int):
    UserAddress.objects.filter(
        user_profile_id=profile_id, id=address_id
    ).delete()

