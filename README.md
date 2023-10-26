![python](https://img.shields.io/badge/python-222324?style=for-the-badge&logo=python&logoColor=yellow)
![scrapy](https://img.shields.io/badge/scrapy-222324?style=for-the-badge&logo=searxng&logoColor=brown)
# maksavit_scrapy
Парсер товаров с сайта maksavit.ru реализован с помощью фреймворка Scrapy.

Реализовано получение информации о товарах интернет-магазина из списка категорий по заранее заданному шаблону.
Информация предоставляется в виде списка словарей и сохраняется JSON файл.
Также есть возможность запустить парсер с использованием [proxy](https://github.com/danlaryushin/maksavit_scrapy#%D0%BF%D1%80%D0%BE%D0%BA%D1%81%D0%B8).
```
{
   "timestamp": int,  # Дата и время сбора товара в формате timestamp.
   "RPC": "str",  # Уникальный код товара.
   "url": "str",  # Ссылка на страницу товара.
   "title": "str",  # Название товара.
   "marketing_tags": ["str"],  # Список маркетинговых тэгов.
   "brand": "str",  # Бренд товара.
   "section": ["str"],  # Иерархия разделов.
   "price_data": {
        "current": float,  # Цена со скидкой.
        "original": float,  # Оригинальная цена.
        "sale_tag": "str"  # Скидка.
    },
   "stock": {
        "in_stock": bool,  # Наличие товара.
        "count": int  # Количество.
    },
   "assets": {
        "main_image": "str",  # Ссылка на основное изображение товара.
        "set_images": ["str"],  # Список ссылок на все изображения товара.
        "view360": ["str"],  # Список ссылок на изображения в формате 360.
        "video": ["str"]  # Список ссылок на видео/видеообложки товара.
    },
   "metadata": {
        "description": "str",  # Описание товара.
        "code": "str", # Код товара.
        "form": "str", # Форма выпуска.
        "exp": "str", # Срок годности.
        "production": "str", # Производитель.
        "country": "str", # Страна производства.
    }
   "variants": int,  # Кол-во вариантов у товара в карточке.
}
```
## Инструкция по запуску парсера

* Клонировать репозиторий
```
git clone https://github.com/danlaryushin/maksavit_scrapy
```
* Установить зависимости
```
cd maksavit_scrapy
```
```
pip install -r requirements.txt
```
* Запустить парсер
```
cd maksavit_scrapy/spiders/
```
```
scrapy crawl maksavit
```

* Файл ```catalog.json``` с каталогом товаров будет размещен в папке ```catalog```

## Прокси
* Для использования прокси, в файле ```settings.py``` нужно задать переменную ```PROXY```
```
# Для использования парсера без прокси установлено дефолтное значение:
PROXY = None
# Для бесплатных прокси задайте значение:
PROXY = {'proxy': 'http://ip:port'}
# Для персональных прокси задайте значение:
PROXY = {'proxy': 'http://ip:port:user:password'}
```

## Автор
[Даниил Ларюшин](https://github.com/danlaryushin)
