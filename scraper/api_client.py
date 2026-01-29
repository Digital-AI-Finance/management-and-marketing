"""
Springer Nature API client for fetching journal metadata and articles.
"""

import logging
import requests
from typing import Optional, Dict, List, Any

from config import (
    SPRINGER_API_KEY,
    SPRINGER_METADATA_ENDPOINT,
    SPRINGER_OPENACCESS_ENDPOINT,
    REQUEST_TIMEOUT,
    MAX_RETRIES,
    RETRY_DELAY,
    USER_AGENT
)

logger = logging.getLogger(__name__)


class SpringerAPIClient:
    """
    Client for interacting with the Springer Nature API.
    Provides methods to fetch journal metadata and articles.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the API client.

        Args:
            api_key: Springer Nature API key. If None, uses SPRINGER_API_KEY from config.
        """
        self.api_key = api_key or SPRINGER_API_KEY
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": USER_AGENT,
            "Accept": "application/json"
        })

        if not self.api_key:
            logger.warning("No Springer API key provided. API functionality will be limited.")

    def is_available(self) -> bool:
        """
        Check if the API is available with the current API key.

        Returns:
            bool: True if API is available, False otherwise.
        """
        if not self.api_key:
            return False

        try:
            # Test API with a simple metadata query
            response = self.session.get(
                SPRINGER_METADATA_ENDPOINT,
                params={
                    "q": "journal:Management and Marketing",
                    "api_key": self.api_key,
                    "p": 1,
                    "s": 1
                },
                timeout=REQUEST_TIMEOUT
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"API availability check failed: {e}")
            return False

    def _make_request(self, url: str, params: Dict[str, Any]) -> Optional[Dict]:
        """
        Make a request to the API with retry logic.

        Args:
            url: API endpoint URL
            params: Query parameters

        Returns:
            dict: JSON response or None if request fails
        """
        if not self.api_key:
            logger.error("Cannot make API request without API key")
            return None

        # Add API key to parameters
        params["api_key"] = self.api_key

        for attempt in range(MAX_RETRIES):
            try:
                logger.debug(f"API request attempt {attempt + 1}/{MAX_RETRIES}: {url}")
                response = self.session.get(url, params=params, timeout=REQUEST_TIMEOUT)
                response.raise_for_status()

                data = response.json()
                logger.info(f"API request successful: {url}")
                return data

            except requests.HTTPError as e:
                if response.status_code == 429:  # Rate limit
                    logger.warning(f"API rate limit hit, retrying in {RETRY_DELAY} seconds...")
                    import time
                    time.sleep(RETRY_DELAY)
                    continue
                elif response.status_code in [500, 502, 503, 504]:  # Server errors
                    logger.warning(f"Server error {response.status_code}, retrying...")
                    import time
                    time.sleep(RETRY_DELAY)
                    continue
                else:
                    logger.error(f"API request failed with status {response.status_code}: {e}")
                    return None

            except requests.RequestException as e:
                logger.error(f"API request failed: {e}")
                if attempt < MAX_RETRIES - 1:
                    import time
                    time.sleep(RETRY_DELAY)
                    continue
                return None

            except ValueError as e:
                logger.error(f"Failed to parse API response as JSON: {e}")
                return None

        logger.error(f"API request failed after {MAX_RETRIES} attempts")
        return None

    def get_journal_metadata(self, journal_id: str) -> Optional[Dict]:
        """
        Fetch metadata for a specific journal.

        Args:
            journal_id: Journal identifier (e.g., "44491")

        Returns:
            dict: Journal metadata or None if request fails
        """
        logger.info(f"Fetching journal metadata for ID: {journal_id}")

        params = {
            "q": f"journal:{journal_id}",
            "p": 1,
            "s": 1
        }

        data = self._make_request(SPRINGER_METADATA_ENDPOINT, params)

        if data and "records" in data and len(data["records"]) > 0:
            return data["records"][0]

        logger.warning(f"No metadata found for journal {journal_id}")
        return None

    def get_articles(
        self,
        journal_id: str,
        start: int = 1,
        count: int = 50,
        year: Optional[int] = None
    ) -> List[Dict]:
        """
        Fetch articles from a journal.

        Args:
            journal_id: Journal identifier (e.g., "44491")
            start: Starting position for pagination (1-indexed)
            count: Number of articles to fetch (max 100)
            year: Optional year filter

        Returns:
            list: List of article metadata dictionaries
        """
        logger.info(f"Fetching articles for journal {journal_id}, start={start}, count={count}")

        # Build query
        query_parts = [f"journal:{journal_id}"]
        if year:
            query_parts.append(f"year:{year}")

        params = {
            "q": " ".join(query_parts),
            "p": start,
            "s": min(count, 100)  # API limit is 100 per request
        }

        data = self._make_request(SPRINGER_METADATA_ENDPOINT, params)

        if data and "records" in data:
            articles = data["records"]
            logger.info(f"Retrieved {len(articles)} articles")
            return articles

        logger.warning(f"No articles found for journal {journal_id}")
        return []

    def get_open_access_content(self, doi: str) -> Optional[Dict]:
        """
        Fetch full open access content for an article by DOI.

        Args:
            doi: Digital Object Identifier for the article

        Returns:
            dict: Article content or None if not available
        """
        logger.info(f"Fetching open access content for DOI: {doi}")

        params = {
            "q": f"doi:{doi}"
        }

        data = self._make_request(SPRINGER_OPENACCESS_ENDPOINT, params)

        if data and "records" in data and len(data["records"]) > 0:
            return data["records"][0]

        logger.warning(f"No open access content found for DOI: {doi}")
        return None

    def search_articles(
        self,
        query: str,
        journal_id: Optional[str] = None,
        start: int = 1,
        count: int = 50
    ) -> List[Dict]:
        """
        Search for articles using a custom query.

        Args:
            query: Search query string
            journal_id: Optional journal ID to restrict search
            start: Starting position for pagination
            count: Number of results to fetch

        Returns:
            list: List of article metadata dictionaries
        """
        logger.info(f"Searching articles with query: {query}")

        # Build query
        if journal_id:
            full_query = f"({query}) AND journal:{journal_id}"
        else:
            full_query = query

        params = {
            "q": full_query,
            "p": start,
            "s": min(count, 100)
        }

        data = self._make_request(SPRINGER_METADATA_ENDPOINT, params)

        if data and "records" in data:
            articles = data["records"]
            logger.info(f"Found {len(articles)} articles matching query")
            return articles

        logger.warning(f"No articles found matching query: {query}")
        return []

    def close(self):
        """Close the session."""
        self.session.close()
        logger.debug("API client session closed")
