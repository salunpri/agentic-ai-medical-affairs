"""PubMed API client for extracting medical research data."""

import os
from typing import List, Dict, Optional
from datetime import datetime
import requests
from loguru import logger


class PubMedClient:
    """Client for interacting with PubMed API to fetch medical research."""
    
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    
    def __init__(self, email: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize PubMed client.
        
        Args:
            email: Email for PubMed API (recommended by NCBI)
            api_key: API key for higher rate limits
        """
        self.email = email or os.getenv("PUBMED_EMAIL", "")
        self.api_key = api_key or os.getenv("PUBMED_API_KEY", "")
        self.session = requests.Session()
        logger.info("PubMed client initialized")
    
    def search_articles(
        self,
        query: str,
        max_results: int = 10,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None
    ) -> List[str]:
        """
        Search for articles in PubMed.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            date_from: Start date (YYYY/MM/DD)
            date_to: End date (YYYY/MM/DD)
            
        Returns:
            List of PubMed IDs
        """
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "json",
            "email": self.email,
        }
        
        if self.api_key:
            params["api_key"] = self.api_key
            
        if date_from:
            params["mindate"] = date_from
        if date_to:
            params["maxdate"] = date_to
        
        try:
            response = self.session.get(
                f"{self.BASE_URL}esearch.fcgi",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            id_list = data.get("esearchresult", {}).get("idlist", [])
            logger.info(f"Found {len(id_list)} articles for query: {query}")
            return id_list
            
        except Exception as e:
            logger.error(f"Error searching PubMed: {e}")
            return []
    
    def fetch_article_details(self, pubmed_ids: List[str]) -> List[Dict]:
        """
        Fetch detailed information for given PubMed IDs.
        
        Args:
            pubmed_ids: List of PubMed IDs
            
        Returns:
            List of article details
        """
        if not pubmed_ids:
            return []
        
        params = {
            "db": "pubmed",
            "id": ",".join(pubmed_ids),
            "retmode": "xml",
            "email": self.email,
        }
        
        if self.api_key:
            params["api_key"] = self.api_key
        
        try:
            response = self.session.get(
                f"{self.BASE_URL}efetch.fcgi",
                params=params,
                timeout=60
            )
            response.raise_for_status()
            
            # Parse XML response
            articles = self._parse_xml_response(response.text)
            logger.info(f"Fetched details for {len(articles)} articles")
            return articles
            
        except Exception as e:
            logger.error(f"Error fetching article details: {e}")
            return []
    
    def _parse_xml_response(self, xml_text: str) -> List[Dict]:
        """
        Parse XML response from PubMed.
        
        Args:
            xml_text: XML response text
            
        Returns:
            List of parsed article dictionaries
        """
        from bs4 import BeautifulSoup
        
        articles = []
        soup = BeautifulSoup(xml_text, "lxml-xml")
        
        for article in soup.find_all("PubmedArticle"):
            try:
                article_data = {}
                
                # Extract PMID
                pmid = article.find("PMID")
                article_data["pmid"] = pmid.text if pmid else ""
                
                # Extract title
                title = article.find("ArticleTitle")
                article_data["title"] = title.text if title else ""
                
                # Extract abstract
                abstract_parts = article.find_all("AbstractText")
                abstract = " ".join([part.text for part in abstract_parts])
                article_data["abstract"] = abstract
                
                # Extract authors
                authors = []
                for author in article.find_all("Author"):
                    last_name = author.find("LastName")
                    fore_name = author.find("ForeName")
                    if last_name and fore_name:
                        authors.append(f"{fore_name.text} {last_name.text}")
                article_data["authors"] = authors
                
                # Extract publication date
                pub_date = article.find("PubDate")
                if pub_date:
                    year = pub_date.find("Year")
                    month = pub_date.find("Month")
                    day = pub_date.find("Day")
                    date_str = ""
                    if year:
                        date_str += year.text
                    if month:
                        date_str += f"-{month.text}"
                    if day:
                        date_str += f"-{day.text}"
                    article_data["publication_date"] = date_str
                
                # Extract journal
                journal = article.find("Title")
                article_data["journal"] = journal.text if journal else ""
                
                # Extract keywords
                keywords = []
                for keyword in article.find_all("Keyword"):
                    keywords.append(keyword.text)
                article_data["keywords"] = keywords
                
                articles.append(article_data)
                
            except Exception as e:
                logger.warning(f"Error parsing article: {e}")
                continue
        
        return articles
    
    def search_and_fetch(
        self,
        query: str,
        max_results: int = 10
    ) -> List[Dict]:
        """
        Convenience method to search and fetch articles in one call.
        
        Args:
            query: Search query string
            max_results: Maximum number of results
            
        Returns:
            List of article details
        """
        pubmed_ids = self.search_articles(query, max_results)
        return self.fetch_article_details(pubmed_ids)
