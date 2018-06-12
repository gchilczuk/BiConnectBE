from django.contrib.auth.models import User
from django.db import models

from descriptor.utils import sound_file_path


class Group(models.Model):
    city = models.CharField(max_length=30)

    class Meta:
        db_table = 'groups'


class Meeting(models.Model):
    date = models.DateField()
    count_members = models.PositiveSmallIntegerField(null=True)
    count_guests = models.PositiveSmallIntegerField(null=True)
    group = models.ForeignKey(to=Group, on_delete=models.CASCADE, related_name='meetings',
                              related_query_name='meeting')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.count_members = self.speeches.filter(person__member=True).distinct().count()
        self.count_guests = self.speeches.filter(person__member=False).distinct().count()
        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        db_table = 'meetings'
        ordering = ['-date']


class BusinessDescription(models.Model):
    description = models.TextField()


class Speech(models.Model):
    person = models.ForeignKey(to='Person', on_delete=models.CASCADE, related_name='speeches',
                               related_query_name='speech', null=True)
    meeting = models.ForeignKey(to=Meeting, on_delete=models.CASCADE, related_name='speeches',
                                related_query_name='speech', null=True)
    business_description = models.ForeignKey(to=BusinessDescription, on_delete=models.SET_NULL,
                                             related_name='speech', null=True)
    sound_file = models.FileField(upload_to=sound_file_path, max_length=255, null=True)
    date = models.DateField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)

    class Meta:
        db_table = 'speeches'
        ordering = ['-id']

    def confirm(self):
        self.confirmed = True
        self.save()


class Person(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    group = models.ForeignKey(to=Group, on_delete=models.PROTECT, related_name='members',
                              related_query_name='member', null=True)
    member = models.BooleanField(default=True)
    newsletter = models.BooleanField(default=True)
    speech_confirm = models.BooleanField(default=True)

    class Meta:
        db_table = 'people'
        ordering = ['id']

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}, {self.user.email}'


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
        ordering = ['id']


class Recommendation(models.Model):
    speech = models.ForeignKey(to=Speech, on_delete=models.CASCADE, related_name='recommendations',
                               related_query_name='recommendation')
    description = models.TextField()
    appearance_date = models.DateField(auto_now_add=True)
    expiration_date = models.DateField(null=True)
    categories = models.ManyToManyField(to='Category')

    class Meta:
        db_table = 'recommendation'
        ordering = ['id']


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    parent_category = models.ForeignKey(to='self', on_delete=models.PROTECT, related_name='subcategories',
                                        related_query_name='subcategory')

    class Meta:
        db_table = 'categories'
        ordering = ['id']
