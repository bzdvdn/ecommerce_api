import graphene
from ecommerce_api.pagination import paginate

from .types import CategoryType, ProductType
from .services import category_service, product_service
from .mutations import (
    CreateBusiness,
    UpdateBusiness,
    DeleteBusiness,
    CreateProduct,
    UpdateProduct,
    DeleteProduct,
    UpdateProductImage,
    CreateProductComment,
    HandleWishList,
    CreateCart,
    UpdateCart,
    DeleteCart,
    CompletePayment,
)


class Query(graphene.ObjectType):
    categories = graphene.List(CategoryType, name=graphene.String())
    products = graphene.Field(
        paginate(ProductType),
        search=graphene.String(),
        min_price=graphene.Float(),
        max_price=graphene.Float(),
        category=graphene.String(),
        business=graphene.String(),
        sort_by=graphene.String(),
        is_asc=graphene.Boolean(),
        page=graphene.Int(),
        page_size=graphene.Int(),
    )
    product = graphene.Field(ProductType, id=graphene.ID(required=True))

    def resolve_categories(self, info, name):
        return category_service.get_categories(name)

    def resolve_products(self, info, **kwargs):
        return product_service.get_products(**kwargs)

    def resolve_product(self, info, id):
        return product_service.get_product(id)


class Mutation(graphene.ObjectType):
    create_business = CreateBusiness.Field()
    update_business = UpdateBusiness.Field()
    delete_business = DeleteBusiness.Field()
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
    delete_product = DeleteProduct.Field()
    update_product_image = UpdateProductImage.Field()
    create_product_comment = CreateProductComment.Field()
    handle_wish_list = HandleWishList.Field()
    create_cart = CreateCart.Field()
    update_cart = UpdateCart.Field()
    delete_cart = DeleteCart.Field()
    complete_payment = CompletePayment.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
