from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Metting(models.Model):
    mettingName = models.CharField(max_length=100, verbose_name="会议名称", null=True, blank=True)
    result = models.CharField(max_length=5000, verbose_name="结果集", null=True, blank=True,)

class User(AbstractUser):
    USER_GENDER_CHOICES = (
        (0, '女'),
        (1, '男'),
    )

    sex = models.SmallIntegerField(choices=USER_GENDER_CHOICES, default=1, verbose_name="性别")
    avatar = models.CharField(max_length=50, default="", null=True, blank=True, verbose_name="头像")
    openid = models.CharField(max_length=64, db_index=True, verbose_name='openid')
    metting = models.ManyToManyField(Metting, through='UserMetting')
    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class UserMetting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    metting = models.ForeignKey(Metting, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_metting_relatinship'
