from django.db import models
from django.utils.translation import ugettext_lazy as _
from feincms.module.page.models import Page
from feincms.module.medialibrary.models import MediaFile
from feincms.content.medialibrary.models import MediaFileContent
from feincms.content.application.models import ApplicationContent
from website.content import *
from feincms.content.application import models as app_models
from django.db.models import signals
from feincms.management.checker import check_database_schema
from feincms.models import Base
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.core.exceptions import ObjectDoesNotExist
from feincms.admin import item_editor
from django.conf import settings
from feincms.module.page.modeladmins import PageAdmin
from django.utils.encoding import python_2_unicode_compatible
from feincms.module.page.extensions.navigation import NavigationExtension, PagePretender
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from website.forms import UserRegForm


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    job_description = models.CharField(_('Function'), max_length=200, blank=True, null=True)
    # area = models.CharField(_('Area'),
    #                         choices=(
    #                             ('sector1', _('sector1')),
    #                             ('sector2', _('sector3')),
    #                             ('sector3', _('sector3')),
    #                         ),
    #                         max_length=200,
    #                         blank=True,
    #                         null=True)
    # whence_your_interest = models.CharField(_('Whence your interest?'), max_length=200, blank=True, null=True)

    organisation = models.CharField(_('Organisation'), max_length=255, blank=True, null=True)
    country = models.CharField(_('Country'), max_length=255, blank=True, null=True)
    newsletter = models.BooleanField(_('Newsletter'), default=False)
    updates_tool_developments = models.BooleanField(_('Updates on tool developments'), default=False)

    def __unicode__(self):
        return '%s' % self.user.email


class Download(models.Model):
    upload_file = models.FileField(_('file'), upload_to='downloads/')

    def __unicode__(self):
        return '%s' % self.upload_file


class People(models.Model):
    language = models.CharField(_('language'),
                                max_length=10,
                                choices=settings.LANGUAGES,
                                default=settings.LANGUAGES[0][0])
    name_full = models.CharField(_('name full'), max_length=200)
    image = models.ForeignKey(MediaFile, verbose_name=_('image'))
    role = models.CharField(_('role'), max_length=200, blank=True, null=True)
    email = models.EmailField(_('email'), max_length=200, blank=True, null=True)
    phone = models.CharField(_('phone'), max_length=200, blank=True, null=True)
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta():
        ordering = ('name_full',)
        verbose_name_plural = _('People')

    def __unicode__(self):
        return '%s %s' % (self.language, self.name_full)

class PublicationCategory(models.Model):
    category = models.CharField(_('category'), max_length=200)

    class Meta():
        ordering = ('category',)
        verbose_name_plural = _('Publication categories')

    def __unicode__(self):
        return '%s' % self.category


class Publication(models.Model):
    language = models.CharField(_('language'),
                                max_length=10,
                                choices=settings.LANGUAGES,
                                default=settings.LANGUAGES[0][0])
    date = models.DateField(_('date'))
    description = models.TextField(_('description'))
    download = models.ForeignKey(Download, verbose_name=_('download'))
    category = models.ForeignKey(PublicationCategory, blank=True, null=True)
    require_registration = models.BooleanField(_('requires registration'), default=False)

    class Meta():
        ordering = ('-date',)

    def __unicode__(self):
        return '%s %s %s' % (self.language, self.date, self.description)


class Banner(models.Model):
    language = models.CharField(_('language'),
                                max_length=10,
                                choices=settings.LANGUAGES,
                                default=settings.LANGUAGES[0][0])
    link = models.CharField(_('link'), max_length=200,
        help_text=("Use absolute links (starting with /) or external links "
                   "(starting with http(s)://)"))
    image = models.ForeignKey(MediaFile, verbose_name=_('image'), blank=True, null=True)
    header = models.CharField(_('header'), max_length=200, blank=True, null=True)
    text = models.TextField(_('text'), blank=True, null=True)
    link_text = models.CharField(_('link text'), max_length=200, blank=True, null=True)

    def save(self, *args, **kwargs):
        # We have no need for relative links in elements that can be used on any
        # page so make them absolute.
        if not self.link.startswith('/') or not self.link.startswith('http'):
            self.link = "/" + self.link
        return super(Banner, self).save(*args, **kwargs)

    def __unicode__(self):
        if self.header:
            return '%s %s %s' % (self.language, self.link, self.header)
        return '%s %s' % (self.language, self.link)


class CarouselLinks(models.Model):
    language = models.CharField(_('language'),
                                    max_length=10,
                                    choices=settings.LANGUAGES,
                                    default=settings.LANGUAGES[0][0])
    link = models.CharField(_('link'), max_length=200)
    link_text = models.CharField(_('link text'), max_length=200)

    def __unicode__(self):
        return '%s %s' % (self.language, self.link_text)

    class Meta:
        verbose_name = _('Carousel Link')
        verbose_name_plural = _('Carousel links')


@python_2_unicode_compatible
class NewsItem(Base):
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(_('slug'))
    date = models.DateField(_('date'))
    intro = models.TextField(_('introduction'), blank=True, null=True)
    main_image = models.ForeignKey(MediaFile, verbose_name=_('main image'), blank=True, null=True)

    class Meta:
        ordering = ('-date',)
        verbose_name = _('News')
        verbose_name_plural = _('News')

    def __str__(self):
        return self.title

    @app_models.permalink
    def get_absolute_url(self):
        return ('newsitem_detail', 'website.news_urls', (), {
           'slug': self.slug,
           })

signals.post_syncdb.connect(check_database_schema(NewsItem, __name__), weak=False)


@python_2_unicode_compatible
class Event(Base):
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(_('slug'))
    start_date = models.DateTimeField(_('start date'))
    end_date = models.DateTimeField(_('end date'))
    place = models.CharField(_('place'), max_length=200)
    intro = models.TextField(_('introduction'), blank=True, null=True)

    class Meta:
        ordering = ('start_date',)
        verbose_name = _('Event')
        verbose_name_plural = _('Events')

    def __str__(self):
        return self.title

    @app_models.permalink
    def get_absolute_url(self):
        return ('event_detail', (self.id,), {})

signals.post_syncdb.connect(check_database_schema(Event, __name__), weak=False)


class NewsItemAdmin(item_editor.ItemEditor):
    search_fields = ['title', 'slug']
    list_display = ['__str__', 'date']
    list_filter = []
    prepopulated_fields = {
        'slug': ('title',),
    }
    raw_id_fields = ['main_image',]


NewsItemAdmin.save_on_top = True


class EventAdmin(item_editor.ItemEditor):
    search_fields = ['title', 'slug']
    list_display = ['__str__', 'start_date', 'end_date']
    list_filter = []
    prepopulated_fields = {
        'slug': ('title',),
    }
    raw_id_fields = []

EventAdmin.save_on_top = True

Page.register_extensions(
    'feincms.module.extensions.seo',
    'feincms.module.extensions.datepublisher',
    'feincms.module.extensions.translations',
    'feincms.module.extensions.changedate',
    'feincms.module.page.extensions.navigation',
    'feincms.module.page.extensions.titles',
    'website.extensions.partner_login_required',
    'website.extensions.main_image',
    'website.extensions.show_in_footer',
    'website.extensions.intro_text',
)

NewsItem.register_extensions(
    'feincms.module.extensions.translations',
    'feincms.module.extensions.seo',
)

Event.register_extensions(
    'feincms.module.extensions.translations',
    'feincms.module.extensions.seo',
)

PageAdmin.save_on_top = True

Page.register_templates(
    {
        'title': _('homepage template'),
        'path': 'homepage.html',
        'regions': (
            ('carousel', _('carousel')),
            ('homepage_top_left', _('top left')),
            ('homepage_top_middle', _('top middle')),
            ('homepage_top_right', _('top right')),
            ('homepage_top', _('top')),
            ('homepage_main', _('main')),
            ('homepage_sidebar', _('sidebar')),
        ),
    },
    {
        'title': _('subhome template'),
        'path': 'subhome.html',
        'regions': (
            ('subhome_top', _('top')),
            ('subhome_main', _('main')),
            ('subhome_sidebar', _('sidebar')),
        ),
    },
    {
        'title': _('content template'),
        'path': 'content.html',
        'regions': (
            ('content_top', _('top')),
            ('content_main', _('main')),
            ('content_sidebar', _('sidebar')),
        ),
    },
    {
        'title': _('news template'),
        'path': 'news.html',
        'regions': (
            ('news_main', _('main')),
            ('news_sidebar', _('sidebar')),
        ),
    },
    {
        'title': _('events template'),
        'path': 'events.html',
        'regions': (
            ('events_main', _('main')),
            ('events_sidebar', _('sidebar')),
        ),
    },
    {
        'title': _('empty template'),
        'path': 'empty.html',
        'regions': (
            ('empty_main', _('main')),
        ),
    },
    {
        'title': _('search template'),
        'path': 'search.html',
        'regions': (
        ),
    },
)

NewsItem.register_templates(
    {
        'title': _('news template'),
        'path': 'website/newsitem_detail.html',
        'regions': (
            ('news_main', _('main')),
            ('news_sidebar', _('sidebar')),
        ),
    },
)
Event.register_templates(
    {
        'title': _('events template'),
        'path': 'website/event_detail.html',
        'regions': (
            ('events_main', _('main')),
            ('events_sidebar', _('sidebar')),
        ),
    },
)


class EventsNavigationExtension(NavigationExtension):
    name = _('Events navigation')

    def children(self, page, **kwargs):
        for event in Event.objects.all():
            yield PagePretender(
                title=event.title,
                url=event.get_absolute_url(),
                )


class NewsItemNavigationExtension(NavigationExtension):
    name = _('NewsItem navigation')

    def children(self, page, **kwargs):
        for newsitem in NewsItem.objects.all():
            yield PagePretender(
                title=newsitem.title,
                url=newsitem.get_absolute_url(),
                )


# page content
Page.create_content_type(ApplicationContent,
                         APPLICATIONS=(
                             ('website.news_urls', 'News application'),
                             ('website.events_urls', 'Events application'),
                         ),
                         regions=(
                             'news_main',
                             'events_main',
                         ))

Page.create_content_type(RichTextContent, regions=(
    'homepage_main',
    'subhome_main',
    'content_main',
    'homepage_top_left',
    'homepage_top_middle',
    'homepage_top_right',
))
Page.create_content_type(ButtonContent, regions=(
    'content_main',
    'homepage_top_left',
    'homepage_top_middle',
    'homepage_top_right',
))
Page.create_content_type(BannerContent, regions=(
    'homepage_main',
    'subhome_main',
    'content_main',
    'content_main',

    'homepage_sidebar',
    'subhome_sidebar',
    'content_sidebar',
    'news_sidebar',
    'events_sidebar',
))
Page.create_content_type(QuoteContent, regions=(
    'homepage_main',
    'subhome_main',
    'content_main',
))
Page.create_content_type(AricleContent, regions=(
    'homepage_main',
    'subhome_main',
    'content_main',
))
Page.create_content_type(PageLinkContent, regions=(
    'homepage_main',
    'subhome_main',
    'content_main',
))
Page.create_content_type(PeopleContent, regions=(
    'homepage_main',
    'subhome_main',
    'content_main',
))
Page.create_content_type(ReportContent, regions=(
    'homepage_sidebar',
    'subhome_sidebar',
    'content_sidebar',
    'news_sidebar',
    'events_sidebar',
))
Page.create_content_type(IframeContent, regions=(
    'content_top',
    'content_main',
    'empty_main',
))
Page.create_content_type(StoryContent, regions=(
    'homepage_top',
    'subhome_top',
    'content_top',
))
Page.create_content_type(CarouselContent, regions=(
    'carousel',
))

Page.create_content_type(RelatedNewsContent, regions=(
    'homepage_main',
    'subhome_main',
    'content_main',
    'homepage_sidebar',
    'subhome_sidebar',
    'content_sidebar',
    'news_sidebar',
    'events_sidebar',
))
Page.create_content_type(LatestNewsContent, regions=(
    'homepage_main',
    'subhome_main',
    'content_main',
    'homepage_sidebar',
    'subhome_sidebar',
    'content_sidebar',
    'news_sidebar',
    'events_sidebar',
))
Page.create_content_type(RelatedEventContent, regions=(
    'homepage_main',
    'subhome_main',
    'content_main',
    'homepage_sidebar',
    'subhome_sidebar',
    'content_sidebar',
    'news_sidebar',
    'events_sidebar',
))
Page.create_content_type(UpcomingEventContent, regions=(
    'homepage_main',
    'subhome_main',
    'content_main',
    'homepage_sidebar',
    'subhome_sidebar',
    'content_sidebar',
    'news_sidebar',
    'events_sidebar',
))
Page.create_content_type(FilteredEventContent, regions=(
    'homepage_main',
    'subhome_main',
    'content_main',
    'homepage_sidebar',
    'subhome_sidebar',
    'content_sidebar',
    'news_sidebar',
    'events_sidebar',
))
Page.create_content_type(RelatedPublicationContent, regions=(
    'homepage_main',
    'subhome_main',
    'content_main',
))
Page.create_content_type(LatestPublicationContent, regions=(
    'homepage_main',
    'subhome_main',
    'content_main',
))
Page.create_content_type(FilteredPublicationContent, regions=(
    'homepage_main',
    'subhome_main',
    'content_main',
))

# event content
Event.create_content_type(RichTextContent, regions=(
    'events_main',
), class_name='RichTextContentEvents')
Event.create_content_type(BannerContent, regions=(
    'events_sidebar',
), class_name='BannerContentEvents')


# newsitem content
NewsItem.create_content_type(BannerContent, regions=(
    'news_sidebar',
), class_name='BannerContentNews')
NewsItem.create_content_type(RichTextContent, regions=(
    'news_main',
), class_name='RichTextContentNews')


def authenticated_request_processor(page, request):
    if (not request.user.is_authenticated() or not request.user.groups.filter(name="partners")) and \
        page.partner_login_required:
        previous = request.GET.get('previous-page', '/%s/' % request.LANGUAGE_CODE)
        if previous is request.META.get('PATH_INFO'):
            previous = '/'
        return HttpResponseRedirect('%s#partner-login=1&navigate-prep=%s' % (previous, request.META.get('PATH_INFO', '/')))

Page.register_request_processor(authenticated_request_processor)


@receiver(pre_save, sender=Page)
def set_page_partner_login(sender, **kwargs):
    obj = kwargs['instance']
    try:
        old_obj = Page.objects.get(pk=obj.pk)
        if not obj.partner_login_required is old_obj.partner_login_required:

            for child in obj.get_children():
                child.partner_login_required = obj.partner_login_required
                child.save()
    except ObjectDoesNotExist:
        if obj.parent:
            obj.partner_login_required = obj.parent.partner_login_required


def user_created(sender, user, request, **kwargs):
    form = UserRegForm(request.POST)

    # Add the first and last name fields to the user model
    user.first_name = form.data['first_name']
    user.last_name = form.data['last_name']
    user.save()

    # Create a user profile which stores additional data for this user:
    data = UserProfile(user=user)
    data.job_description = form.data["job_description"]
    data.organisation = form.data["organisation"]
    data.country = form.data["country"]
    data.newsletter = form.data["newsletter"]
    data.updates_tool_developments = form.data["updates_tool_developments"]
    data.save()

from registration.signals import user_registered
user_registered.connect(user_created)






