import graphene

from ecommerce_api.permissions import is_authenticated

from .types import (
    BusinessType,
    ProductInput,
    ProductType,
    ProductImageInput,
    ProductCommentType,
    CartType,
    ProductImageType,
)
from .services import business_service, product_service


class CreateBusiness(graphene.Mutation):
    business = graphene.Field(BusinessType)

    class Argumens:
        name = graphene.String(required=True)

    @is_authenticated
    def mutate(self, info, name):
        business = business_service.create_business(name, info.context.user.id)
        return CreateBusiness(business=business)


class UpdateBusiness(graphene.Mutation):
    business = graphene.Field(BusinessType)

    class Argumens:
        name = graphene.String(required=True)

    @is_authenticated
    def mutate(self, info, name):
        business = business_service.update_business(name, info.context.user)
        return UpdateBusiness(business=business)


class DeleteBusiness(graphene.Mutation):
    status = graphene.Boolean()

    @is_authenticated
    def mutate(self, info, **kwargs):
        business_service.delete_business(info.context.user.id)
        return DeleteBusiness(status=True)


# products


class CreateProduct(graphene.Mutation):
    product = graphene.Field(ProductType)

    class Arguments:
        product_data = ProductInput(required=True)
        total_count = graphene.Int(required=True)
        images = graphene.List(ProductImageInput)

    @is_authenticated
    def mutate(self, info, product_data, total_count, images):
        product = product_service.create_product(
            product_data, info.context.user, images, total_count
        )
        return CreateProduct(product=product)


class UpdateProduct(graphene.Mutation):
    product = graphene.Field(ProductType)

    class Arguments:
        product_id = graphene.ID(required=True)
        product_data = ProductInput()
        total_availeble = graphene.Int()

    @is_authenticated
    def mutate(self, info, product_id, product_data, total_availeble):
        product = product_service.update_product(
            product_id, product_data, info.context.user, total_availeble
        )
        return UpdateProduct(product=product)


class DeleteProduct(graphene.Mutation):
    status = graphene.Boolean()

    class Arguments:
        product_id = graphene.ID(required=True)

    @is_authenticated
    def mutate(self, info, product_id):
        product_service.delete_product(product_id)
        return DeleteProduct(status=True)


class UpdateProductImage(graphene.Mutation):
    image = graphene.Field(ProductImageType)

    class Arguments:
        image_data = ProductImageInput()
        id = graphene.ID(required=True)

    @is_authenticated
    def mutate(self, info, image_data, id):
        image = product_service.update_product_image(id, image_data, info.context.user)
        return UpdateProductImage(image=image)


class CreateProductComment(graphene.Mutation):
    product_comment = graphene.Field(ProductCommentType)

    class Arguments:
        product_id = graphene.ID(required=True)
        comment = graphene.String(required=True)
        rate = graphene.Int()

    @is_authenticated
    def mutate(self, info, product_id, comment, rate):
        product_comment = product_service.create_product_comment(
            product_id, comment, info.context.user, rate
        )
        return CreateProductComment(product_comment=product_comment)


class HandleWishList(graphene.Mutation):
    status = graphene.Boolean()

    class Arguments:
        product_id = graphene.ID(required=True)
        is_check = graphene.Boolean()

    @is_authenticated
    def mutate(self, info, product_id, is_check=False):
        status = product_service.handle_wish_list(
            info.context.user, product_id, is_check
        )
        return HandleWishList(status=status)


class CreateCart(graphene.Mutation):
    cart = graphene.Field(CartType)

    class Arguments:
        product_id = graphene.ID(required=True)
        quantity = graphene.Int()

    @is_authenticated
    def mutate(self, info, product_id, quantity):
        cart = product_service.create_cart(product_id, info.context.user, quantity)
        return CreateCart(cart=cart)


class UpdateCart(graphene.Mutation):
    cart = graphene.Field(CartType)

    class Arguments:
        cart_id = graphene.ID(required=True)
        quantity = graphene.Int()

    @is_authenticated
    def mutate(self, info, cart_id, quantity):
        cart = product_service.update_cart(cart_id, info.context.user, quantity)
        return UpdateCart(cart=cart)


class DeleteCart(graphene.Mutation):
    status = graphene.Boolean()

    class Arguments:
        cart_id = graphene.ID(required=True)

    @is_authenticated
    def mutate(self, info, cart_id):
        product_service.delete_cart(cart_id)
        return DeleteCart(status=True)


class CompletePayment(graphene.Mutation):
    status = graphene.Boolean()

    @is_authenticated
    def mutate(self, info):
        status = product_service.complete_payment(info.context.user)
        return CompletePayment(status=status)
