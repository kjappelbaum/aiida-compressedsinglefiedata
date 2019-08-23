""" Helper functions and classes for tests
"""
from __future__ import absolute_import
import os
from aiida.manage.fixtures import PluginTestCase

__all__ = ('PluginTestCase', 'get_backend')

TEST_DIR = os.path.dirname(os.path.realpath(__file__))


def get_backend():
    from aiida.backends.profile import BACKEND_DJANGO, BACKEND_SQLA
    if os.environ.get('TEST_AIIDA_BACKEND') == BACKEND_SQLA:
        return BACKEND_SQLA
    return BACKEND_DJANGO
