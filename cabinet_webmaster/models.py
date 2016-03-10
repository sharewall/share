import uuid
from django.db import models
from django.contrib.auth.models import User

class CabinetWebmasterModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="related user", related_name="cabinet_webmaster")
    wmr = models.CharField("wmr", max_length=100, null=True, blank=True, default="")
    mobile_phone = models.CharField("mobile phone", max_length=200, blank=True, default="")
    skype = models.CharField("skype", max_length=200, blank=True, default="")
    money = models.FloatField("money in rub", default=0.0)
    db_table = 'CabinetWebmasterModel'

    def __str__(self):
        return str("user.name: %s" % self.user.username + " , user.email: %s" % self.user.email)
