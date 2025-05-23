import csv
from urllib.parse import urlparse
# import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..utils.lang_detector import GuaraniDetector
from ..items import GuaraniWord

class GuaraniSpider(CrawlSpider):
    name = "guarani"
    
    def __init__(self, csv_file=None, *args, **kwargs):
        super(GuaraniSpider, self).__init__(*args, **kwargs)
        self.detector = GuaraniDetector()
        
        # Read URLs from CSV
        if csv_file:
            with open(csv_file) as f:
                reader = csv.DictReader(f)
                self.start_urls = [row['url'] for row in reader]
                
        # Configure rules
        self.rules = (
            Rule(
                LinkExtractor(),
                callback='parse_item',
                follow=True
            ),
        )
        
        super()._compile_rules()
    
    def parse_item(self, response):
        # Extract all text 
        words = response.xpath('//text()').getall()
        
        for word in words:
            word = word.strip()
            if word and self.detector.is_guarani(word):
                yield GuaraniWord(
                    word=word,
                    url=response.url,
                    domain=urlparse(response.url).netloc
                )