import argparse
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from guarani_scraper.guarani_scraper.spiders.guarani_spider import GuaraniSpider


def main():
    """
    Main entry point for the Guarani scraper CLI.

    Parses command-line arguments and starts the crawler process
    to scrape Guarani words from websites listed in the provided CSV file.

    Command-line arguments:
        --csv: Path to a CSV file with columns: name,description,url
    """
    parser = argparse.ArgumentParser(
        description="Scraper de palabras en guarani de sitios web."
    )
    parser.add_argument(
        "--csv", required=True, help="Archivo csv con columnas: name,description,url"
    )

    args = parser.parse_args()

    process = CrawlerProcess(get_project_settings())
    process.crawl(GuaraniSpider, csv_file=args.csv)
    process.start()


if __name__ == "__main__":
    main()
