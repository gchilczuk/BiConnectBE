from django.contrib.auth.models import User
from django.db import models

from descriptor.utils import sound_file_path


class Group(models.Model):
    city = models.CharField(max_length=30)

    class Meta:
        db_table = 'groups'


class Meeting(models.Model):
    date = models.DateField(auto_now_add=True)
    count_members = models.PositiveSmallIntegerField(null=True)
    count_guests = models.PositiveSmallIntegerField(null=True)
    group = models.ForeignKey(to=Group, on_delete=models.CASCADE, related_name='meetings',
                              related_query_name='meeting')

    class Meta:
        db_table = 'meetings'


class Speech(models.Model):
    person = models.ForeignKey(to='Person', on_delete=models.CASCADE, related_name='speeches',
                               related_query_name='speech')
    meeting = models.ForeignKey(to=Meeting, on_delete=models.CASCADE, related_name='speeches',
                                related_query_name='speech', null=True)
    sound_file = models.FileField(upload_to=sound_file_path, max_length=255, null=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'speeches'


class Person(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    group = models.ForeignKey(to=Group, on_delete=models.PROTECT, related_name='members',
                              related_query_name='member', null=True)
    member = models.BooleanField(default=True)
    newsletter = models.BooleanField(default=True)
    speech_confirm = models.BooleanField(default=True)

    class Meta:
        db_table = 'people'


class Requirement(models.Model):
    speech = models.ForeignKey(to=Speech, on_delete=models.CASCADE, related_name='requirements',
                               related_query_name='requirement')
    description = models.TextField()
    appearance_date = models.DateField(auto_now_add=True)
    expiration_date = models.DateField(null=True)
    fulfilled_positively = models.NullBooleanField()
    categories = models.ManyToManyField(to='Category')

    class Meta:
        db_table = 'requirements'


class Recommendation(models.Model):
    speech = models.ForeignKey(to=Speech, on_delete=models.CASCADE, related_name='recommendations',
                               related_query_name='recommendation')
    description = models.TextField()
    appearance_date = models.DateField(auto_now_add=True)
    expiration_date = models.DateField(null=True)
    categories = models.ManyToManyField(to='Category')

    class Meta:
        db_table = 'recommendation'


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    parent_category = models.ForeignKey(to='self', on_delete=models.PROTECT, related_name='subcategories',
                                        related_query_name='subcategory')

    class Meta:
        db_table = 'categories'
