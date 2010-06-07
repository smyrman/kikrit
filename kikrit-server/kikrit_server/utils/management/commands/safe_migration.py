from optparse import make_option

from django import db
from django.core import management
from django.core.management.base import BaseCommand
from django import VERSION as DJANGO_VERSION

from south import migration
from south.models import MigrationHistory
from south.exceptions import NoMigrations
from south.management.commands import migrate

# TODO: I have writen a patch to South that implements the same functionallety
# as this wrapper command. If that patch is applied, this entire file can be
# completly removed.

class Command(BaseCommand):
	option_list = migrate.Command.option_list + (
		make_option('--autoskip-first', action='store_true', dest='autoskip',
			default=False,
			help='Automatically fake the first migration if there exist '
			'tables for the app in question in the db.'),
		make_option('--first-migration', action='store', type="string",
			dest='autoskip_target', default='0001',
			help='Specefy an alternative name to match for the first '
			'migration (affects the --autoskip-first option).'),
		)

	help = "A small wrapper to souths migrate command that supplies two extra "\
			"options: '--autoskip-first' and '--first-migration'."

	args = "[app] [migrationname|zero]"

	def handle(self, app=None, target=None, **options):

		# Preserve original argumets to use in the finall migrate command call:
		_app = app
		_target = target

		# GUARD: If not auto-skip, just call south's migrate command:
		if not options.get('autoskip', False):
			return management.call_command('migrate', _app, _target, **options)

		# DUPLICATE OF 'south.mannagement.commands.migrate':
		# if all_apps flag is set, shift app over to target
		if options.get('all_apps', False):
			target = app
			app = None

		# Migrate each app
		if app:
			try:
				apps = [migration.Migrations(app)]
			except NoMigrations:
				print "The app '%s' does not appear to use migrations." % app
				print "./manage.py migrate " + self.args
				return
		else:
			apps = list(migration.all_migrations())
		# END DUPE CODE

		# Prefore a fake first migration for all apps needing that:
		autoskip_first_migration(apps, **options)

		# Finally, preform the real migrations:
		management.call_command('migrate', _app, _target, **options)



def autoskip_first_migration(apps, **options):
	"""Find out for what apps the first migration should be skipped. Then issue
	a fake migration for those apps.

	"""
	autoskip_apps = []
	# Added Django 1.1 compatibility code:
	if DJANGO_VERSION[:3] >= (1, 2, 0):
		database = options.get('database', db.DEFAULT_DB_ALIAS)
		connection = connections[database]
	else:
		connection = db.connection

	# Get a list of installed tables:
	tables = connection.introspection.table_names()

	# Find apps where the first migration should be skiped.
	for app in apps:
		app_label = app.app_label()
		# GUARD: If there is migration history for this app, the first
		# migration should never be skiped:
		if MigrationHistory.objects.filter(app_name=app_label,
				applied__isnull=False).count() > 0:
			continue

		# If one of the app's models have a table in the  database, assume that
		# the first migration should be skipped for app:
		for model in db.models.get_models(db.models.get_app(app_label)):
			if model._meta.db_table in tables:
				# If integrated to south, you probably want to append app
				# instead of app_label :)
				autoskip_apps.append(app_label)
				break

	# Skip the first migration for these apps:
	options['fake'] = True
	fake_target = options.get('autoskip_target')
	for app_label in autoskip_apps:
		management.call_command('migrate', app_label, fake_target, **options)

	# Be obvious about what we did:
	if len(autoskip_apps) > 0:
		print "The first migration was faked for the following apps:"
		print '\n'.join(autoskip_apps)
