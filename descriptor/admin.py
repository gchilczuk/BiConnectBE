from django.contrib import admin

from descriptor.models import Group, Meeting, Speech, Person, Requirement, Recommendation, Category


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    pass


@admin.register(Speech)
class SpeechAdmin(admin.ModelAdmin):
    pass


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass


@admin.register(Requirement)
class RequirementAdmin(admin.ModelAdmin):
    pass


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
