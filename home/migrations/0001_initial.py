# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Menu'
        db.create_table(u'home_menu', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'home', ['Menu'])

        # Adding model 'MenuItem'
        db.create_table(u'home_menuitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('new_page', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'home', ['MenuItem'])

        # Adding M2M table for field menus on 'MenuItem'
        m2m_table_name = db.shorten_name(u'home_menuitem_menus')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('menuitem', models.ForeignKey(orm[u'home.menuitem'], null=False)),
            ('menu', models.ForeignKey(orm[u'home.menu'], null=False))
        ))
        db.create_unique(m2m_table_name, ['menuitem_id', 'menu_id'])

        # Adding model 'SliderItem'
        db.create_table(u'home_slideritem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('new_page', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('img_height', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('img_width', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'home', ['SliderItem'])

        # Adding model 'Widget'
        db.create_table(u'home_widget', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('contents', self.gf('django.db.models.fields.TextField')(max_length=1000)),
        ))
        db.send_create_signal(u'home', ['Widget'])


    def backwards(self, orm):
        # Deleting model 'Menu'
        db.delete_table(u'home_menu')

        # Deleting model 'MenuItem'
        db.delete_table(u'home_menuitem')

        # Removing M2M table for field menus on 'MenuItem'
        db.delete_table(db.shorten_name(u'home_menuitem_menus'))

        # Deleting model 'SliderItem'
        db.delete_table(u'home_slideritem')

        # Deleting model 'Widget'
        db.delete_table(u'home_widget')


    models = {
        u'home.menu': {
            'Meta': {'object_name': 'Menu'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'home.menuitem': {
            'Meta': {'object_name': 'MenuItem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'menus': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'menuitems'", 'symmetrical': 'False', 'to': u"orm['home.Menu']"}),
            'new_page': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'home.slideritem': {
            'Meta': {'object_name': 'SliderItem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'img_height': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'img_width': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'new_page': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'home.widget': {
            'Meta': {'object_name': 'Widget'},
            'contents': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['home']