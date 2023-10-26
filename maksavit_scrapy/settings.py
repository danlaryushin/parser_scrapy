from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
RESULTS_DIR = 'catalog'
DOMAIN = 'maksavit.ru'
MAIN_URL = 'https://maksavit.ru/novosibirsk/catalog/'
LOCATION = '0000949228'
CATEGORIES = [
    'materinstvo_i_detstvo/detskaya_gigiena/',
    'allergologiya/protivoallergicheskie/',
    'dietologiya/sportivnoe_pitanie/',
]
PROXY = None
# Для бесплатных {'proxy': 'http://ip:port'}
# Для персональных {'proxy': 'http://ip:port:user:password'}

LOG_LEVEL = 'INFO'

BOT_NAME = "maksavit_scrapy"

SPIDER_MODULES = ["maksavit_scrapy.spiders"]
NEWSPIDER_MODULE = "maksavit_scrapy.spiders"

ROBOTSTXT_OBEY = True

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# fmt: off
FEEDS = {
    BASE_DIR / RESULTS_DIR / 'catalog.json': {
        'format': 'json',
        'fields': [
            'timestamp',
            'RPC',
            'url',
            'title',
            'marketing_tags',
            'brand',
            'section',
            'price',
            'stock',
            'assets',
            'metadata',
            'variants',
        ],
        'overwrite': True,
    },
}
