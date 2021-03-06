import unittest
import pep8
import logging
import os

from pyramid import testing

logging.basicConfig()
log = logging.getLogger(__file__)
here = os.path.dirname(os.path.abspath(__file__))


class MotmomFunctionalTests(unittest.TestCase):
    def setUp(self):
        from motmom import main
        app = main({})
        from webtest import TestApp

        self.testapp = TestApp(app)

    def test_home_page(self):
        res = self.testapp.get('/', status=200)
        self.assertIn(b'Pyramid Motmom', res.body)


class TestCodeFormat(unittest.TestCase):
    def test_pep8_conformance(self):
        log.warning('PEP8 Test')
        pep8style = pep8.StyleGuide()
        result = pep8style.check_files(['motmom/subscribers.py',
                                        'motmom/views.py',
                                        'motmom/security.py',
                                        'motmom/service.py',
                                        'motmom/__init__.py',
                                        'motmom/tests.py'])
        self.assertEqual(result.total_errors, 0,
                         'Found code style errors (and warnings).')
