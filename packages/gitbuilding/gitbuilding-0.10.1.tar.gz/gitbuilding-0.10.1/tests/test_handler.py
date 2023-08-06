import unittest
import logging
from gitbuilding.handler import GBHandler

_LOGGER = logging.getLogger('BuildUp.GitBuilding')

class UtilitiesTestCase(unittest.TestCase):

    def setUp(self):
        self.handler = GBHandler(silent=True)
        logger = logging.getLogger('BuildUp')
        logger.setLevel(logging.INFO)
        logger.addHandler(self.handler)

    def test_warning(self):
        _LOGGER.warning("This is a warning test.")
        self.assertEqual(self.handler.log_length, 1)
        first_record = self.handler.log_from(0)[0]
        self.assertFalse(first_record['fussy'])

    def test_fussy_warning(self):
        _LOGGER.warning("This is a warning test.",
                        extra={'fussy':True})
        self.assertEqual(self.handler.log_length, 1)
        first_record = self.handler.log_from(0)[0]
        self.assertTrue(first_record['fussy'])
    
    def test_info(self):
        _LOGGER.info("This is an info message")
        self.assertEqual(self.handler.log_length, 0)

    def test_active_page(self):
        _LOGGER.warning("This is a warning test.")
        _LOGGER.info('Changing page', extra={'set_active_page': 'page.md'})
        _LOGGER.warning("This is a warning test.")
        _LOGGER.info('Some other information, no page change')
        _LOGGER.warning("This is a warning test.")
        _LOGGER.info('Changing page', extra={'set_active_page': None})
        _LOGGER.warning("This is a warning test.")
        self.assertEqual(self.handler.log_length, 4)
        records = self.handler.log_from(0)
        self.assertIsNone(records[0]['active_page'])
        self.assertEqual(records[1]['active_page'], 'page.md')
        self.assertEqual(records[2]['active_page'], 'page.md')
        self.assertIsNone(records[3]['active_page'])