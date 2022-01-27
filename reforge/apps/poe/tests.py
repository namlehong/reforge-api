import os

from django.test import TestCase

from . import parsers


# Create your tests here.
class ParserTest(TestCase):
    HTML_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'html')

    def get_html(self, filename):
        return os.path.join(self.HTML_DIR, filename)

    def test_harvest_craft_parser(self):
        with open(self.get_html('harvest_craft.html'), 'r', encoding="utf8") as f:
            html = f.read()

            harvest_craft = parsers.harvest_craft_poe_db_parser(html)
            # TODO write more detail test
            self.assertEqual(harvest_craft[0].get('description'),
                             'Reforge a Normal, Magic or Rare item as a Rare item with random modifiers, including a Caster modifier')
