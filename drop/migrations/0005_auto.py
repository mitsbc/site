# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field events on 'ResumeBook'
        m2m_table_name = db.shorten_name(u'drop_resumebook_events')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('resumebook', models.ForeignKey(orm[u'drop.resumebook'], null=False)),
            ('dropevent', models.ForeignKey(orm[u'drop.dropevent'], null=False))
        ))
        db.create_unique(m2m_table_name, ['resumebook_id', 'dropevent_id'])


    def backwards(self, orm):
        # Removing M2M table for field events on 'ResumeBook'
        db.delete_table(db.shorten_name(u'drop_resumebook_events'))


    models = {
        u'drop.company': {
            'Meta': {'object_name': 'Company'},
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'unique_hash': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'drop.dropevent': {
            'Meta': {'object_name': 'DropEvent'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'})
        },
        u'drop.resume': {
            'Meta': {'object_name': 'Resume'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '200'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['drop.DropEvent']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'resume': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'unique_hash': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '2018', 'max_length': '4'})
        },
        u'drop.resumebook': {
            'Meta': {'object_name': 'ResumeBook'},
            'book': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['drop.DropEvent']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '2018', 'max_length': '4'})
        }
    }

    complete_apps = ['drop']