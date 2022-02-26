"""Module covering the test suite to make sure your catalog is set up properly.

.. include:: ../../gh_pages/test_suite.md
"""
from . import catalog_tests
from . import column_store_tests
from . import description_tests


__all__ = [
    'catalog_tests',
    'column_store_tests',
    'description_tests'
]
