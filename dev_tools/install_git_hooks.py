#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren, Andreas Hopland Sperre
#
# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.

"""Copy all hooks from dev_tools/git_hooks/ to .git/hooks/

"""

import os

PROJECT_ROOT = os.path.abspath(__file__).rsplit(os.path.sep, 2)[0]

def main():
	# Run Django database tests for our apps:
	os.chdir(PROJECT_ROOT)
	return os.system("cp dev_tools/git_hooks/* .git/hooks/.")


if __name__ == "__main__":
	exit(main())
