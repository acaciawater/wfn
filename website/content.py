from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.template.context import RequestContext
from django.template.loader import render_to_string
from feincms.admin.item_editor import ItemEditorForm
from feincms.content.richtext.models import RichTextContent as FeinRichTextContent
from markitup.widgets import MarkItUpWidget
from django import forms
from django.db import models
from sortedm2m.fields import SortedManyToManyField
from feincms.admin.item_editor import FeinCMSInline
from feincms.module.medialibrary.models import MediaFile
from django.conf import settings
from django.template.base import TemplateDoesNotExist



class MarkItUpFeinWidget(MarkItUpWidget):
    def render(self, name, value, attrs=None):
        html = super(MarkItUpWidget, self).render(name, value, attrs)

        if self.auto_preview:
            auto_preview = "$('a[title=\"Preview\"]').trigger('mouseup');"
        else:
            auto_preview = ''

        html += ('<script type="text/javascript">'
                 '(function($) { '
                 '$(document).ready(function() {'
                 '  $("#%(id)s:not(.markItUpEditor)").markItUp(mySettings);'
                 '  %(auto_preview)s '
                 '});'
                 '})(jQuery);'
                 '</script>' % {'id': attrs['id'],
                                'auto_preview': auto_preview})
        return mark_safe(html)


class RichTextContent(FeinRichTextContent):
    class Meta:
        abstract = True
        verbose_name = _('rich text')
        verbose_name_plural = _('rich texts')

    def render(self, **kwargs):
        return render_to_string('content/richtext.html', {
            'text': self.text,
        }, context_instance=RequestContext(kwargs['request']))

    @classmethod
    def initialize_type(cls):
        class TextileContentAdminForm(ItemEditorForm):
            text = forms.CharField(widget=MarkItUpFeinWidget(), required=False, label=_('text'))

        cls.feincms_item_editor_form = TextileContentAdminForm


class LatestPublicationContent(models.Model):
    header = models.CharField(_('header'), max_length=200, blank=True, null=True)
    count = models.PositiveIntegerField(_('count'), default=1)

    def render(self, **kwargs):
        from website.models import Publication
        return render_to_string('content/publication.html', {
            'object': self,
            'publication_collection': Publication.objects.filter(language=kwargs.get('request').LANGUAGE_CODE)
        }, context_instance=RequestContext(kwargs['request']))

    class Meta:
        abstract = True
        verbose_name = _('latest publications')
        verbose_name_plural = _('latest publications')


class RelatedPublicationContent(models.Model):
    header = models.CharField(_('header'), max_length=200, blank=True, null=True)

    def render(self, **kwargs):
        return render_to_string('content/publication.html', {
            'object': self,
            'publication_collection': self.publication_collection.all()
        }, context_instance=RequestContext(kwargs['request']))

    @classmethod
    def initialize_type(cls):
        from website.models import Publication
        cls.add_to_class('publication_collection',
            models.ManyToManyField(Publication, verbose_name=_('publication items'),
                related_name='%s_%s_set' % (cls._meta.app_label, cls._meta.module_name)
            ))

        class RelatedPublicationContentAdminForm(ItemEditorForm):
            def __init__(self, *args, **kwargs):
                super(RelatedPublicationContentAdminForm, self).__init__(*args, **kwargs)
                try:
                    instance = kwargs['instance']
                    self.fields['publication_collection'].queryset = Publication.objects.filter(language=instance.parent.language)
                except KeyError:
                    pass

        cls.feincms_item_editor_form = RelatedPublicationContentAdminForm

    class Meta:
        abstract = True
        verbose_name = _('related publications')
        verbose_name_plural = _('related publications')


class FilteredPublicationContent(models.Model):
    header = models.CharField(_('header'), max_length=200, blank=True, null=True)
    start_date = models.DateField(_('start date'), blank=True, null=True)
    end_date = models.DateField(_('end date'), blank=True, null=True)
    count = models.PositiveIntegerField(_('count'), blank=True, null=True)

    @classmethod
    def initialize_type(cls):
        from website.models import PublicationCategory
        cls.add_to_class('category',
            models.ManyToManyField(PublicationCategory, verbose_name=_('category'),
                                   blank=True,
                                   null=True,
                                   related_name='%s_%s_set' % (cls._meta.app_label, cls._meta.module_name)
            ))



    def render(self, **kwargs):
        request = kwargs['request']
        from website.models import Publication
        publications = Publication.objects.filter(language=request.LANGUAGE_CODE)
        categories = [category.id for category in self.category.all()]
        if self.start_date:
            publications = publications.filter(date__gte=self.start_date)
        if self.end_date:
            publications = publications.filter(date__lte=self.end_date)

        if categories:
            publications = publications.filter(category__in=categories)

        if self.count:
            publications = publications[:self.count]


        return render_to_string('content/publication.html', {
            'object': self,
            'publication_collection': publications
        }, context_instance=RequestContext(request))

    class Meta:
        abstract = True
        verbose_name = _('filtered publications')
        verbose_name_plural = _('filtered publications')


class QuoteContent(models.Model):
    text = models.TextField(_('text'))
    author = models.CharField(_('author'), max_length=100, blank=True, null=True)

    def render(self, **kwargs):
        return render_to_string('content/quote.html', {
            'object': self,
        }, context_instance=RequestContext(kwargs['request']))

    class Meta:
        abstract = True
        verbose_name_plural = _('quote')
        verbose_name = _('quote')


class ReportContent(models.Model):
    header = models.CharField(_('header'), max_length=200, blank=True, null=True)
    title = models.CharField(_('title'), max_length=200)
    text = models.TextField(_('text'), blank=True, null=True)
    link = models.CharField(_('link'), max_length=200, blank=True, null=True)
    link_text = models.CharField(_('link text'), max_length=200, blank=True, null=True)

    def render(self, **kwargs):
        return render_to_string('content/report.html', {
            'object': self,
        }, context_instance=RequestContext(kwargs['request']))

    class Meta:
        abstract = True
        verbose_name_plural = _('report')
        verbose_name = _('report')


class BannerContent(models.Model):
    def render(self, **kwargs):
        return render_to_string('content/banner.html', {
            'object': self,
        }, context_instance=RequestContext(kwargs['request']))

    @classmethod
    def initialize_type(cls):
        from website.models import Banner
        cls.add_to_class('banner',
            models.ForeignKey(Banner, verbose_name=_('banner'),
                related_name='%s_%s_set' % (cls._meta.app_label, cls._meta.module_name)
            ))

        class BannerContentAdminForm(ItemEditorForm):
            def __init__(self, *args, **kwargs):
                super(BannerContentAdminForm, self).__init__(*args, **kwargs)
                try:
                    instance = kwargs['instance']
                    self.fields['banner'].queryset = Banner.objects.filter(language=instance.parent.language)
                except KeyError:
                    pass

        cls.feincms_item_editor_form = BannerContentAdminForm

    class Meta:
        abstract = True
        verbose_name = _('banner')
        verbose_name_plural = _('banner')

class ButtonContent(models.Model):
    link = models.CharField(_('link'), max_length=200)
    link_text = models.CharField(_('link text'), max_length=200)

    class Meta:
        abstract = True
        verbose_name = _('button')
        verbose_name_plural = _('buttons')

    def render(self, **kwargs):
        return render_to_string('content/button.html', {
            'object': self,
        }, context_instance=RequestContext(kwargs['request']))


class PeopleContent(models.Model):
    def render(self, **kwargs):
        return render_to_string('content/people.html', {
            'object': self,
        }, context_instance=RequestContext(kwargs['request']))

    @classmethod
    def initialize_type(cls):
        from website.models import People
        cls.add_to_class('people',
            models.ManyToManyField(People, verbose_name=_('people'),
                related_name='%s_%s_set' % (cls._meta.app_label, cls._meta.module_name)
            ))

        class PeopleContentAdminForm(ItemEditorForm):
            def __init__(self, *args, **kwargs):
                super(PeopleContentAdminForm, self).__init__(*args, **kwargs)
                try:
                    instance = kwargs['instance']
                    self.fields['people'].queryset = People.objects.filter(language=instance.parent.language)
                except KeyError:
                    pass

        cls.feincms_item_editor_form = PeopleContentAdminForm

    class Meta:
        abstract = True
        verbose_name = _('people')
        verbose_name_plural = _('people')


class RelatedNewsContent(models.Model):
    header = models.CharField(_('header'), max_length=200, blank=True, null=True)

    def render(self, **kwargs):

        template = 'content/newsitem_%s.html' % self.region
        data = {
            'object': self,
            'newsitem_collection': self.newsitem_collection.all(),
        }
        context = RequestContext(kwargs['request'])

        try:
            return render_to_string(template, data, context_instance=context)
        except TemplateDoesNotExist:
            return render_to_string('content/related_news.html', data, context_instance=context)


    @classmethod
    def initialize_type(cls):
        from website.models import NewsItem
        cls.add_to_class('newsitem_collection',
            models.ManyToManyField(NewsItem, verbose_name=_('news items'),
                related_name='%s_%s_set' % (cls._meta.app_label, cls._meta.module_name),

            ))

        class RelatedNewsContentAdminForm(ItemEditorForm):
            def __init__(self, *args, **kwargs):

                super(RelatedNewsContentAdminForm, self).__init__(*args, **kwargs)
                try:
                    instance = kwargs['instance']
                    self.fields['newsitem_collection'].queryset = NewsItem.objects.filter(language=instance.parent.language)
                except KeyError:
                    pass

        cls.feincms_item_editor_form = RelatedNewsContentAdminForm

    class Meta:
        abstract = True
        verbose_name = _('related news')
        verbose_name_plural = _('related news')


class LatestNewsContent(models.Model):
    header = models.CharField(_('header'), max_length=200, blank=True, null=True)
    count = models.PositiveIntegerField(_('count'), default=1)

    def render(self, **kwargs):
        from website.models import NewsItem
        template = 'content/newsitem_%s.html' % self.region
        import re
        p = re.compile(r'^/(?P<lang>[a-zA-Z]+)/.*$')
        lang =  p.search(kwargs['request'].path_info).group('lang')
        data = {
            'object': self,
            'newsitem_collection': NewsItem.objects.filter(language=lang)[:self.count],
        }
        context = RequestContext(kwargs['request'])
        try:
            return render_to_string(template, data, context_instance=context)
        except TemplateDoesNotExist:
            return render_to_string('content/related_news.html', data, context_instance=context)


    class Meta:
        abstract = True
        verbose_name = _('latest news')
        verbose_name_plural = _('latest news')


class UpcomingEventContent(models.Model):
    header = models.CharField(_('header'), max_length=200, blank=True, null=True)
    count = models.PositiveIntegerField(_('count'), default=1)

    def render(self, **kwargs):
        from website.models import Event
        from datetime import datetime
        template = 'content/events_%s.html' % self.region
        data = {
            'object': self,
            'event_collection': Event.objects.filter(language=kwargs['request'].LANGUAGE_CODE,
                                                     end_date__gte=datetime.now())[:self.count],
        }
        context = RequestContext(kwargs['request'])

        try:
            return render_to_string(template, data, context_instance=context)
        except TemplateDoesNotExist:
            return render_to_string('content/related_events.html', data, context_instance=context)

    class Meta:
        abstract = True
        verbose_name = _('upcoming events')
        verbose_name_plural = _('upcoming events')


class RelatedEventContent(models.Model):
    header = models.CharField(_('header'), max_length=200, blank=True, null=True)

    def render(self, **kwargs):
        from datetime import datetime
        template = 'content/events_%s.html' % self.region
        data = {
            'object': self,
            'event_collection': self.event_collection.filter(language=kwargs['request'].LANGUAGE_CODE, end_date__gte=datetime.now())
        }
        context = RequestContext(kwargs['request'])

        try:
            return render_to_string(template, data, context_instance=context)
        except TemplateDoesNotExist:
            return render_to_string('content/related_events.html', data, context_instance=context)

    @classmethod
    def initialize_type(cls):
        from website.models import Event
        cls.add_to_class('event_collection',
            models.ManyToManyField(Event, verbose_name=_('events'),
                related_name='%s_%s_set' % (cls._meta.app_label, cls._meta.module_name)
            ))

        class RelatedEventContentAdminForm(ItemEditorForm):
            def __init__(self, *args, **kwargs):
                super(RelatedEventContentAdminForm, self).__init__(*args, **kwargs)
                try:
                    instance = kwargs['instance']
                    self.fields['newsitem_collection'].queryset = Event.objects.filter(language=instance.parent.language)
                except KeyError:
                    pass

        cls.feincms_item_editor_form = RelatedEventContentAdminForm

    class Meta:
        abstract = True
        verbose_name = _('related events')
        verbose_name_plural = _('related events')

class FilteredEventContent(models.Model):
    header = models.CharField(_('header'), max_length=200, blank=True, null=True)
    start_date = models.DateTimeField(_('start date & time'), blank=True, null=True)
    end_date = models.DateTimeField(_('end date & time'), blank=True, null=True)
    past_events = models.BooleanField(_('include past events'), default=False)
    order = models.BooleanField(_('descending'), help_text=_('if checked future events become first'), default=False)
    count = models.PositiveIntegerField(_('count'), help_text=_('limit final count to entered number'), blank=True, null=True)

    def render(self, **kwargs):
        from datetime import datetime
        from website.models import Event
        events = Event.objects.filter(language=kwargs['request'].LANGUAGE_CODE)
        template = 'content/events_%s.html' % self.region
        if not self.past_events:
            events = events.filter(start_date__gte=datetime.now())
        if self.start_date:
            events = events.filter(start_date__gte=self.start_date)
        if self.end_date:
            events = events.filter(end_date__lte=self.end_date)
        if self.order:
            events = events.order_by('-start_date')
        if self.count:
            events = events[:self.count]

        data = {
            'object': self,
            'event_collection': events,
        }
        context = RequestContext(kwargs['request'])

        try:
            return render_to_string(template, data, context_instance=context)
        except TemplateDoesNotExist:
            return render_to_string('content/related_events.html', data, context_instance=context)

    class Meta:
        abstract = True
        verbose_name = _('filtered events')
        verbose_name_plural = _('filtered events')


class CarouselContentInline(FeinCMSInline):
    raw_id_fields = ('image', 'background')


class CarouselContent(models.Model):
    header = models.CharField(_('header'), max_length=200)
    tab_text = models.CharField(_('tab text'), max_length=100)
    link_text = models.CharField(_('link text'), max_length=200, blank=True, null=True)
    sub_header = models.CharField(_('sub header'), max_length=200, blank=True, null=True)
    last = models.BooleanField(_('last'), default=False)

    feincms_item_editor_inline = CarouselContentInline

    def render(self, **kwargs):
        from website.models import CarouselLinks
        links = []
        if self.last:
            links = [link for link in CarouselLinks.objects.filter(language=kwargs['request'].LANGUAGE_CODE)]
        return render_to_string('content/carousel.html', {
            'object': self,
            'links': links,
        }, context_instance=RequestContext(kwargs['request']))
    def render_tab(self, **kwargs):
        return render_to_string('content/carousel_tab.html', {
            'object': self,
        })

    @classmethod
    def initialize_type(cls):
        cls.add_to_class('image',
            models.ForeignKey(MediaFile, verbose_name=_('image'),
                related_name='%s_%s_set' % (cls._meta.app_label, cls._meta.module_name)
            ))
        cls.add_to_class('background',
            models.ForeignKey(MediaFile, verbose_name=_('overlay image'),
                related_name='%s_%s_background_set' % (cls._meta.app_label, cls._meta.module_name),
                blank=True,
                null=True
                )
            )

    class Meta:
        abstract = True
        verbose_name = _('carousel item')
        verbose_name_plural = _('carousel item')


class ContentImageInline(FeinCMSInline):
    raw_id_fields = ('image', )


class StoryContent(models.Model):
    header = models.CharField(_('header'), max_length=200)
    sub_header = models.CharField(_('sub header'), max_length=200, blank=True, null=True)
    text = models.TextField(_('text'))
    link = models.CharField(_('link'), max_length=200, blank=True, null=True)
    link_text = models.CharField(_('link text'), max_length=200, blank=True, null=True)
    image_mask = models.CharField(_('image mask'),
                                  choices=(
                                      ('mask-1', 'mask-1'),
                                      ('mask-1b', 'mask-1 mirror'),
                                      ('mask-2', 'mask-2'),
                                      ('mask-2b', 'mask-2 mirror'),
                                      ('mask-3', 'mask-3'),
                                      ('mask-3b', 'mask-3 mirror'),
                                      ('mask-4', 'mask-4'),
                                      ('mask-4b', 'mask-4 mirror'),
                                      ('mask-5', 'mask-5'),
                                      ('mask-6', 'mask-6'),
                                      ('mask-7', 'mask-7'),
                                      ('mask-8', 'mask-8'),
                                      ('mask-9', 'mask-9'),
                                      ('mask-10', 'mask-10'),
                                      ('mask-11', 'mask-11'),
                                      ('mask-12', 'mask-12'),
                                  ),
                                  max_length=100,
                                  default='mask-1')
    image_position = models.CharField(_('image position'),
                                  choices=(('drop', 'left'), ('dropExt', 'right'),),
                                  max_length=100,
                                  default='drop')

    feincms_item_editor_inline = ContentImageInline

    def render(self, **kwargs):
        return render_to_string('content/story.html', {
            'object': self,
        }, context_instance=RequestContext(kwargs['request']))

    @classmethod
    def initialize_type(cls):
        cls.add_to_class('image',
            models.ForeignKey(MediaFile, verbose_name=_('image'),
                related_name='%s_%s_set' % (cls._meta.app_label, cls._meta.module_name)
            ))

    class Meta:
        abstract = True
        verbose_name = _('story item')
        verbose_name_plural = _('story items')


class AricleContent(models.Model):
    header = models.CharField(_('header'), max_length=200)
    text = models.TextField(_('text'))
    link = models.CharField(_('link'), max_length=200, blank=True, null=True)
    link_text = models.CharField(_('link text'), max_length=200, blank=True, null=True)

    feincms_item_editor_inline = ContentImageInline

    def render(self, **kwargs):
        return render_to_string('content/article.html', {
            'object': self,
        }, context_instance=RequestContext(kwargs['request']))

    @classmethod
    def initialize_type(cls):
        cls.add_to_class('image',
            models.ForeignKey(MediaFile, verbose_name=_('image'),
                related_name='%s_%s_set' % (cls._meta.app_label, cls._meta.module_name)
            ))

    class Meta:
        abstract = True
        verbose_name = _('article item')
        verbose_name_plural = _('article items')

class IframeContent(models.Model):
    url = models.CharField(_('url'), max_length=200)
    width = models.PositiveIntegerField(_('width'), blank=True, null=True, help_text=_('When empty, width is 100%'))
    height = models.PositiveIntegerField(_('height'), blank=True, null=True, help_text=_('When empty, height is 100%'))
    scrollable = models.BooleanField(_('scrollable'), default=False)

    def render(self, **kwargs):
        return render_to_string('content/iframe.html', {
            'object': self,
        }, context_instance=RequestContext(kwargs['request']))

    class Meta:
        abstract = True
        verbose_name = _('iframe')
        verbose_name_plural = _('iframe items')


class PageLinkContentInline(FeinCMSInline):
    raw_id_fields = ('page', )


class PageLinkContent(models.Model):
    feincms_item_editor_inline = PageLinkContentInline
    def render(self, **kwargs):
        obj = {
            "link": self.page.get_absolute_url(),
            "header": self.page.title,
            "image": self.page.main_image,
        }
        return render_to_string('content/article.html', {
            'object': obj,
        }, context_instance=RequestContext(kwargs['request']))

    @classmethod
    def initialize_type(cls):
        from feincms.module.page.models import Page
        cls.add_to_class('page',
            models.ForeignKey(Page, verbose_name=_('page'),
                related_name='%s_%s_set' % (cls._meta.app_label, cls._meta.module_name)
            ))

    class Meta:
        abstract = True
        verbose_name = _('page link')
        verbose_name_plural = _('page links')

