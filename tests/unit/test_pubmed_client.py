"""Unit tests for PubMed client."""

import pytest
from unittest.mock import Mock, patch
from policy_drafting.evidence.pubmed_client import PubMedClient


class TestPubMedClient:
    """Test PubMed client functionality."""
    
    def test_initialization(self):
        """Test client initialization."""
        client = PubMedClient(email="test@example.com")
        assert client.email == "test@example.com"
        assert client.session is not None
    
    @patch('requests.Session.get')
    def test_search_articles(self, mock_get):
        """Test article search."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "esearchresult": {
                "idlist": ["12345", "67890"]
            }
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        client = PubMedClient()
        results = client.search_articles("diabetes", max_results=10)
        
        assert len(results) == 2
        assert "12345" in results
        assert "67890" in results
    
    @patch('requests.Session.get')
    def test_search_articles_error(self, mock_get):
        """Test article search with error."""
        mock_get.side_effect = Exception("Network error")
        
        client = PubMedClient()
        results = client.search_articles("diabetes")
        
        assert len(results) == 0
    
    def test_parse_xml_response(self):
        """Test XML parsing."""
        client = PubMedClient()
        xml_data = """
        <PubmedArticleSet>
            <PubmedArticle>
                <PMID>12345</PMID>
                <Article>
                    <ArticleTitle>Test Article</ArticleTitle>
                    <Abstract>
                        <AbstractText>Test abstract content</AbstractText>
                    </Abstract>
                </Article>
            </PubmedArticle>
        </PubmedArticleSet>
        """
        
        articles = client._parse_xml_response(xml_data)
        
        assert len(articles) == 1
        assert articles[0]["pmid"] == "12345"
        assert articles[0]["title"] == "Test Article"
        assert "Test abstract" in articles[0]["abstract"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
