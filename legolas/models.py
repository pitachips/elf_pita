from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone

from elf.utils import random_name_upload_to, thumbnail


## Area와 SubArea 데이터는 area_fixtures.json 으로 관리
class Area(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class SubArea(models.Model):
    name = models.CharField(max_length=20)
    parent = models.ForeignKey(Area)

    def __str__(self):
        return self.name



## Category와 SubCategory 데이터는 category_fixtures.json 으로 관리
class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=20)
    parent = models.ForeignKey(Category)

    def __str__(self):
        return self.name


## Store 모델

class Store(models.Model):
    name = models.CharField(max_length=80)
    address = models.CharField(max_length=80)
    tel = models.CharField(max_length=20, blank=True)
    intro = models.TextField(max_length=500, blank=True)
    hours = models.TextField(max_length=200, blank=True)

    website = models.URLField(blank=True)

    photo = models.ImageField(blank=True, upload_to=random_name_upload_to)
    store_rating = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])

    area = models.ForeignKey(Area, blank=True, null=True)
    sub_area = models.ForeignKey(SubArea, blank=True, null=True)
    categories = models.ManyToManyField(Category, blank=True)
    sub_categories = models.ManyToManyField(SubCategory, blank=True)

    ## 추가
    n_review = models.PositiveSmallIntegerField(default=0)
    menu = models.TextField(max_length=1000, blank=True)
    parking = models.CharField(max_length=20, blank=True)
    holiday = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.photo.delete()
        return super(Store, self).delete(*args, **kwargs)

    def update_store_rating_by_review_delete(self, user_rating):
        temp_total = self.store_rating * self.n_review - user_rating
        self.n_review -= 1
        self.store_rating = temp_total / self.n_review
        self.save()

def pre_on_store_save(sender, **kwargs):
    store = kwargs['instance']
    if store.photo:
        max_width = 500
        if store.photo.width > max_width or store.photo.height > max_width:
            processed_file = thumbnail(store.photo.file, max_width, max_width)
            store.photo.save(store.photo.name, File(processed_file))

pre_save.connect(pre_on_store_save, sender=Store)



## Review 모델
class Review(models.Model):
    store = models.ForeignKey(Store)
    user_rating = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    content = models.TextField(blank=True)
    photo = models.ImageField(blank=True, null=True, upload_to=random_name_upload_to)
    author = models.ForeignKey(settings.AUTH_USER_MODEL )
    created_at = models.DateTimeField(auto_now_add=True)
    n_like = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.content

    def delete(self, *args, **kwargs):
        self.photo.delete()
        self.store.update_store_rating_by_review_delete(self.user_rating)
        return super(Review, self).delete(*args, **kwargs)


## Comment 모델

class Comment(models.Model):
    review = models.ForeignKey(Review)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


