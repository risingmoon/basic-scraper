import unittest
from scraper import (fetch_search_results, read_search_results, parse_source,
                     extract_listings)
import bs4


class ScraperTest(unittest.TestCase):

    def test_fetch_search_results(self):
        #Tests empty search parameter
        with self.assertRaises(ValueError):
            fetch_search_results()
        html, encoding = fetch_search_results(
            minAsk=500, maxAsk=1000, bedrooms=2
        )
        self.assertIsInstance(html, str)
        self.assertIsInstance(encoding, str)

    def test_read_search_results(self):
        #Tests non-existing file exception
        with self.assertRaises(IOError):
            read_search_results('test.html')
        html, encoding = read_search_results()
        #Test returned instance type are both string
        self.assertIsInstance(html, str)
        self.assertIsInstance(encoding, str)

    def test_parse_source(self):
        html, encoding = read_search_results()
        #Test returned instance type is bs4.BeatifulSoup
        self.assertIsInstance(parse_source(html), bs4.BeautifulSoup)

    def test_extract_listings(self):
        html, encoding = read_search_results()
        doc = parse_source(html)
        #Test returned instance type is a list
        self.assertIsInstance(extract_listings(doc), list)

if __name__ == "__main__":
    unittest.main()
