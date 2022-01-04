from typing import Optional
from django.db.models import QuerySet, Q
from django.contrib.auth import get_user_model
from ecommerce_api.permissions import get_query

from ..models import Product, ProductImage, ProductComment, Wish, Cart, RequestCart


User = get_user_model()


def get_products(**search_kwargs) -> QuerySet:
    qs = Product.objects.select_related("business", "category").prefetch_related(
        "product_images",
        "product_comments",
        "product_wishes",
        "product_carts",
        "product_requests",
    )

    if search_kwargs.get('search'):
        search = search_kwargs['search']
        search_fields = (
            "name",
            "description",
            "category__name",
        )
        search_data = get_query(search, search_fields)
        qs = qs.filter(search_data)

    if search_kwargs.get('min_price'):
        qs = qs.filter(price__gte=search_kwargs['min_price']).distinct()

    if search_kwargs.get('max_price'):
        qs = qs.filter(price__lte=search_kwargs['max_price']).distinct()

    if search_kwargs.get('category'):
        category = search_kwargs['category']
        qs = qs.filter(
            Q(category__name__icontaince=category) | Q(category__name__iexact=category)
        ).distinct()

    if search_kwargs.get('business'):
        business = search_kwargs['business']
        qs = qs.filter(
            Q(business__name__icontaince=business) | Q(business__name__iexact=business)
        ).distinct()

    if search_kwargs.get('sort_by'):
        sort_field = search_kwargs['sort_by']
        is_asc = search_kwargs.get('is_asc', False)
        sort_by = f'-{sort_field}' if not is_asc else sort_field
        qs = qs.order_by(sort_by)

    return qs


def get_product(self, id_: int) -> Product:
    qs = Product.objects.select_related("business", "category").prefetch_related(
        "product_images",
        "product_comments",
        "product_wishes",
        "product_carts",
        "product_requests",
    )
    product = qs.get(pk=id_)
    return product


def create_product(
    product_data: dict, user: User, images: list, total_count: int
) -> Product:
    try:
        business_id = user.user_business.id
    except User.user_business.RelatedObjectDoesNotExist:
        raise Exception('User has no user_business')

    product, created = Product.objects.get_or_create(
        business_id=business_id,
        category_id=product_data['category_id'],
        name=product_data['name'],
        defaults={
            'price': product_data['price'],
            'total_count': total_count,
            'total_availeble': total_count,
            'description': product_data['description'],
        },
    )
    if not created:
        raise Exception(
            f'product with name - {product_data["name"]} exists for this business and category'
        )

    product_images = [ProductImage(prodct_id=product.id, **image) for image in images]
    ProductImage.objects.bulk_create(product_images, batch_size=100)

    return product


def update_product(
    product_id: int,
    product_data: dict,
    user: User,
    total_availeble: int,
    images: Optional[list] = None,
):
    try:
        business_id = user.user_business.id
    except User.user_business.RelatedObjectDoesNotExist:
        raise Exception('User has no user_business')

    if product_data.get('name'):
        exists = (
            Product.objects.filter(business_id=business_id, name=product_data['name'])
            .exclude(id=product_id)
            .exists()
        )
        if exists:
            raise Exception(
                f'product with name - {product_data["name"]} exists for this business and category with another product_id'
            )
    product_data['total_availeble'] = total_availeble
    db_product = Product.objects.filter(product_id=product_id).first()
    if not db_product:
        raise Exception(f'product does not exist with this product_id - {product_id}')
    for attr, value in product_data.items():
        setattr(db_product, attr, value)

    db_product.save()
    return db_product


def update_product_image(image_id: int, image_data: dict, user: User) -> ProductImage:
    try:
        business_id = user.user_business.id
    except User.user_business.RelatedObjectDoesNotExist:
        raise Exception('User has no user_business')

    image = ProductImage.objects.filter(
        product__business_id=business_id, id=image_id
    ).first()
    if not image:
        raise Exception('you dont have access to this product')

    for attr, value in image_data.items():
        setattr(image, attr, value)

    image.save()

    if image_data.get('is_cover'):
        ProductImage.objects.filter(product__business_id=business_id).exclude(
            id=image_id
        ).update(is_cover=False)

    return image


def delete_product(product_id: int):
    Product.objects.filter(pk=product_id).delete()


def create_product_comment(
    product_id: int, comment: str, user: User, rate: Optional[int] = 3
) -> ProductComment:

    try:
        business_id = user.user_business.id
    except User.user_business.RelatedObjectDoesNotExist:
        business_id = None

    if business_id:
        own_product = Product.objects.filter(
            product_id=product_id, business_id=business_id
        )
        if own_product:
            raise Exception('you cannot comment your products')

    product_comment, created = ProductComment.objects.get_or_create(
        user_id=user.id,
        product_id=product_id,
        defaults={'comment': comment, 'rate': rate},
    )
    if not created:
        raise Exception(
            'you cannot comment this product, coz u comment this product as well'
        )
    return product_comment


def handle_wish_list(user: User, product_id: int, is_check: bool = False) -> bool:
    product = Product.objects.filter(id=product_id).first()
    if not product:
        raise Exception(f"product with product_id: {product_id} does not exist")
    try:
        user_wish = user.user_wish
    except User.user_wish.RelatedObjectDoesNotExist:
        user_wish = Wish.objects.create(user_id=user.id)

    has_product = user_wish.products.filter(id=product_id).exists()

    if has_product:
        if is_check:
            return True
        user_wish.products.remove(product)
    else:
        if is_check:
            return False
        user_wish.products.add(product)
    return True


def create_cart(product_id: int, user: User, quantity: int = 1) -> Cart:
    cart, created = Cart.objects.get_or_crate(
        product_id=product_id, user_id=user, defaults={'quantity': quantity}
    )
    if not created:
        raise Exception(f'this product_id {product_id} in cart')
    return cart


def update_cart(cart_id: int, user: User, quantity: int = 1) -> Cart:
    cart = Cart.objects.filter(pk=cart_id, user_id=user.id).first()

    if not cart:
        raise Exception(f'invalid cart_id - {cart_id}')

    cart.quantity = quantity
    cart.save()
    return cart


def delete_cart(cart_id: int):
    Cart.objects.filter(pk=cart_id).delete()


def complete_payment(user: User):
    user_carts = Cart.objects.filter(user_id=user.id)

    RequestCart.objects.bulk_create(
        [
            RequestCart(
                user_id=user.id,
                business_id=cart_item.product.business.id,
                product_id=cart_item.product.id,
                quantity=cart_item.quantity,
                price=cart_item.quantity * cart_item.product.price,
            )
            for cart_item in user_carts
        ]
    )

    user_carts.delete()

    return True
