'''
from modeltranslation.translator import TranslationOptions, translator
from website.models import Download, Banner
from schedule.models.events import Event


class BannerTranslationOptions(TranslationOptions):
    fields = ('link',)

class DownloadTranslationOptions(TranslationOptions):
    fields = ('upload_file',)

class EventTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)

translator.register(Banner, BannerTranslationOptions)
translator.register(Download, DownloadTranslationOptions)
translator.register(Event, EventTranslationOptions)
'''
