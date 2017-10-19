"""
Add an excerpt field to the page.
"""

from django.db import models
from django.utils.translation import ugettext_lazy as _

from feincms import extensions


class Extension(extensions.Extension):
    def handle_model(self):
        self.model.add_to_class('partner_login_required', models.BooleanField(
            _('partner login required'),
            help_text=_('If changed all children of this page will be marked with the same value. '
                        'If checked viewing this page will be restricted to partner login only.')))

    def handle_modeladmin(self, modeladmin):
        modeladmin.list_display.extend(['partner_login_required'])
        modeladmin.list_filter.extend(['partner_login_required'])
        modeladmin.add_extension_options('partner_login_required')