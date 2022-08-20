from core.models import User, Profile
from django.db.models.signals import post_save
from django.dispatch import receiver


# A post_save signal received when a User instance is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, id_user=instance.id)
