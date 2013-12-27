# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Resume._type'
        db.delete_column(u'ine_resume', '_type')

        # Deleting field 'Resume._hash'
        db.delete_column(u'ine_resume', '_hash')

        # Adding field 'Resume.industry'
        db.add_column(u'ine_resume', 'industry',
                      self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1),
                      keep_default=False)

        # Adding field 'Resume.unique_hash'
        db.add_column(u'ine_resume', 'unique_hash',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)

        # Deleting field 'ResumeBook._type'
        db.delete_column(u'ine_resumebook', '_type')

        # Adding field 'ResumeBook.industry'
        db.add_column(u'ine_resumebook', 'industry',
                      self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1),
                      keep_default=False)

        # Deleting field 'Company._type'
        db.delete_column(u'ine_company', '_type')

        # Deleting field 'Company._hash'
        db.delete_column(u'ine_company', '_hash')

        # Adding field 'Company.industry'
        db.add_column(u'ine_company', 'industry',
                      self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1),
                      keep_default=False)

        # Adding field 'Company.unique_hash'
        db.add_column(u'ine_company', 'unique_hash',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Resume._type'
        db.add_column(u'ine_resume', '_type',
                      self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1),
                      keep_default=False)

        # Adding field 'Resume._hash'
        db.add_column(u'ine_resume', '_hash',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)

        # Deleting field 'Resume.industry'
        db.delete_column(u'ine_resume', 'industry')

        # Deleting field 'Resume.unique_hash'
        db.delete_column(u'ine_resume', 'unique_hash')

        # Adding field 'ResumeBook._type'
        db.add_column(u'ine_resumebook', '_type',
                      self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1),
                      keep_default=False)

        # Deleting field 'ResumeBook.industry'
        db.delete_column(u'ine_resumebook', 'industry')

        # Adding field 'Company._type'
        db.add_column(u'ine_company', '_type',
                      self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1),
                      keep_default=False)

        # Adding field 'Company._hash'
        db.add_column(u'ine_company', '_hash',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)

        # Deleting field 'Company.industry'
        db.delete_column(u'ine_company', 'industry')

        # Deleting field 'Company.unique_hash'
        db.delete_column(u'ine_company', 'unique_hash')


    models = {
        u'ine.company': {
            'Meta': {'object_name': 'Company'},
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'unique_hash': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'ine.resume': {
            'Meta': {'object_name': 'Resume'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'resume': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'unique_hash': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '2017', 'max_length': '4'})
        },
        u'ine.resumebook': {
            'Meta': {'object_name': 'ResumeBook'},
            'book': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '2017', 'max_length': '4'})
        }
    }

    complete_apps = ['ine']