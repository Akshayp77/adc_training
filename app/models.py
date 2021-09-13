from django.db import models
from django.db.models.base import Model
from django.conf import settings
from django.db.models.deletion import DO_NOTHING
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False,**Kwargs):
    if created:
        Token.objects.create(user=instance)

class Recommend(models.Model):
    liked_by=models.ForeignKey(User,on_delete=DO_NOTHING)
    jsondata = models.JSONField(blank=True,null=True)
