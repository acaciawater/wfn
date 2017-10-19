"""
Add an excerpt field to the page.
"""

from django.db import models
from django.utils.translation import ugettext_lazy as _

from feincms import extensions


class Extension(extensions.Extension):
    def handle_model(self):
        self.model.add_to_class('show_in_footer', models.BooleanField(
            _('show in footer'),
            help_text=_('If selected this page will shown in the the footer')))

    def handle_modeladmin(self, modeladmin):
        modeladmin.list_display.extend(['show_in_footer'])
        modeladmin.list_filter.extend(['show_in_footer'])
        modeladmin.add_extension_options('show_in_footer')