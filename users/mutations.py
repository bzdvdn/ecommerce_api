import graphene
from ecommerce_api.permissions import is_authenticated
from graphene_file_upload.scalars import Upload

from .types import (
    UserType,
    ImageUploadType,
    UserProfileType,
    UserAddressType,
    UserProfileInput,
    AddressInput,
)
from .services import user_service, image_service


class RegisterUser(graphene.Mutation):
    status = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)

    def mutate(self, info, email, password, **kwargs):
        user_service.create_user(email, password, **kwargs)

        return RegisterUser(status=True, message="User created successfully")


class LoginUser(graphene.Mutation):
    access = graphene.String()
    refresh = graphene.String()
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, email, password):
        user, access, refresh = user_service.authenticate_user(email, password)
        return LoginUser(access=access, refresh=refresh, user=user)


class GetAccess(graphene.Mutation):
    access = graphene.String()

    class Arguments:
        refresh = graphene.String(required=True)

    def mutate(self, info, refresh):
        access = user_service.get_access_token_from_refresh(refresh)

        return GetAccess(access=access)


class ImageUploadMain(graphene.Mutation):
    image = graphene.Field(ImageUploadType)

    class Arguments:
        image = Upload(required=True)

    def mutate(self, info, image):
        image = image_service.create_image_upload(image)

        return ImageUploadMain(image=image)


class CreateUserProfile(graphene.Mutation):
    user_profile = graphene.Field(UserProfileType)

    class Arguments:
        profile_data = UserProfileInput()
        dob = graphene.Date(required=True)
        phone = graphene.Int(required=True)

    @is_authenticated
    def mutate(self, info, profile_data, **kwargs):
        user_profile = user_service.create_user_profile(
            info.context.user.id, profile_data, **kwargs
        )

        return CreateUserProfile(user_profile=user_profile)


class UpdateUserProfile(graphene.Mutation):
    user_profile = graphene.Field(UserProfileType)

    class Arguments:
        profile_data = UserProfileInput()
        dob = graphene.Date()
        phone = graphene.Int()

    @is_authenticated
    def mutate(self, info, profile_data, **kwargs):
        user_profile = user_service.update_user_profile(
            info.context.user, profile_data, **kwargs
        )

        return UpdateUserProfile(user_profile=user_profile)


class CreateUserAddress(graphene.Mutation):
    address = graphene.Field(UserAddressType)

    class Arguments:
        address_data = AddressInput(required=True)
        is_default = graphene.Boolean()

    @is_authenticated
    def mutate(self, info, address_data, is_default=False):
        address = user_service.create_user_address(
            info.context.user, address_data, is_default
        )

        return CreateUserAddress(address=address)


class UpdateUserAddress(graphene.Mutation):
    address = graphene.Field(UserAddressType)

    class Arguments:
        address_data = AddressInput()
        is_default = graphene.Boolean()
        address_id = graphene.ID(required=True)

    @is_authenticated
    def mutate(self, info, address_data, address_id, is_default=False):
        address = user_service.update_user_address(
            info.context.user, address_id, address_data, is_default
        )

        return UpdateUserAddress(address=address)


class DeleteUserAddress(graphene.Mutation):
    status = graphene.Boolean()

    class Arguments:
        address_id = graphene.ID(required=True)

    @is_authenticated
    def mutate(self, info, profile_id, address_id):
        user_service.delete_user_address(profile_id, address_id)

        return DeleteUserAddress(status=True)

