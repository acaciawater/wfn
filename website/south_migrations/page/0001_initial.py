# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Page'
        db.create_table(u'page_page', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=150)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['page.Page'])),
            ('in_navigation', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('override_url', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('redirect_to', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('_cached_url', self.gf('django.db.models.fields.CharField')(default='', max_length=255, db_index=True, blank=True)),
            ('meta_keywords', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('meta_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('publication_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 12, 21, 0, 0))),
            ('publication_end_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(default='en', max_length=10)),
            ('translation_of', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='translations', null=True, to=orm['page.Page'])),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('modification_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('navigation_extension', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('_content_title', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('_page_title', self.gf('django.db.models.fields.CharField')(max_length=69, blank=True)),
            ('partner_login', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('template_key', self.gf('django.db.models.fields.CharField')(default='homepage.html', max_length=255)),
        ))
        db.send_create_signal(u'page', ['Page'])

        # Adding model 'ApplicationContent'
        db.create_table(u'page_page_applicationcontent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parameters', self.gf('feincms.contrib.fields.JSONField')(null=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='applicationcontent_set', to=orm['page.Page'])),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('urlconf_path', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'page', ['ApplicationContent'])

        # Adding model 'StoryContent'
        db.create_table(u'page_page_storycontent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('header', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('sub_header', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('link_text', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='storycontent_set', to=orm['page.Page'])),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'page_storycontent_set', to=orm['medialibrary.MediaFile'])),
        ))
        db.send_create_signal(u'page', ['StoryContent'])

        # Adding model 'CarouselContent'
        db.create_table(u'page_page_carouselcontent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('header', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('tab_text', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('link_text', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('sub_header', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='carouselcontent_set', to=orm['page.Page'])),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'page_carouselcontent_set', to=orm['medialibrary.MediaFile'])),
        ))
        db.send_create_signal(u'page', ['CarouselContent'])

        # Adding model 'BannerContent'
        db.create_table(u'page_page_bannercontent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='bannercontent_set', to=orm['page.Page'])),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('banner', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'page_bannercontent_set', to=orm['website.Banner'])),
        ))
        db.send_create_signal(u'page', ['BannerContent'])

        # Adding model 'QuoteContent'
        db.create_table(u'page_page_quotecontent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='quotecontent_set', to=orm['page.Page'])),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'page', ['QuoteContent'])

        # Adding model 'RichTextContent'
        db.create_table(u'page_page_richtextcontent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('feincms.contrib.richtext.RichTextField')(blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='richtextcontent_set', to=orm['page.Page'])),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'page', ['RichTextContent'])

        # Adding model 'RelatedNewsContent'
        db.create_table(u'page_page_relatednewscontent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('header', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='relatednewscontent_set', to=orm['page.Page'])),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'page', ['RelatedNewsContent'])

        # Adding M2M table for field newsitem_collection on 'RelatedNewsContent'
        m2m_table_name = db.shorten_name(u'page_page_relatednewscontent_newsitem_collection')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('relatednewscontent', models.ForeignKey(orm[u'page.relatednewscontent'], null=False)),
            ('newsitem', models.ForeignKey(orm[u'website.newsitem'], null=False))
        ))
        db.create_unique(m2m_table_name, ['relatednewscontent_id', 'newsitem_id'])

        # Adding model 'LatestNewsContent'
        db.create_table(u'page_page_latestnewscontent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('header', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('count', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='latestnewscontent_set', to=orm['page.Page'])),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'page', ['LatestNewsContent'])

        # Adding model 'UpcomingEventContent'
        db.create_table(u'page_page_upcomingeventcontent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('header', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('count', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='upcomingeventcontent_set', to=orm['page.Page'])),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'page', ['UpcomingEventContent'])

        # Adding model 'RelatedEventContent'
        db.create_table(u'page_page_relatedeventcontent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('header', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='relatedeventcontent_set', to=orm['page.Page'])),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'page', ['RelatedEventContent'])

        # Adding M2M table for field event_collection on 'RelatedEventContent'
        m2m_table_name = db.shorten_name(u'page_page_relatedeventcontent_event_collection')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('relatedeventcontent', models.ForeignKey(orm[u'page.relatedeventcontent'], null=False)),
            ('event', models.ForeignKey(orm[u'website.event'], null=False))
        ))
        db.create_unique(m2m_table_name, ['relatedeventcontent_id', 'event_id'])

        # Adding model 'FilteredEventContent'
        db.create_table(u'page_page_filteredeventcontent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('header', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('past_events', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('order', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('count', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='filteredeventcontent_set', to=orm['page.Page'])),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'page', ['FilteredEventContent'])

        # Adding model 'RelatedPublicationContent'
        db.create_table(u'page_page_relatedpublicationcontent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('header', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='relatedpublicationcontent_set', to=orm['page.Page'])),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'page', ['RelatedPublicationContent'])

        # Adding M2M table for field publication_collection on 'RelatedPublicationContent'
        m2m_table_name = db.shorten_name(u'page_page_relatedpublicationcontent_publication_collection')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('relatedpublicationcontent', models.ForeignKey(orm[u'page.relatedpublicationcontent'], null=False)),
            ('publication', models.ForeignKey(orm[u'website.publication'], null=False))
        ))
        db.create_unique(m2m_table_name, ['relatedpublicationcontent_id', 'publication_id'])

        # Adding model 'LatestPublicationContent'
        db.create_table(u'page_page_latestpublicationcontent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('header', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('count', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='latestpublicationcontent_set', to=orm['page.Page'])),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'page', ['LatestPublicationContent'])

        # Adding model 'AricleContent'
        db.create_table(u'page_page_ariclecontent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('header', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('link_text', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ariclecontent_set', to=orm['page.Page'])),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'page_ariclecontent_set', to=orm['medialibrary.MediaFile'])),
        ))
        db.send_create_signal(u'page', ['AricleContent'])

        # Adding model 'FilteredPublicationContent'
        db.create_table(u'page_page_filteredpublicationcontent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('header', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('count', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='filteredpublicationcontent_set', to=orm['page.Page'])),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'page', ['FilteredPublicationContent'])

        # Adding model 'PeopleContent'
        db.create_table(u'page_page_peoplecontent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='peoplecontent_set', to=orm['page.Page'])),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'page', ['PeopleContent'])

        # Adding M2M table for field people on 'PeopleContent'
        m2m_table_name = db.shorten_name(u'page_page_peoplecontent_people')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('peoplecontent', models.ForeignKey(orm[u'page.peoplecontent'], null=False)),
            ('people', models.ForeignKey(orm[u'website.people'], null=False))
        ))
        db.create_unique(m2m_table_name, ['peoplecontent_id', 'people_id'])

        # Adding model 'ReportContent'
        db.create_table(u'page_page_reportcontent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('link_text', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='reportcontent_set', to=orm['page.Page'])),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'page', ['ReportContent'])


    def backwards(self, orm):
        # Deleting model 'Page'
        db.delete_table(u'page_page')

        # Deleting model 'ApplicationContent'
        db.delete_table(u'page_page_applicationcontent')

        # Deleting model 'StoryContent'
        db.delete_table(u'page_page_storycontent')

        # Deleting model 'CarouselContent'
        db.delete_table(u'page_page_carouselcontent')

        # Deleting model 'BannerContent'
        db.delete_table(u'page_page_bannercontent')

        # Deleting model 'QuoteContent'
        db.delete_table(u'page_page_quotecontent')

        # Deleting model 'RichTextContent'
        db.delete_table(u'page_page_richtextcontent')

        # Deleting model 'RelatedNewsContent'
        db.delete_table(u'page_page_relatednewscontent')

        # Removing M2M table for field newsitem_collection on 'RelatedNewsContent'
        db.delete_table(db.shorten_name(u'page_page_relatednewscontent_newsitem_collection'))

        # Deleting model 'LatestNewsContent'
        db.delete_table(u'page_page_latestnewscontent')

        # Deleting model 'UpcomingEventContent'
        db.delete_table(u'page_page_upcomingeventcontent')

        # Deleting model 'RelatedEventContent'
        db.delete_table(u'page_page_relatedeventcontent')

        # Removing M2M table for field event_collection on 'RelatedEventContent'
        db.delete_table(db.shorten_name(u'page_page_relatedeventcontent_event_collection'))

        # Deleting model 'FilteredEventContent'
        db.delete_table(u'page_page_filteredeventcontent')

        # Deleting model 'RelatedPublicationContent'
        db.delete_table(u'page_page_relatedpublicationcontent')

        # Removing M2M table for field publication_collection on 'RelatedPublicationContent'
        db.delete_table(db.shorten_name(u'page_page_relatedpublicationcontent_publication_collection'))

        # Deleting model 'LatestPublicationContent'
        db.delete_table(u'page_page_latestpublicationcontent')

        # Deleting model 'AricleContent'
        db.delete_table(u'page_page_ariclecontent')

        # Deleting model 'FilteredPublicationContent'
        db.delete_table(u'page_page_filteredpublicationcontent')

        # Deleting model 'PeopleContent'
        db.delete_table(u'page_page_peoplecontent')

        # Removing M2M table for field people on 'PeopleContent'
        db.delete_table(db.shorten_name(u'page_page_peoplecontent_people'))

        # Deleting model 'ReportContent'
        db.delete_table(u'page_page_reportcontent')


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
        u'page.applicationcontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'ApplicationContent', 'db_table': "u'page_page_applicationcontent'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parameters': ('feincms.contrib.fields.JSONField', [], {'null': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'applicationcontent_set'", 'to': u"orm['page.Page']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'urlconf_path': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'page.ariclecontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'AricleContent', 'db_table': "u'page_page_ariclecontent'"},
            'header': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'page_ariclecontent_set'", 'to': u"orm['medialibrary.MediaFile']"}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'link_text': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ariclecontent_set'", 'to': u"orm['page.Page']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'page.bannercontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'BannerContent', 'db_table': "u'page_page_bannercontent'"},
            'banner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'page_bannercontent_set'", 'to': u"orm['website.Banner']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bannercontent_set'", 'to': u"orm['page.Page']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'page.carouselcontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'CarouselContent', 'db_table': "u'page_page_carouselcontent'"},
            'header': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'page_carouselcontent_set'", 'to': u"orm['medialibrary.MediaFile']"}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'link_text': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'carouselcontent_set'", 'to': u"orm['page.Page']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sub_header': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'tab_text': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'page.filteredeventcontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'FilteredEventContent', 'db_table': "u'page_page_filteredeventcontent'"},
            'count': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'header': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'filteredeventcontent_set'", 'to': u"orm['page.Page']"}),
            'past_events': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'page.filteredpublicationcontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'FilteredPublicationContent', 'db_table': "u'page_page_filteredpublicationcontent'"},
            'count': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'header': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'filteredpublicationcontent_set'", 'to': u"orm['page.Page']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        u'page.latestnewscontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'LatestNewsContent', 'db_table': "u'page_page_latestnewscontent'"},
            'count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'header': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'latestnewscontent_set'", 'to': u"orm['page.Page']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'page.latestpublicationcontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'LatestPublicationContent', 'db_table': "u'page_page_latestpublicationcontent'"},
            'count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'header': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'latestpublicationcontent_set'", 'to': u"orm['page.Page']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'page.page': {
            'Meta': {'ordering': "['tree_id', 'lft']", 'object_name': 'Page'},
            '_cached_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'db_index': 'True', 'blank': 'True'}),
            '_content_title': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            '_page_title': ('django.db.models.fields.CharField', [], {'max_length': '69', 'blank': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_navigation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '10'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'meta_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'meta_keywords': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'modification_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'navigation_extension': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'override_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['page.Page']"}),
            'partner_login': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'publication_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 12, 21, 0, 0)'}),
            'publication_end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'redirect_to': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'}),
            'template_key': ('django.db.models.fields.CharField', [], {'default': "'homepage.html'", 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'translation_of': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'translations'", 'null': 'True', 'to': u"orm['page.Page']"}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'page.peoplecontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'PeopleContent', 'db_table': "u'page_page_peoplecontent'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'peoplecontent_set'", 'to': u"orm['page.Page']"}),
            'people': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'page_peoplecontent_set'", 'symmetrical': 'False', 'to': u"orm['website.People']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'page.quotecontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'QuoteContent', 'db_table': "u'page_page_quotecontent'"},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'quotecontent_set'", 'to': u"orm['page.Page']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'page.relatedeventcontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'RelatedEventContent', 'db_table': "u'page_page_relatedeventcontent'"},
            'event_collection': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'page_relatedeventcontent_set'", 'symmetrical': 'False', 'to': u"orm['website.Event']"}),
            'header': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relatedeventcontent_set'", 'to': u"orm['page.Page']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'page.relatednewscontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'RelatedNewsContent', 'db_table': "u'page_page_relatednewscontent'"},
            'header': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'newsitem_collection': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'page_relatednewscontent_set'", 'symmetrical': 'False', 'to': u"orm['website.NewsItem']"}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relatednewscontent_set'", 'to': u"orm['page.Page']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'page.relatedpublicationcontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'RelatedPublicationContent', 'db_table': "u'page_page_relatedpublicationcontent'"},
            'header': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relatedpublicationcontent_set'", 'to': u"orm['page.Page']"}),
            'publication_collection': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'page_relatedpublicationcontent_set'", 'symmetrical': 'False', 'to': u"orm['website.Publication']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'page.reportcontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'ReportContent', 'db_table': "u'page_page_reportcontent'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'link_text': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reportcontent_set'", 'to': u"orm['page.Page']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'page.richtextcontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'RichTextContent', 'db_table': "u'page_page_richtextcontent'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'richtextcontent_set'", 'to': u"orm['page.Page']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('feincms.contrib.richtext.RichTextField', [], {'blank': 'True'})
        },
        u'page.storycontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'StoryContent', 'db_table': "u'page_page_storycontent'"},
            'header': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'page_storycontent_set'", 'to': u"orm['medialibrary.MediaFile']"}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'link_text': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'storycontent_set'", 'to': u"orm['page.Page']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sub_header': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'page.upcomingeventcontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'UpcomingEventContent', 'db_table': "u'page_page_upcomingeventcontent'"},
            'count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'header': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'upcomingeventcontent_set'", 'to': u"orm['page.Page']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
        }
    }

    complete_apps = ['page']