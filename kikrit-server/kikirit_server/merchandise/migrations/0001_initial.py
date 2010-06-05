# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

	def forwards(self, orm):

		# Adding model 'MerchandiseTag'
		db.create_table('merchandise_merchandisetag', (
			('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
			('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
			('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
		))
		db.send_create_signal('merchandise', ['MerchandiseTag'])

		# Adding model 'Merchandise'
		db.create_table('merchandise_merchandise', (
			('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
			('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
			('ordinary_price', self.gf('django.db.models.fields.PositiveIntegerField')()),
			('internal_price', self.gf('django.db.models.fields.PositiveIntegerField')()),
			('ean', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
		))
		db.send_create_signal('merchandise', ['Merchandise'])

		# Adding M2M table for field tags on 'Merchandise'
		db.create_table('merchandise_merchandise_tags', (
			('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
			('merchandise', models.ForeignKey(orm['merchandise.merchandise'], null=False)),
			('merchandisetag', models.ForeignKey(orm['merchandise.merchandisetag'], null=False))
		))
		# SQLite workaroundd for unique constrain:
		# TODO: This workaround can be removed if ticet #144 for South is
		# solved:
		if db.backend_name == 'sqlite3':
			db.create_index('merchandise_merchandise_tags', ['merchandise_id',
				'merchandisetag_id'], unique=True)
		else:
			db.create_unique('merchandise_merchandise_tags', ['merchandise_id',
				'merchandisetag_id'])

		# Adding model 'PurchasedItem'
		db.create_table('merchandise_purchaseditem', (
			('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
			('transaction', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.Transaction'])),
			('merchandise', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['merchandise.Merchandise'])),
			('price', self.gf('django.db.models.fields.PositiveIntegerField')()),
		))
		db.send_create_signal('merchandise', ['PurchasedItem'])


	def backwards(self, orm):

		# Deleting model 'MerchandiseTag'
		db.delete_table('merchandise_merchandisetag')

		# Deleting model 'Merchandise'
		db.delete_table('merchandise_merchandise')

		# Removing M2M table for field tags on 'Merchandise'
		db.delete_table('merchandise_merchandise_tags')

		# Deleting model 'PurchasedItem'
		db.delete_table('merchandise_purchaseditem')


	models = {
		'accounts.account': {
			'Meta': {'object_name': 'Account'},
			'balance': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
			'color': ('django.db.models.fields.SmallIntegerField', [], {}),
			'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'limit_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.LimitGroup']", 'null': 'True', 'blank': 'True'}),
			'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
			'phone_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
			'timestamp_grey': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
			'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
		},
		'accounts.limitgroup': {
			'Meta': {'object_name': 'LimitGroup'},
			'black_limit': ('django_kikrit.accounts.fields.NegativeIntegerField', [], {'default': '0'}),
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'internal_price': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
			'max_grey_hours': ('django.db.models.fields.SmallIntegerField', [], {'default': '24'}),
			'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
		},
		'accounts.transaction': {
			'Meta': {'object_name': 'Transaction'},
			'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Account']"}),
			'amount': ('django.db.models.fields.IntegerField', [], {}),
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'responsible': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
			'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
			'type': ('django.db.models.fields.IntegerField', [], {})
		},
		'auth.group': {
			'Meta': {'object_name': 'Group'},
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
			'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
		},
		'auth.permission': {
			'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
			'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
			'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
		},
		'auth.user': {
			'Meta': {'object_name': 'User'},
			'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
			'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
			'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
			'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
			'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
			'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
			'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
			'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
			'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
			'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
			'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
		},
		'contenttypes.contenttype': {
			'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
			'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
			'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
		},
		'merchandise.merchandise': {
			'Meta': {'object_name': 'Merchandise'},
			'ean': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'internal_price': ('django.db.models.fields.PositiveIntegerField', [], {}),
			'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
			'ordinary_price': ('django.db.models.fields.PositiveIntegerField', [], {}),
			'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['merchandise.MerchandiseTag']", 'null': 'True', 'blank': 'True'})
		},
		'merchandise.merchandisetag': {
			'Meta': {'object_name': 'MerchandiseTag'},
			'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
		},
		'merchandise.purchaseditem': {
			'Meta': {'object_name': 'PurchasedItem'},
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'merchandise': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['merchandise.Merchandise']"}),
			'price': ('django.db.models.fields.PositiveIntegerField', [], {}),
			'transaction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Transaction']"})
		}
	}

	complete_apps = ['merchandise']
