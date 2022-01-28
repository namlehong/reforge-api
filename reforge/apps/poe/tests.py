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

            harvest_craft = list(parsers.harvest_craft_poe_db_parser(html))

            # test structure of output data
            self.assertEqual(harvest_craft[0].get('tier'), 1)
            self.assertEqual(harvest_craft[0].get('description'), 'Reforge a Normal, Magic or Rare item as a Rare item with random modifiers, including a Caster modifier')
            self.assertEqual(harvest_craft[0].get('seed_name'), 'Wild Ursaling')
            self.assertListEqual(harvest_craft[0].get('keywords'), [['Reforge', 'Caster']])

            # test number of craft
            self.assertEqual(len(harvest_craft), 242)

    def test_bench_craft_parser(self):
        with open(self.get_html('bench_craft.html'), 'r', encoding="utf8") as f:
            html = f.read()

            bench_craft = list(parsers.bench_craft_poe_db_parser(html))
            # test structure of output data
            self.assertEqual(bench_craft[0].get('mod'), 'Two Sockets')
            self.assertListEqual(bench_craft[0].get('cost'), ["Jeweller's Orb", '1'])
            self.assertListEqual(bench_craft[0].get('item_types'), ['One Hand Melee', 'Two Hand Melee','One Hand Ranged', 'Two Hand Ranged', 'Body Armour', 'Gloves', 'Boots', 'Helmet', 'Shield'])
            self.assertEqual(bench_craft[0].get('unlock'), 'Reef Map')


            # test number of craft
            self.assertEqual(len(bench_craft), 797)
