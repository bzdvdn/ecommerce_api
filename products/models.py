from django.db import models
from django.contrib.auth import get_user_model
from users.models import ImageUpload

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return f'name: {self.name}, created_at: {self.created_at.strftime("%Y-%m-%d %H:%M:%S")}'


class Business(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user_business'
    )
    name = models.CharField(max_length=255, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'name: {self.name}, created_at: {self.created_at.strftime("%Y-%m-%d %H:%M:%S")}, updated_at: {self.updated_at.strftime("%Y-%m-%d %H:%M:%S")}'


class Product(models.Model):
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, related_name='product_categories'
    )
    business = models.ForeignKey(
        'Business', on_delete=models.CASCADE, related_name='business_products'
    )
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    total_availeble = models.PositiveIntegerField()
    total_count = models.PositiveIntegerField()
    description = models.TextField()

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'name: {self.name}, category: {self.category.name}, business: {self.business.name}'


class ProductImage(models.Model):
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='product_images'
    )
    image = models.ForeignKey(
        ImageUpload, on_delete=models.CASCADE, related_name='product_image'
    )
    is_cover = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.__str__()} - {self.image}"


class ProductComment(models.Model):
    product = models.ForeignKey(
        Product, related_name="product_comments", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User, related_name="user_comments", on_delete=models.CASCADE
    )
    comment = models.TextField()
    rate = models.IntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{str(self.product)}: {self.created_at.strftime("%Y-%m-%d %H:%M:%S")}'


class Wish(models.Model):
    user = models.OneToOneField(
        User, related_name="user_wish", on_delete=models.CASCADE
    )
    products = models.ManyToManyField(Product, related_name="products_wished")
    created_at = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    product = models.ForeignKey(
        Product, related_name="product_carts", on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, related_name="user_carts", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.user.email}"

    class Meta:
        ordering = ("-created_at",)


class RequestCart(models.Model):
    user = models.ForeignKey(
        User, related_name="user_requests", on_delete=models.CASCADE
    )
    business = models.ForeignKey(
        Business, related_name="business_requests", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, related_name="product_requests", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)
