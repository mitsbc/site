# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'DropEvent.slug'
        db.add_column(u'drop_dropevent', 'slug',
                      self.gf('django.db.models.fields.SlugField')(default='ine', max_length=100),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'DropEvent.slug'
        db.delete_column(u'drop_dropevent', 'slug')


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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'})
        },
        u'drop.resume': {
            'Meta': {'object_name': 'Resume'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'resume': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'unique_hash': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '2018', 'max_length': '4'})
        },
        u'drop.resumebook': {
            'Meta': {'object_name': 'ResumeBook'},
            'book': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '2018', 'max_length': '4'})
        }
    }

    complete_apps = ['drop']