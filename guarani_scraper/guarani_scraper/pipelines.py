# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
from urllib.parse import urlparse  
from itemadapter import ItemAdapter


class GuaraniScraperPipeline:
    
    def __init__(self):
        self.files = {}
        os.makedirs("../../corpus", exist_ok=True)
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        domain = adapter["domain"]
        
        if domain not in self.files:
            self.files[domain] = open(f"corpus/{domain}.txt", "w", encoding="utf-8")
            
        self.files[domain].write(f"{adapter['word']}\n")
        return item
    
    def close_spider(self, spider):
        for file in self.files.values():
            file.close()
            
