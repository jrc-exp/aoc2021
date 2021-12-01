""" Developed by Ryan Crawford not for the U.S. Government. Copyright 2021 Ryan Crawford. Unlimited Copy and Paste Rights. """

# Every distribution that uses the namespace package must include an identical __init__.py.
# If any distribution does not, it will cause the namespace logic to fail and the other
# sub-packages will not be importable. Any additional code in __init__.py will be inaccessible.
# Follow the link for more details.
# https://packaging.python.org/guides/packaging-namespace-packages/#pkgutil-style-namespace-packages
__path__ = __import__('pkgutil').extend_path(__path__, __name__)

