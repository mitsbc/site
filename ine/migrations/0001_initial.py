# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Resume'
        db.create_table(u'ine_resume', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=200)),
            ('year', self.gf('django.db.models.fields.IntegerField')(default=2016, max_length=4)),
            ('resume', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'ine', ['Resume'])

        # Adding model 'ResumeBook'
        db.create_table(u'ine_resumebook', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')(default=2016, max_length=4)),
            ('_type', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=1)),
            ('book', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'ine', ['ResumeBook'])

        # Adding model 'Company'
        db.create_table(u'ine_company', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('contact_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('contact_email', self.gf('django.db.models.fields.EmailField')(max_length=100, null=True, blank=True)),
            ('_type', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=1)),
        ))
        db.send_create_signal(u'ine', ['Company'])


    def backwards(self, orm):
        # Deleting model 'Resume'
        db.delete_table(u'ine_resume')

        # Deleting model 'ResumeBook'
        db.delete_table(u'ine_resumebook')

        # Deleting model 'Company'
        db.delete_table(u'ine_company')


    models = {
        u'ine.company': {
            'Meta': {'object_name': 'Company'},
            '_type': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '1'}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'ine.resume': {
            'Meta': {'object_name': 'Resume'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'resume': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '2016', 'max_length': '4'})
        },
        u'ine.resumebook': {
            'Meta': {'object_name': 'ResumeBook'},
            '_type': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '1'}),
            'book': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '2016', 'max_length': '4'})
        }
    }

    complete_apps = ['ine']