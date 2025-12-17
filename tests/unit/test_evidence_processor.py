"""Unit tests for evidence processor."""

import pytest
from policy_drafting.evidence.evidence_processor import EvidenceProcessor


class TestEvidenceProcessor:
    """Test evidence processor functionality."""
    
    def test_initialization(self):
        """Test processor initialization."""
        processor = EvidenceProcessor()
        assert processor.evidence_cache is not None
    
    def test_extract_key_findings(self):
        """Test key findings extraction."""
        processor = EvidenceProcessor()
        
        articles = [
            {
                "pmid": "12345",
                "title": "Test Study",
                "abstract": "RESULTS: The study showed significant improvement. CONCLUSION: Treatment is effective.",
                "authors": ["Smith J", "Jones A"],
                "publication_date": "2023-01-15",
                "journal": "Medical Journal",
                "keywords": ["diabetes", "treatment", "clinical trial"]
            }
        ]
        
        processed = processor.extract_key_findings(articles)
        
        assert len(processed) == 1
        assert processed[0]["pmid"] == "12345"
        assert "evidence_quality" in processed[0]
        assert "relevance_score" in processed[0]
    
    def test_assess_evidence_quality(self):
        """Test evidence quality assessment."""
        processor = EvidenceProcessor()
        
        # High quality article
        article = {
            "publication_date": "2023-01-15",
            "abstract": "A" * 600,  # Long abstract
            "keywords": ["k1", "k2", "k3", "k4", "k5"],
            "authors": ["A1", "A2", "A3", "A4", "A5", "A6"]
        }
        
        quality = processor._assess_evidence_quality(article)
        assert quality == "high"
        
        # Low quality article
        article = {
            "publication_date": "2010-01-15",
            "abstract": "Short",
            "keywords": [],
            "authors": ["A1"]
        }
        
        quality = processor._assess_evidence_quality(article)
        assert quality == "low"
    
    def test_synthesize_evidence(self):
        """Test evidence synthesis."""
        processor = EvidenceProcessor()
        
        processed_evidence = [
            {
                "pmid": "12345",
                "title": "Study 1",
                "evidence_quality": "high",
                "key_findings": ["Finding 1", "Finding 2"]
            },
            {
                "pmid": "67890",
                "title": "Study 2",
                "evidence_quality": "medium",
                "key_findings": ["Finding 3"]
            }
        ]
        
        synthesis = processor.synthesize_evidence(processed_evidence, "Test Topic")
        
        assert synthesis["topic"] == "Test Topic"
        assert synthesis["total_articles"] == 2
        assert synthesis["high_quality_count"] == 1
        assert len(synthesis["key_findings"]) >= 1
    
    def test_filter_by_quality(self):
        """Test quality filtering."""
        processor = EvidenceProcessor()
        
        evidence = [
            {"evidence_quality": "high"},
            {"evidence_quality": "medium"},
            {"evidence_quality": "low"}
        ]
        
        filtered = processor.filter_by_quality(evidence, "medium")
        assert len(filtered) == 2
        
        filtered = processor.filter_by_quality(evidence, "high")
        assert len(filtered) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
