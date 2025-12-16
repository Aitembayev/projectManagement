from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to="products/")
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title


class CartItem(models.Model):
    session_key = models.CharField(max_length=40, db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["session_key", "product"], name="uniq_cart_session_product")
        ]

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"

    def get_total_price(self):
        return self.product.price * self.quantity
