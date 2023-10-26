from datetime import datetime

import scrapy
from scrapy.http import Request

from maksavit_scrapy.items import ScrapyMaksavitItem
from maksavit_scrapy.settings import (CATEGORIES, DOMAIN, LOCATION, MAIN_URL,
                                      PROXY)


class MaksavitSpider(scrapy.Spider):
    name = 'maksavit'
    page = 1
    allowed_domains = [DOMAIN]
    start_urls = []

    def start_requests(self):
        for category in CATEGORIES:
            self.start_urls.append(f'{MAIN_URL}{category}?location={LOCATION}')

        for url in self.start_urls:
            yield Request(url, dont_filter=True, meta=PROXY)

    def parse(self, response):
        print(response.request.url)
        max_page = int(
            response.css(
                'div.app-filter__pagination a::text').getall()[-1].strip()
        )

        for product in response.css('div.product-card-block'):
            link = product.css('a.product-card-block__title::attr(href)').get()
            yield response.follow(link, callback=self.parse_item)
        current_page = int(
            response.css('a.ui-pagination__item_checked::text').get().strip()
        )
        next_page = current_page + 1

        if current_page < max_page:
            url = f'{response.request.url}'.replace(
                f'&page={current_page}', '')
            yield response.follow(
                f'{url}&page={next_page}', callback=self.parse
            )

    def parse_item(self, response):
        timestamp = int(datetime.timestamp(datetime.now()))
        code = response.request.url.split('/')[-2]
        url = response.request.url
        title = response.css('h1.product-top__title::text').get()
        badge = response.css('div.badge-discount::text').get()
        badges = [badge.strip()] if badge is not None else badge
        production = response.css('a.product-info__brand-value::text').get()
        brand = (None if production is None else ', '.join(
            production.strip().split(', ')[:-1]))
        country = (
            None if production is None else production.strip().split(', ')[-1]
        )
        sections = response.css(
            'ul.breadcrumbs li a.breadcrumbs__link span::text').getall()

        current_price = response.css('div.price-info__price span::text').get()
        current_price = (
            float(current_price.split(' ')[0])
            if current_price is not None else None)

        original_price = response.css('div.price-box__old-price::text').get()
        original_price = (current_price if original_price is None else float(
            original_price.replace('\xa0₽', '').replace(' ', '').strip()))

        discount = (((original_price - current_price) / original_price)
                    * 100 if current_price != original_price else 0)
        sale_tag = f'Скидка {discount:.0f}%' if discount != 0 else None

        status = response.css('div.available-count ::text').get()
        status = None if status is None else status[:-1]
        in_stock = True if status == 'сегодня' else False
        count = None

        img = response.css('div.product-picture img::attr(src)').get()
        main_img = response.urljoin(img) if img != '' else None
        set_img = [response.urljoin(img) if img != '' else None
                   for img in response.css(
            'div.product-picture img::attr(src)').getall()]

        # На сайте не представлено ни одного фото360/видео.
        # Т.к. в ТЗ эти элементы перечислены обязательными,
        # добавил round_view и video для демонстрации их поиска
        round_view = (
            response.css('div.product-picture')
            .xpath('//img[contains(@src, "360view")]/@src')
            .getall()
        )
        video = (
            response.css('div.product-picture')
            .xpath('//img[contains(@src, "video")]/@src')
            .getall()
        )

        info = response.css('div.product-instruction__guide')

        description = info.css('div.ph23 ::text').getall()
        description = (
            ''.join(description).replace('Описание', '')
            if description
            else None
        )

        form = info.css('div.ph14 ::text').getall()
        form = ''.join(form).replace('Форма выпуска', '') if form else None

        exp = info.css('div.ph17 ::text').getall()
        exp = ''.join(exp).replace('Срок годности', '') if exp else None

        quanity = response.css(
            'div.quantity-items-wrapper span::text').getall()
        quanity = len(quanity) if quanity else 1

        price = {
            'current': current_price,
            'original': original_price,
            'sale_tag': sale_tag,
        }
        assets = {
            'main_image': main_img,
            'set_images': set_img,
            'view360': round_view,
            'video': video,
        }
        stock = {'in_stock': in_stock, 'count': count}
        metadata = {
            'description': description,
            'code': code,
            'form': form,
            'exp': exp,
            'production': brand,
            'country': country,
        }
        data = {
            'timestamp': timestamp,
            'RPC': code,
            'url': url,
            'title': title,
            'marketing_tags': badges,
            'brand': brand,
            'section': sections,
            'price': price,
            'stock': stock,
            'assets': assets,
            'metadata': metadata,
            'variants': quanity,
        }
        yield ScrapyMaksavitItem(data)
