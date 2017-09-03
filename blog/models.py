from django.db import models
import re
from django.forms import ValidationError
from django.conf import settings
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import Thumbnail

# Create your models here.


def lnglat_validator(value):
    if not re.match(r'^([+-]?\d+\.?\d*),([+-]?\d+\.?\d*)$', value):
        raise ValidationError('Invalid LngLat Type')


class Post(models.Model):
    STATUS_CHOICES=(
        ("d", "Draft"),
        ("p", "Published"),
        ("w", "Withdrawn"),
    )

    #   author=models.CharField(max_length=20)
    user=models.ForeignKey(settings.AUTH_USER_MODEL)
    title=models.CharField(max_length=100, verbose_name='제목',
                           help_text="포스팅 제목을 입력해주세요. 최대 100자 내외.")
    content=models.TextField(verbose_name="내용")
    photo=models.ImageField(blank=True, upload_to="blog/post/%Y/%m")
    photo_thumbnail=ImageSpecField(source="photo",
                                   processors=[Thumbnail(300, 300)],
                                   format="JPEG",
                                   options={"quality":60})

    tags=models.CharField(max_length=100, blank=True)
    tag_set=models.ManyToManyField('Tag', blank=True)

    lnglat=models.CharField(max_length=50, blank=True,
                            validators=[lnglat_validator],
                            help_text="경도/위도 format으로 입력.")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=1, choices=STATUS_CHOICES)

    class Meta:
        ordering=['-id']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:detail", args=[self.id])

class Comment(models.Model):
    post=models.ForeignKey(Post)
    author=models.CharField(max_length=20)
    message=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


class Tag(models.Model):
    name=models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.name