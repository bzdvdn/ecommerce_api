import graphene
from ecommerce_api.permissions import paginate, is_authenticated

from .models import User, ImageUpload
from .types import (
    UserType,
    ImageUploadType,
)
from .mutations import (
    RegisterUser,
    ImageUploadType,
    LoginUser,
    GetAccess,
    ImageUploadMain,
    CreateUserProfile,
    UpdateUserProfile,
    CreateUserAddress,
    UpdateUserAddress,
    DeleteUserAddress,
)


class Query(graphene.ObjectType):
    users = graphene.Field(
        paginate(UserType), page=graphene.Int(), page_size=graphene.Int()
    )
    image_uploads = graphene.Field(
        paginate(ImageUploadType), page=graphene.Int(), page_size=graphene.Int()
    )
    me = graphene.Field(UserType)

    def resolve_users(self, info, **kwargs):
        return User.objects.filter(**kwargs)

    def resolve_image_uploads(self, info, **kwargs):
        return ImageUpload.objects.filter(**kwargs)

    @is_authenticated
    def resolve_me(self, info):
        return info.context.user


class Mutation(graphene.ObjectType):
    register_user = RegisterUser.Field()
    login_user = LoginUser.Field()
    get_access = GetAccess.Field()
    image_upload = ImageUploadMain.Field()
    create_user_profile = CreateUserProfile.Field()
    update_user_profile = UpdateUserProfile.Field()
    create_user_address = CreateUserAddress.Field()
    update_user_address = UpdateUserAddress.Field()
    delete_user_address = DeleteUserAddress.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
