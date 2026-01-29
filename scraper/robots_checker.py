"""
Robots.txt checker for compliance with web scraping policies.
"""

import logging
import time
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser
import requests

from config import ROBOTS_URL, ROBOTS_CACHE_EXPIRY, USER_AGENT, REQUEST_TIMEOUT

logger = logging.getLogger(__name__)

# Springer's explicitly allowed patterns (from Allow rules in robots.txt)
ALLOWED_PATTERNS = [
    '/journal',
    '/article/',
    '/articles',
    '/submission-guidelines',
    '/about'
]


class RobotsChecker:
    """
    Handles robots.txt parsing and compliance checking.
    Implements caching to avoid repeated fetches.
    """

    def __init__(self):
        """Initialize the robots checker with an empty cache."""
        self.parser = RobotFileParser()
        self.last_fetch_time = None
        self.cache_expiry = ROBOTS_CACHE_EXPIRY
        self.robots_url = ROBOTS_URL
        self.user_agent = USER_AGENT

    def fetch_robots(self):
        """
        Fetch and parse the robots.txt file.

        Returns:
            bool: True if robots.txt was successfully fetched and parsed.
        """
        try:
            logger.info(f"Fetching robots.txt from {self.robots_url}")
            response = requests.get(
                self.robots_url,
                timeout=REQUEST_TIMEOUT,
                headers={"User-Agent": self.user_agent}
            )
            response.raise_for_status()

            # Parse the robots.txt content
            self.parser.parse(response.text.splitlines())
            self.last_fetch_time = time.time()

            logger.info("Successfully fetched and parsed robots.txt")
            return True

        except requests.RequestException as e:
            logger.error(f"Failed to fetch robots.txt: {e}")
            # If we can't fetch robots.txt, err on the side of caution
            # and assume we're not allowed to crawl
            return False
        except Exception as e:
            logger.error(f"Error parsing robots.txt: {e}")
            return False

    def is_cache_valid(self):
        """
        Check if the cached robots.txt is still valid.

        Returns:
            bool: True if cache is valid, False otherwise.
        """
        if self.last_fetch_time is None:
            return False

        elapsed = time.time() - self.last_fetch_time
        return elapsed < self.cache_expiry

    def can_fetch(self, url):
        """
        Check if the given URL can be fetched according to robots.txt.

        Args:
            url (str): The URL to check.

        Returns:
            bool: True if URL can be fetched, False otherwise.
        """
        # Refresh cache if expired
        if not self.is_cache_valid():
            if not self.fetch_robots():
                logger.warning("Could not fetch robots.txt, denying access by default")
                return False

        # Check if URL can be fetched
        try:
            # Extract path from URL
            parsed_url = urlparse(url)
            url_path = parsed_url.path

            # Check if path matches any explicitly allowed pattern
            for pattern in ALLOWED_PATTERNS:
                if url_path.startswith(pattern):
                    logger.debug(f"URL allowed by explicit Allow pattern '{pattern}': {url}")
                    return True

            # Fall back to parser
            can_fetch = self.parser.can_fetch(self.user_agent, url)

            if can_fetch:
                logger.debug(f"URL allowed by robots.txt: {url}")
            else:
                logger.warning(f"URL disallowed by robots.txt: {url}")

            return can_fetch

        except Exception as e:
            logger.error(f"Error checking robots.txt permission for {url}: {e}")
            # Err on the side of caution
            return False

    def get_crawl_delay(self):
        """
        Get the crawl delay specified in robots.txt.

        Returns:
            float: Crawl delay in seconds, or None if not specified.
        """
        if not self.is_cache_valid():
            self.fetch_robots()

        try:
            delay = self.parser.crawl_delay(self.user_agent)
            if delay:
                logger.info(f"Crawl delay from robots.txt: {delay} seconds")
            return delay
        except Exception as e:
            logger.error(f"Error getting crawl delay: {e}")
            return None

    def get_request_rate(self):
        """
        Get the request rate specified in robots.txt.

        Returns:
            tuple: (requests, seconds) or None if not specified.
        """
        if not self.is_cache_valid():
            self.fetch_robots()

        try:
            rate = self.parser.request_rate(self.user_agent)
            if rate:
                logger.info(f"Request rate from robots.txt: {rate.requests} requests per {rate.seconds} seconds")
            return rate
        except Exception as e:
            logger.error(f"Error getting request rate: {e}")
            return None
