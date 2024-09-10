from django.db import models
from PIL import Image

# Create your models here.
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
            
            # Defina o tamanho desejado
            output_size = (340, 300)
            img = img.resize(output_size)
            
            # Salve a imagem redimensionada
            img.save(self.image.path)

    def __str__(self):
        return self.name