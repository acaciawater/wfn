from django.db import models
from django.utils.translation import ugettext_lazy as _
from feincms.module.medialibrary.models import MediaFile

from feincms import extensions


class Extension(extensions.Extension):
    def handle_model(self):
        self.model.add_to_class('intro_text', models.TextField(
            verbose_name=_('introduction'),
            default='',
            blank=True,
            null=True,
            help_text=_('The introduction will be shown below the title')))


    def handle_modeladmin(self, modeladmin):
        modeladmin.add_extension_options('intro_text')