from django.db import models

# Create your models here.
class User(AbstractUser):
    USER_GENDER_CHOICES = (
        (0, '女'),
        (1, '男'),
    )

    sex = models.SmallIntegerField(choices=USER_GENDER_CHOICES, default=1, verbose_name="性别")
    avatar = models.CharField(max_length=50, default="", null=True, blank=True, verbose_name="头像")
    openid = models.CharField(max_length=64, db_index=True, verbose_name='openid')

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name