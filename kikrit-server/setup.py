#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from distutils2.core import setup
from kikrit_server import get_version

def recursive_listdir(package, cur_dir):
	"""Recursivly list the files of a directory"""
	files=[]
	all_files = os.listdir(os.path.join(package, cur_dir))
	for entry in all_files:
		fname = os.path.join(cur_dir, entry)
		if os.path.isdir(os.path.join(package,fname)):
			files += recursive_listdir(package, fname)
		else:
			files.append(fname)
	return files


setup(name='kikrit-server',
      version=get_version(short=True),
      author='Sindre Røkenes Myren',
      author_email='smyrman@gmail.com',
      home_page='http://github.com/smyrman/kikrit',
      summary='A credit system created for student bars (server)',
      description=open('README.rst').read(),
      keywords=['credit', 'merchandise', 'bar', 'kikrit'],
      license='GPLv3',
      platforms='Linux',
      requires=['Django>=1.2.3', 'South>=0.7.1', 'PIL'],
      packages=['kikrit_server'],
      package_data={'kikrit_server':
          recursive_listdir('kikrit_server','media') +
          recursive_listdir('kikrit_server','templates') +
          recursive_listdir('kikrit_server','accounts/fixtures') +
          recursive_listdir('kikrit_server','merchandise/fixtures')
          },
      scripts=['scripts/kikrit-admin'],
      )
