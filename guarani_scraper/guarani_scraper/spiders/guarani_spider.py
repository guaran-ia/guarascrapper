import csv
from urllib.parse import urlparse

# import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..utils.lang_detector import GuaraniDetector
from ..items import GuaraniWord


class GuaraniSpider(CrawlSpider):
    """
    Spider for crawling websites and extracting Guarani words.

    This spider crawls websites specified in a CSV file and extracts
    text content that is detected as being in the Guarani language.
    """

    name = "guarani"

    def __init__(self, csv_file=None, *args, **kwargs):
        """
        Initialize the GuaraniSpider with a CSV file containing URLs to crawl.

        Args:
            csv_file (str): Path to CSV file with URLs to crawl
            *args, **kwargs: Additional arguments passed to CrawlSpider
        """
        super(GuaraniSpider, self).__init__(*args, **kwargs)
        self.detector = GuaraniDetector()

        # Read URLs from CSV
        if csv_file:
            with open(csv_file) as f:
                reader = csv.DictReader(f)
                self.start_urls = [row["url"] for row in reader]

        # Configure rules
        self.rules = (Rule(LinkExtractor(), callback="parse_item", follow=True),)

        super()._compile_rules()

    def parse_item(self, response):
        """
        Parse a web page and extract Guarani words.

        Extracts all visible text from the page by selecting text from
        paragraphs, headings, links, and other content elements. The text
        is then cleaned, normalized, and split into individual words.
        Each word is checked to determine if it's Guarani using the
        GuaraniDetector, and if identified as Guarani, it's yielded
        as a GuaraniWord item.

        Args:
            response (scrapy.http.Response): The HTTP response object
                containing the web page content

        Yields:
            GuaraniWord: Items containing Guarani words along with metadata
                         such as the source URL and domain
        """
        # Extract all text
        text = " ".join(response.xpath("//text()").getall())
        words = [w.strip() for w in text.split() if w.strip()]

        batch_size = 100
        for i in range(0, len(words), batch_size):
            batch = words[i : i + batch_size]
            for word in batch:
                if self.detector.is_guarani(word):
                    yield GuaraniWord(
                        word=word,
                        url=response.url,
                        domain=urlparse(response.url).netloc,
                    )
