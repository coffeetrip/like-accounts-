from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="followings")
    # User에 User를 다대다로 연결시켜야한다.
    # 자기자신 : AUTH_USER_MODEL = 'auth.User'
    # class는 자기자신을 불러올 수 없다.
    # settings에서 'accounts.User'변수이름 바꾸기
