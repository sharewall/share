import uuid
from django.db import models
from django.contrib.auth.models import User

class CabinetWebmasterModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="related user", related_name="cabinet_webmaster")
    db_table = 'CabinetWebmasterModel'
    def __str__(self):
        return str("user.name: %s" % self.user.username + " , user.email: %s" % self.user.email)
