Basic Scraper
=============
[![Build Status](https://travis-ci.org/risingmoon/basic-scraper.png?branch=master)](https://travis-ci.org/risingmoon/basic-scraper)

In this project, "scraper.py" uses Python to scrape apartmental listings from Seattle [Craigslist] (http://seattle.craigslist.org/search/apa).

If no arguments are given:

    $ python scraper.py

The program makes a request with default parameters for price between 500 and 1000 for 2 bedrooms, saves it as default file "apartment.html", and prints out location, link, description, size, and price data.

If typed:

    $ python scraper.py test
  
The program instead reads from existing "apartmental.html" if it exists, and parses the results under the assumption of 'utf-8' encoding. See NOTE[1]


NOTE[1]: It's assumed that html pages are utf-8 encoded. Approximately over half of world wide web uses utf-8 standad.

See source: http://en.wikipedia.org/wiki/UTF-8

