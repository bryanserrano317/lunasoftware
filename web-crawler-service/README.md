# Scrapy Project Documentation

## Overview
This project is a **Scrapy-based web crawler** designed to scrape content from websites. It includes item models, middlewares, pipelines, and settings required for web scraping.

---

## Components

### `items.py`
- Defines Scrapy items used to structure the extracted data.
- Uses `scrapy.Item` to define item fields.
- Currently contains a placeholder item model `CrawlingItem`【items.py】.

#### Dependencies
- `scrapy`

---

### `middlewares.py`
- Defines custom middlewares for request processing.
- Implements the `CrawlingSpiderMiddleware` class to modify request handling【middlewares.py】.
- Uses Scrapy signals to control request flow.

#### Dependencies
- `scrapy`
- `scrapy.exceptions.IgnoreRequest`
- `itemadapter`

---

### `pipelines.py`
- Handles item processing before storing scraped data.
- The `CrawlingPipeline` class processes each scraped item.
- To enable pipelines, they need to be added in `settings.py`【pipelines.py】.

#### Dependencies
- `itemadapter`

---

### `settings.py`
- Defines Scrapy project settings.
- Configures the bot name, modules, and crawling policies.
- Uses `USER_AGENT` settings and respects `robots.txt`【settings.py】.

#### Key Settings
- **BOT_NAME**: `"crawling"`
- **SPIDER_MODULES**: `["crawling.spiders"]`
- **ROBOTSTXT_OBEY**: `True` (ensures the bot respects robots.txt rules)

---

### `crawling_spider.py`
- Implements the main Scrapy spider for crawling.
- Uses `CrawlSpider` with `LinkExtractor` to follow links.
- Targets a website for scraping.
- Handles HTTP status codes (404, 403, 302)【crawling_spider.py】.

#### Key Components
- **`allowed_domains = ['awebsite.com']`**: Limits the crawl to specific domains.
- **`start_urls = ["awebsite.com/suburl"]`**: Entry point for scraping.
- **`parse_item(response)`**: Extracts page data.

#### Dependencies
- `scrapy`
- `scrapy.spiders.CrawlSpider`
- `scrapy.linkextractors.LinkExtractor`
- `logging`

---

## Setup Instructions

1. **Install dependencies:**
   ```bash
   pip install scrapy
   ```
2. **Run the Scrapy spider:**
   ```bash
   scrapy crawl crawling
   ```

---

## License
This project is licensed under MIT License.
