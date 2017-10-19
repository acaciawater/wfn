from django.contrib import admin
from website.models import *
from modeltranslation.admin import TranslationAdmin
from feincms.admin import item_editor
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin



class DefaultAdmin(admin.ModelAdmin):
    pass

class DefaultFilterLangAdmin(admin.ModelAdmin):
    list_filter = ('language',)

class BannerAdmin(DefaultFilterLangAdmin):
    pass

class DownloadAdmin(DefaultAdmin):
    pass

class PublicationAdmin(DefaultFilterLangAdmin):
    list_display = ['description', 'date', 'category']

class PublicationCategoryAdmin(admin.ModelAdmin):
    pass

class PeopleAdmin(DefaultFilterLangAdmin):
    raw_id_fields = ['image']

admin.site.unregister(User)
class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline, ]
admin.site.register(User, UserProfileAdmin)



admin.site.register(Publication, PublicationAdmin)
admin.site.register(PublicationCategory, PublicationCategoryAdmin)
admin.site.register(Banner, DefaultFilterLangAdmin)
admin.site.register(Download, DefaultAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(NewsItem, NewsItemAdmin)
admin.site.register(People, PeopleAdmin)
admin.site.register(CarouselLinks, DefaultFilterLangAdmin)

