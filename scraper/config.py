"""
Configuration settings for the journal scraper.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base URLs
BASE_URL = "https://link.springer.com/journal/44491"
ROBOTS_URL = "https://link.springer.com/robots.txt"

# Springer Nature API Configuration
SPRINGER_API_KEY = os.getenv("SPRINGER_API_KEY")
SPRINGER_API_BASE = "https://api.springernature.com"
SPRINGER_METADATA_ENDPOINT = f"{SPRINGER_API_BASE}/meta/v2/json"
SPRINGER_OPENACCESS_ENDPOINT = f"{SPRINGER_API_BASE}/openaccess/json"

# Request Configuration
REQUEST_DELAY = 2.5  # Delay in seconds between requests
REQUEST_TIMEOUT = 30  # Request timeout in seconds
MAX_RETRIES = 3  # Maximum number of retries for failed requests
RETRY_DELAY = 5  # Delay in seconds between retries

# User Agent Configuration
USER_AGENT = (
    "Mozilla/5.0 (compatible; AcademicResearchBot/1.0; "
    "+https://example.com/bot; research@example.com)"
)

# Robots.txt Cache Configuration
ROBOTS_CACHE_EXPIRY = 3600  # Cache expiry in seconds (1 hour)

# CSS Selectors with Fallback Chains
SELECTORS = {
    "journal_title": [
        "h1.c-article-title",
        "h1.app-article-masthead__title",
        "h1.page-title",
        "h1[data-test='journal-title']",
        "h1.journal-title"
    ],
    "journal_description": [
        "div.c-article-body p",
        "div.app-article-body p",
        "div.journal-description p",
        "div[data-test='journal-description'] p"
    ],
    "article_title": [
        "h3.c-card__title a",
        "h3.app-card-open__heading a",
        "a.title",
        "h3.article-title a",
        "a[data-test='article-title']"
    ],
    "article_authors": [
        "ul.c-author-list li",
        "ul.app-author-list li",
        "span.authors span",
        "ul.author-list li",
        "div[data-test='authors'] span"
    ],
    "article_date": [
        "time.c-meta__item",
        "time.app-meta__item",
        "span.date",
        "time[datetime]",
        "span[data-test='published-date']"
    ],
    "article_type": [
        "span.c-card__type",
        "span.app-card__type",
        "span.article-type",
        "span[data-test='content-type']"
    ],
    "article_link": [
        "a.c-card__link",
        "a.app-card__link",
        "a.article-link",
        "a[data-test='article-link']"
    ],
    "editorial_board_member": [
        "div.editorial-board-member",
        "div.editor",
        "div[data-test='editor']",
        "li.board-member"
    ],
    "editor_name": [
        "h3.editor-name",
        "span.name",
        "strong.name",
        "div.name"
    ],
    "editor_affiliation": [
        "p.affiliation",
        "span.affiliation",
        "div.affiliation"
    ],
    "aims_scope": [
        "div#aims-and-scope",
        "section.aims-scope",
        "div[data-test='aims-scope']",
        "div.aims-and-scope-content"
    ]
}

# Output Configuration
OUTPUT_DIR = "data"
OUTPUT_FORMAT = "json"
OUTPUT_ENCODING = "utf-8"

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = "scraper.log"
