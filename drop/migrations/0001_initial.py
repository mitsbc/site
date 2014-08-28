# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DropEvent'
        db.create_table(u'drop_dropevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'drop', ['DropEvent'])

        # Adding model 'Resume'
        db.create_table(u'drop_resume', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=200)),
            ('year', self.gf('django.db.models.fields.IntegerField')(default=2018, max_length=4)),
            ('resume', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('industry', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1)),
            ('unique_hash', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'drop', ['Resume'])

        # Adding model 'ResumeBook'
        db.create_table(u'drop_resumebook', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')(default=2018, max_length=4)),
            ('industry', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1)),
            ('book', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'drop', ['ResumeBook'])

        # Adding model 'Company'
        db.create_table(u'drop_company', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('contact_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('contact_email', self.gf('django.db.models.fields.EmailField')(max_length=100, null=True, blank=True)),
            ('industry', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1)),
            ('unique_hash', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'drop', ['Company'])


    def backwards(self, orm):
        # Deleting model 'DropEvent'
        db.delete_table(u'drop_dropevent')

        # Deleting model 'Resume'
        db.delete_table(u'drop_resume')

        # Deleting model 'ResumeBook'
        db.delete_table(u'drop_resumebook')

        # Deleting model 'Company'
        db.delete_table(u'drop_company')


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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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