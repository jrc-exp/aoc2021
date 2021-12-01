""" Developed by Ryan Crawford not for the U.S. Government. Copyright 2021 Ryan Crawford. Unlimited Copy and Paste Rights. """

import setuptools
import site
import sys

# Allow editable install into user site directory.
# See https://github.com/pypa/pip/issues/7953.
site.ENABLE_USER_SITE = '--user' in sys.argv[1:]

# needed for editable installs with pip and setup.cfg for now:
# https://packaging.python.org/tutorials/packaging-projects/
setuptools.setup()
