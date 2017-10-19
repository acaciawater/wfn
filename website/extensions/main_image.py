"""
Add an excerpt field to the page.
"""

from django.db import models
from django.utils.translation import ugettext_lazy as _
from feincms.module.medialibrary.models import MediaFile

from feincms import extensions


class Extension(extensions.Extension):
    def handle_model(self):
        self.model.add_to_class('main_image', models.ForeignKey(
            MediaFile,
            verbose_name=_('main image'),
            default=1,
            blank=True,
            null=True,
            help_text=_('If you link to this page with the page link content this image will also be used.')))


    def handle_modeladmin(self, modeladmin):
        modeladmin.add_extension_options('main_image')
        modeladmin.raw_id_fields = ['main_image']