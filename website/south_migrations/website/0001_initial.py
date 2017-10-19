# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Download'
        db.create_table(u'website_download', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('upload_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'website', ['Download'])

        # Adding model 'People'
        db.create_table(u'website_people', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.CharField')(default='en', max_length=10)),
            ('name_full', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['medialibrary.MediaFile'])),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=200, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.EmailField')(max_length=200, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'website', ['People'])

        # Adding model 'PublicationCategory'
        db.create_table(u'website_publicationcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'website', ['PublicationCategory'])

        # Adding model 'Publication'
        db.create_table(u'website_publication', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.CharField')(default='en', max_length=10)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('download', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Download'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.PublicationCategory'], null=True, blank=True)),
        ))
        db.send_create_signal(u'website', ['Publication'])

        # Adding model 'Banner'
        db.create_table(u'website_banner', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.CharField')(default='en', max_length=10)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['medialibrary.MediaFile'], null=True, blank=True)),
            ('header', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('link_text', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'website', ['Banner'])

        # Adding model 'NewsItem'
        db.create_table(u'website_newsitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('intro', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(default='en', max_length=10)),
            ('translation_of', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='translations', null=True, to=orm['website.NewsItem'])),
            ('template_key', self.gf('django.db.models.fields.CharField')(default='website/newsitem_detail.html', max_length=255)),
        ))
        db.send_create_signal(u'website', ['NewsItem'])

        # Adding model 'Event'
        db.create_table(u'website_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('place', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('language', self.gf('django.db.models.fields.CharField')(default='en', max_length=10)),
            ('translation_of', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='translations', null=True, to=orm['website.Event'])),
            ('template_key', self.gf('django.db.models.fields.CharField')(default='website/event_detail.html', max_length=255)),
        ))
        db.send_create_signal(u'website', ['Event'])

        # Adding model 'RichTextContentEvents'
        db.create_table(u'website_event_richtextcontentevents', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('feincms.contrib.richtext.RichTextField')(blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='richtextcontentevents_set', to=orm['website.Event'])),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'website', ['RichTextContentEvents'])

        # Adding model 'BannerContentEvents'
        db.create_table(u'website_event_bannercontentevents', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='bannercontentevents_set', to=orm['website.Event'])),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('banner', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'website_bannercontentevents_set', to=orm['website.Banner'])),
        ))
        db.send_create_signal(u'website', ['BannerContentEvents'])

        # Adding model 'BannerContentNews'
        db.create_table(u'website_newsitem_bannercontentnews', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='bannercontentnews_set', to=orm['website.NewsItem'])),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('banner', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'website_bannercontentnews_set', to=orm['website.Banner'])),
        ))
        db.send_create_signal(u'website', ['BannerContentNews'])

        # Adding model 'RichTextContentNews'
        db.create_table(u'website_newsitem_richtextcontentnews', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('feincms.contrib.richtext.RichTextField')(blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='richtextcontentnews_set', to=orm['website.NewsItem'])),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'website', ['RichTextContentNews'])


    def backwards(self, orm):
        # Deleting model 'Download'
        db.delete_table(u'website_download')

        # Deleting model 'People'
        db.delete_table(u'website_people')

        # Deleting model 'PublicationCategory'
        db.delete_table(u'website_publicationcategory')

        # Deleting model 'Publication'
        db.delete_table(u'website_publication')

        # Deleting model 'Banner'
        db.delete_table(u'website_banner')

        # Deleting model 'NewsItem'
        db.delete_table(u'website_newsitem')

        # Deleting model 'Event'
        db.delete_table(u'website_event')

        # Deleting model 'RichTextContentEvents'
        db.delete_table(u'website_event_richtextcontentevents')

        # Deleting model 'BannerContentEvents'
        db.delete_table(u'website_event_bannercontentevents')

        # Deleting model 'BannerContentNews'
        db.delete_table(u'website_newsitem_bannercontentnews')

        # Deleting model 'RichTextContentNews'
        db.delete_table(u'website_newsitem_richtextcontentnews')


    models = {
        u'medialibrary.category': {
            'Meta': {'ordering': "['parent__title', 'title']", 'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['medialibrary.Category']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'medialibrary.mediafile': {
            'Meta': {'ordering': "['-created']", 'object_name': 'MediaFile'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['medialibrary.Category']", 'null': 'True', 'blank': 'True'}),
            'copyright': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255'}),
            'file_size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        },
        u'website.banner': {
            'Meta': {'object_name': 'Banner'},
            'header': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['medialibrary.MediaFile']", 'null': 'True', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '10'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'link_text': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'website.bannercontentevents': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'BannerContentEvents', 'db_table': "u'website_event_bannercontentevents'"},
            'banner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'website_bannercontentevents_set'", 'to': u"orm['website.Banner']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bannercontentevents_set'", 'to': u"orm['website.Event']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'website.bannercontentnews': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'BannerContentNews', 'db_table': "u'website_newsitem_bannercontentnews'"},
            'banner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'website_bannercontentnews_set'", 'to': u"orm['website.Banner']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bannercontentnews_set'", 'to': u"orm['website.NewsItem']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'website.download': {
            'Meta': {'object_name': 'Download'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'upload_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        u'website.event': {
            'Meta': {'ordering': "('start_date',)", 'object_name': 'Event'},
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '10'}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'template_key': ('django.db.models.fields.CharField', [], {'default': "'website/event_detail.html'", 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'translation_of': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'translations'", 'null': 'True', 'to': u"orm['website.Event']"})
        },
        u'website.newsitem': {
            'Meta': {'ordering': "('date',)", 'object_name': 'NewsItem'},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '10'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'template_key': ('django.db.models.fields.CharField', [], {'default': "'website/newsitem_detail.html'", 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'translation_of': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'translations'", 'null': 'True', 'to': u"orm['website.NewsItem']"})
        },
        u'website.people': {
            'Meta': {'ordering': "('name_full',)", 'object_name': 'People'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['medialibrary.MediaFile']"}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '10'}),
            'name_full': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'phone': ('django.db.models.fields.EmailField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'website.publication': {
            'Meta': {'ordering': "('date',)", 'object_name': 'Publication'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.PublicationCategory']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'download': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Download']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '10'})
        },
        u'website.publicationcategory': {
            'Meta': {'ordering': "('category',)", 'object_name': 'PublicationCategory'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'website.richtextcontentevents': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'RichTextContentEvents', 'db_table': "u'website_event_richtextcontentevents'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'richtextcontentevents_set'", 'to': u"orm['website.Event']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('feincms.contrib.richtext.RichTextField', [], {'blank': 'True'})
        },
        u'website.richtextcontentnews': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'RichTextContentNews', 'db_table': "u'website_newsitem_richtextcontentnews'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'richtextcontentnews_set'", 'to': u"orm['website.NewsItem']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('feincms.contrib.richtext.RichTextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['website']