from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

# this will run everytime a user gets created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# this will save profile whenever the user object gets saved
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


# this is to create the user profile once he registers, instead going to backend and creating manually in the admins page
# there is sender=User and signal=post_save, this says that when a user is saved, send this signal, and this signal is going to be received by the receiver which is create_profile func, and this func takes all the arguments passed by the post_save signal passed to it, and check if the user was created then create the profile object with the user equals to the object of the user that was created
# after this go to apps.py and enter configuration