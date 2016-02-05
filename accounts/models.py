from django.conf import settings
from django.core.files import File
from django.db import models
from django.db.models.signals import pre_save

from elf.utils import random_name_upload_to, thumbnail
from legolas.models import Area, SubArea


class UserProfile(models.Model):
    '''
    User의 확장.
    User에서 주로 사용될 것들은: email, password, username, date_joined
    '''
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(blank=True, upload_to=random_name_upload_to)
    intro = models.TextField(max_length=200, blank=True)
    n_following = models.PositiveSmallIntegerField(default=0, blank=True)
    n_follower = models.PositiveSmallIntegerField(default=0, blank=True)
    ## 이거 수정필요. 인터레스트
    interest = models.BooleanField()
    area = models.ForeignKey(Area, blank=True, null=True)
    sub_area = models.ForeignKey(SubArea, blank=True, null=True)
    n_review = models.PositiveSmallIntegerField(default=0, blank=True)

    def __str__(self):
        return self.user.username

    def delete(self, *args, **kwargs):
        self.photo.delete()
        return super(Profile, self).delete(*args, **kwargs)



def pre_on_user_profile_save(sender, **kwargs):
    user_profile = kwargs['instance']
    if user_profile.photo:
        max_width = 500
        if user_profile.photo.width > max_width or user_profile.photo.height > max_width:
            processed_file = thumbnail(user_profile.photo.file, max_width, max_width)
            user_profile.photo.save(user_profile.photo.name, File(processed_file))

pre_save.connect(pre_on_user_profile_save, sender=UserProfile)