from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from PIL import Image

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=150, blank=True, null=True) 
    last_name = models.CharField(max_length=150, blank=True, null=True)   
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    street_number = models.CharField(max_length=10, blank=True, null=True)
    cpf = models.CharField(max_length=11, unique=True, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.profile_picture:
            img = Image.open(self.profile_picture.path)
            output_size = (150, 150)
            img.thumbnail(output_size)
            img.save(self.profile_picture.path)

    def __str__(self):
        return self.username

User = get_user_model()

class Game(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='games_images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            output_size = (340, 300)
            img = img.resize(output_size)
            img.save(self.image.path)

    def __str__(self):
        return self.name

class Comment(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.game.name}'