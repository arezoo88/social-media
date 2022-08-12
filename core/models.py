from django.db import models
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField
from mapbox_location_field.models import LocationField

User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profile_image = CloudinaryField('image')
    location = models.CharField(max_length=100, blank=False)

    def __str__(self) -> str:
        return self.user.username
