# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

	def forwards(self, orm):

		# Adding model 'LimitGroup'
		db.create_table('accounts_limitgroup', (
			('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
			('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
			('black_limit', self.gf('kikrit_server.accounts.fields.NegativeIntegerField')(default=0)),
			('max_grey_hours', self.gf('django.db.models.fields.SmallIntegerField')(default=24)),
			('internal_price', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
		))
		db.send_create_signal('accounts', ['LimitGroup'])

		# Adding model 'Account'
		db.create_table('accounts_account', (
			('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
			('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, null=True, blank=True)),
			('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
			('balance', self.gf('django.db.models.fields.IntegerField')(default=0)),
			('limit_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.LimitGroup'], null=True, blank=True)),
			('color', self.gf('django.db.models.fields.SmallIntegerField')()),
			('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
			('phone_number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
			('timestamp_grey', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
		))
		db.send_create_signal('accounts', ['Account'])

		# Adding model 'BalanceImage'
		db.create_table('accounts_balanceimage', (
			('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
			('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
			('minimum_balance', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
			('maximum_balance', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
			('white', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
			('grey', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
			('black', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
		))
		db.send_create_signal('accounts', ['BalanceImage'])

		# Adding model 'RFIDCard'
		db.create_table('accounts_rfidcard', (
			('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
			('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.Account'])),
			('rfid_string', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
		))
		db.send_create_signal('accounts', ['RFIDCard'])

		# Adding model 'Transaction'
		db.create_table('accounts_transaction', (
			('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
			('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
			('responsible', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
			('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.Account'])),
			('amount', self.gf('django.db.models.fields.IntegerField')()),
			('type', self.gf('django.db.models.fields.IntegerField')()),
		))
		db.send_create_signal('accounts', ['Transaction'])


	def backwards(self, orm):

		# Deleting model 'LimitGroup'
		db.delete_table('accounts_limitgroup')

		# Deleting model 'Account'
		db.delete_table('accounts_account')

		# Deleting model 'BalanceImage'
		db.delete_table('accounts_balanceimage')

		# Deleting model 'RFIDCard'
		db.delete_table('accounts_rfidcard')

		# Deleting model 'Transaction'
		db.delete_table('accounts_transaction')


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
		'accounts.balanceimage': {
			'Meta': {'object_name': 'BalanceImage'},
			'black': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
			'grey': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
			'maximum_balance': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
			'minimum_balance': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
			'white': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
		},
		'accounts.limitgroup': {
			'Meta': {'object_name': 'LimitGroup'},
			'black_limit': ('kikrit_server.accounts.fields.NegativeIntegerField', [], {'default': '0'}),
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'internal_price': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
			'max_grey_hours': ('django.db.models.fields.SmallIntegerField', [], {'default': '24'}),
			'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
		},
		'accounts.rfidcard': {
			'Meta': {'object_name': 'RFIDCard'},
			'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Account']"}),
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'rfid_string': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
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
		}
	}

	complete_apps = ['accounts']
