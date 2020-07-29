from django.db import models
from django.contrib.auth.models import User
# Pillow package
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # upload profile pic to profile_pics folder(media folder)
    image = models.ImageField(default='default.svg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username}'
    # overwrite func to resize image
    def save(self):
        # save the large image
        super().save()
        # open the image of the current instance
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
