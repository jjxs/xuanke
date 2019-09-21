from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
# Create your models here.

class Metting(models.Model):
    mettingName = models.CharField(max_length=100, verbose_name="会议名称", null=True, blank=True)
    config = models.CharField(default="5,5,5,5,5", max_length=200, verbose_name="配置座位", help_text="例：5,5,5,5 第一排5个座位，第二排5个座位......")
    result = models.CharField(editable=False, max_length=5000, verbose_name="结果集", null=True, blank=True,)
    time = models.DateTimeField(null=True, blank=True, verbose_name="会议开始时间")
    # row = models.IntegerField(blank=True, null=True, verbose_name="横座位数量", default=10)
    # col = models.IntegerField(blank=True, null=True, verbose_name="纵座位数量", default=10)

    def __str__(self):
        return self.mettingName
    class Meta:
        verbose_name = '会议'
        verbose_name_plural = verbose_name

class User(AbstractUser):
    USER_GENDER_CHOICES = (
        (0, '女'),
        (1, '男'),
    )

    sex = models.SmallIntegerField(choices=USER_GENDER_CHOICES, default=1, verbose_name="性别")
    avatar = models.CharField(max_length=50, default="", null=True, blank=True, verbose_name="头像")
    openid = models.CharField(max_length=64, db_index=True, verbose_name='openid')
    metting = models.ManyToManyField(Metting, through='UserMetting')

    def __str__(self):
        return self.username
    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class UserMetting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    metting = models.ForeignKey(Metting, on_delete=models.CASCADE, verbose_name="会议")
    seat_num = models.IntegerField(verbose_name="座位号")
    class Meta:
        db_table = 'user_metting_relatinship'
        verbose_name = '用户/会议'
        verbose_name_plural = verbose_name
