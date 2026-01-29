"""
Main scraper for Management & Marketing journal website.
Implements API-first approach with web scraping fallback.
"""

import json
import logging
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from config import (
    BASE_URL,
    USER_AGENT,
    REQUEST_DELAY,
    REQUEST_TIMEOUT,
    MAX_RETRIES,
    RETRY_DELAY,
    SELECTORS,
    OUTPUT_DIR,
    OUTPUT_FORMAT,
    OUTPUT_ENCODING,
    LOG_LEVEL,
    LOG_FORMAT,
    LOG_FILE
)
from robots_checker import RobotsChecker
from api_client import SpringerAPIClient

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class JournalScraper:
    """
    Main scraper class for Management & Marketing journal.
    Handles both API requests and web scraping with robots.txt compliance.
    """

    def __init__(self):
        """Initialize the scraper with necessary components."""
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})

        # Initialize robots checker and API client
        self.robots_checker = RobotsChecker()
        self.api_client = SpringerAPIClient()

        # Track last request time for rate limiting
        self.last_request_time = None

        # Check if API is available
        self.api_available = self.api_client.is_available()
        if self.api_available:
            logger.info("Springer API is available - will use API-first approach")
        else:
            logger.info("Springer API not available - will use web scraping")

        logger.info(f"Scraper initialized with base URL: {self.base_url}")

    def _enforce_rate_limit(self):
        """Enforce rate limiting between requests."""
        if self.last_request_time is not None:
            elapsed = time.time() - self.last_request_time
            if elapsed < REQUEST_DELAY:
                sleep_time = REQUEST_DELAY - elapsed
                logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
                time.sleep(sleep_time)

        self.last_request_time = time.time()

    def _check_robots_compliance(self, url: str) -> bool:
        """
        Check if URL can be fetched according to robots.txt.

        Args:
            url: URL to check

        Returns:
            bool: True if allowed, False otherwise
        """
        if not self.robots_checker.can_fetch(url):
            logger.warning(f"Access to {url} disallowed by robots.txt")
            return False
        return True

    def _make_request(self, url: str, allow_redirects: bool = True) -> Optional[requests.Response]:
        """
        Make an HTTP request with error handling and redirect tracking.

        Args:
            url: URL to fetch
            allow_redirects: Whether to follow redirects

        Returns:
            Response object or None if request fails
        """
        # Check robots.txt compliance
        if not self._check_robots_compliance(url):
            return None

        # Enforce rate limiting
        self._enforce_rate_limit()

        for attempt in range(MAX_RETRIES):
            try:
                logger.debug(f"Request attempt {attempt + 1}/{MAX_RETRIES}: {url}")

                response = self.session.get(
                    url,
                    timeout=REQUEST_TIMEOUT,
                    allow_redirects=allow_redirects
                )

                # Log redirect chain if redirects occurred
                if response.history:
                    logger.info(f"Redirect chain for {url}:")
                    for resp in response.history:
                        logger.info(f"  {resp.status_code} -> {resp.url}")
                    logger.info(f"  Final: {response.status_code} -> {response.url}")

                    # Verify final URL is on Springer domain
                    final_domain = urlparse(response.url).netloc
                    if "springer.com" not in final_domain:
                        logger.warning(f"Redirected to non-Springer domain: {final_domain}")

                response.raise_for_status()
                logger.info(f"Successfully fetched: {url}")
                return response

            except requests.HTTPError as e:
                if response.status_code == 429:  # Rate limit
                    logger.warning(f"Rate limit hit, retrying in {RETRY_DELAY} seconds...")
                    time.sleep(RETRY_DELAY)
                    continue
                elif response.status_code == 303:  # See Other redirect
                    logger.info(f"303 redirect encountered for {url}")
                    if attempt < MAX_RETRIES - 1:
                        continue
                elif response.status_code in [500, 502, 503, 504]:  # Server errors
                    logger.warning(f"Server error {response.status_code}, retrying...")
                    time.sleep(RETRY_DELAY)
                    continue
                else:
                    logger.error(f"HTTP error {response.status_code}: {e}")
                    return None

            except requests.RequestException as e:
                logger.error(f"Request failed: {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
                    continue
                return None

        logger.error(f"Request failed after {MAX_RETRIES} attempts: {url}")
        return None

    def _parse_with_fallback(self, soup: BeautifulSoup, selector_key: str) -> List:
        """
        Try multiple CSS selectors with fallback chain.

        Args:
            soup: BeautifulSoup object
            selector_key: Key in SELECTORS dict

        Returns:
            list: Found elements or empty list
        """
        selectors = SELECTORS.get(selector_key, [])

        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                logger.debug(f"Found elements with selector '{selector}' for key '{selector_key}'")
                return elements

        logger.warning(f"No elements found for selector key '{selector_key}'")
        return []

    def get_journal_info(self) -> Dict[str, Any]:
        """
        Fetch journal information (title, description, ISSN, etc.).
        Uses API first, falls back to web scraping.

        Returns:
            dict: Journal information
        """
        logger.info("Fetching journal information")

        # Try API first
        if self.api_available:
            journal_data = self.api_client.get_journal_metadata("44491")
            if journal_data:
                return {
                    "title": journal_data.get("title", ""),
                    "description": journal_data.get("abstract", ""),
                    "issn": journal_data.get("issn", ""),
                    "eisn": journal_data.get("eisn", ""),
                    "publisher": journal_data.get("publisher", ""),
                    "url": journal_data.get("url", [{}])[0].get("value", ""),
                    "source": "api",
                    "timestamp": datetime.now().isoformat()
                }

        # Fallback to web scraping
        logger.info("Using web scraping fallback for journal info")
        response = self._make_request(self.base_url)
        if not response:
            logger.error("Failed to fetch journal homepage")
            return {}

        soup = BeautifulSoup(response.content, "lxml")

        # Extract journal title
        title_elements = self._parse_with_fallback(soup, "journal_title")
        title = title_elements[0].get_text(strip=True) if title_elements else ""

        # Extract description
        desc_elements = self._parse_with_fallback(soup, "journal_description")
        description = " ".join([p.get_text(strip=True) for p in desc_elements])

        return {
            "title": title,
            "description": description,
            "url": self.base_url,
            "source": "scraping",
            "timestamp": datetime.now().isoformat()
        }

    def get_articles(self, start: int = 1, count: int = 50, year: Optional[int] = None) -> List[Dict]:
        """
        Fetch articles from the journal.
        Uses API first, falls back to web scraping.

        Args:
            start: Starting position for pagination
            count: Number of articles to fetch
            year: Optional year filter

        Returns:
            list: List of article dictionaries
        """
        logger.info(f"Fetching articles (start={start}, count={count}, year={year})")

        # Try API first
        if self.api_available:
            articles = self.api_client.get_articles("44491", start, count, year)
            if articles:
                return self._normalize_api_articles(articles)

        # Fallback to web scraping
        logger.info("Using web scraping fallback for articles")
        return self._scrape_articles(start, count)

    def _normalize_api_articles(self, api_articles: List[Dict]) -> List[Dict]:
        """
        Normalize API article data to standard format.

        Args:
            api_articles: List of articles from API

        Returns:
            list: Normalized article dictionaries
        """
        normalized = []

        for article in api_articles:
            # Extract authors
            creators = article.get("creators", [])
            authors = [creator.get("creator", "") for creator in creators]

            # Extract URLs
            urls = article.get("url", [])
            article_url = urls[0].get("value", "") if urls else ""

            normalized.append({
                "title": article.get("title", ""),
                "authors": authors,
                "date": article.get("publicationDate", ""),
                "type": article.get("contentType", ""),
                "doi": article.get("doi", ""),
                "url": article_url,
                "abstract": article.get("abstract", ""),
                "source": "api"
            })

        return normalized

    def _scrape_articles(self, start: int, count: int) -> List[Dict]:
        """
        Scrape articles from the journal website.

        Args:
            start: Starting position
            count: Number of articles to fetch

        Returns:
            list: List of article dictionaries
        """
        articles = []
        page = (start - 1) // 20 + 1  # Assuming 20 articles per page

        while len(articles) < count:
            url = f"{self.base_url}/articles?page={page}"
            response = self._make_request(url)

            if not response:
                break

            soup = BeautifulSoup(response.content, "lxml")

            # Parse article cards
            article_elements = self._parse_with_fallback(soup, "article_title")

            if not article_elements:
                logger.info("No more articles found")
                break

            for elem in article_elements:
                if len(articles) >= count:
                    break

                # Extract article data
                article_data = self._parse_article_element(soup, elem)
                if article_data:
                    articles.append(article_data)

            page += 1

        return articles

    def _parse_article_element(self, soup: BeautifulSoup, title_elem) -> Optional[Dict]:
        """
        Parse a single article element from HTML.

        Args:
            soup: BeautifulSoup object
            title_elem: Title element

        Returns:
            dict: Article data or None
        """
        try:
            # Get parent article container
            article_container = title_elem.find_parent("article") or title_elem.find_parent("div")

            if not article_container:
                return None

            # Extract title and URL
            title = title_elem.get_text(strip=True)
            url = title_elem.get("href", "")
            if url and not url.startswith("http"):
                url = urljoin(self.base_url, url)

            # Extract authors
            author_elements = article_container.select(SELECTORS["article_authors"][0])
            authors = [author.get_text(strip=True) for author in author_elements]

            # Extract date
            date_elements = article_container.select(SELECTORS["article_date"][0])
            date = date_elements[0].get_text(strip=True) if date_elements else ""

            # Extract type
            type_elements = article_container.select(SELECTORS["article_type"][0])
            article_type = type_elements[0].get_text(strip=True) if type_elements else ""

            return {
                "title": title,
                "authors": authors,
                "date": date,
                "type": article_type,
                "url": url,
                "source": "scraping"
            }

        except Exception as e:
            logger.error(f"Error parsing article element: {e}")
            return None

    def get_editorial_board(self) -> List[Dict]:
        """
        Fetch editorial board information.

        Returns:
            list: List of editor dictionaries
        """
        logger.info("Fetching editorial board")

        url = f"{self.base_url}/editors"
        response = self._make_request(url)

        if not response:
            logger.error("Failed to fetch editorial board page")
            return []

        soup = BeautifulSoup(response.content, "lxml")

        editors = []
        editor_elements = self._parse_with_fallback(soup, "editorial_board_member")

        for elem in editor_elements:
            # Extract name
            name_elements = elem.select(SELECTORS["editor_name"][0])
            name = name_elements[0].get_text(strip=True) if name_elements else ""

            # Extract affiliation
            affiliation_elements = elem.select(SELECTORS["editor_affiliation"][0])
            affiliation = affiliation_elements[0].get_text(strip=True) if affiliation_elements else ""

            if name:
                editors.append({
                    "name": name,
                    "affiliation": affiliation
                })

        logger.info(f"Found {len(editors)} editorial board members")
        return editors

    def get_aims_scope(self) -> str:
        """
        Fetch journal aims and scope.

        Returns:
            str: Aims and scope text
        """
        logger.info("Fetching aims and scope")

        url = f"{self.base_url}/aims-and-scope"
        response = self._make_request(url)

        if not response:
            logger.error("Failed to fetch aims and scope page")
            return ""

        soup = BeautifulSoup(response.content, "lxml")

        aims_elements = self._parse_with_fallback(soup, "aims_scope")

        if aims_elements:
            aims_text = aims_elements[0].get_text(strip=True)
            logger.info(f"Retrieved aims and scope ({len(aims_text)} characters)")
            return aims_text

        return ""

    def save_data(self, data: Dict, filename: str):
        """
        Save scraped data to a JSON file.

        Args:
            data: Data to save
            filename: Output filename
        """
        # Create output directory if it doesn't exist
        output_dir = Path(OUTPUT_DIR)
        output_dir.mkdir(exist_ok=True)

        filepath = output_dir / filename

        try:
            with open(filepath, "w", encoding=OUTPUT_ENCODING) as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            logger.info(f"Data saved to {filepath}")

        except Exception as e:
            logger.error(f"Failed to save data to {filepath}: {e}")

    def close(self):
        """Clean up resources."""
        self.session.close()
        self.api_client.close()
        logger.info("Scraper closed")


def main():
    """
    Main function to run the scraper.
    """
    logger.info("=" * 60)
    logger.info("Starting Management & Marketing Journal Scraper")
    logger.info("=" * 60)

    scraper = JournalScraper()

    try:
        # Fetch journal information
        journal_info = scraper.get_journal_info()
        if journal_info:
            scraper.save_data(journal_info, "journal_info.json")

        # Fetch articles
        articles = scraper.get_articles(start=1, count=50)
        if articles:
            scraper.save_data({"articles": articles, "count": len(articles)}, "articles.json")

        # Fetch editorial board
        editors = scraper.get_editorial_board()
        if editors:
            scraper.save_data({"editors": editors, "count": len(editors)}, "editorial_board.json")

        # Fetch aims and scope
        aims_scope = scraper.get_aims_scope()
        if aims_scope:
            scraper.save_data({"aims_scope": aims_scope}, "aims_scope.json")

        logger.info("=" * 60)
        logger.info("Scraping completed successfully")
        logger.info("=" * 60)

    except KeyboardInterrupt:
        logger.info("Scraping interrupted by user")
    except Exception as e:
        logger.error(f"Scraping failed with error: {e}", exc_info=True)
    finally:
        scraper.close()


if __name__ == "__main__":
    main()
