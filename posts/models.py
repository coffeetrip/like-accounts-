from django.db import models
from django.conf import settings
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField


class HashTag(models.Model):
    content = models.CharField(max_length=100)


class Post(models.Model):
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    image = ProcessedImageField(
        processors=[ResizeToFill(300, 300)],
        format='JPEG',
        options={'quality': 90},
        upload_to='media'
    )

    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="like_posts")
    create_at = models.DateTimeField(auto_now_add=True)
    hashtags = models.ManyToManyField(HashTag, related_name="taged_post")
# post안에 hashtag가 있다.(사실위치상관 x)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    comment_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                     on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
