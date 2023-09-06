from django.db import models
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=30,unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.email

    class Meta:
        app_label = 'api'  # Add this line to specify the app label

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    barcode = models.CharField(max_length=255)
    product_image = models.FileField(upload_to='product/docs')
    brand = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    def __str__(self):
        return self.product_name

    def __str__(self):
        return self.name



class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review of {self.product.name} by {self.user.username}"
