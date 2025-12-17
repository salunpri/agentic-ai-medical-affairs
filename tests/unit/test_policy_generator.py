"""Unit tests for policy generator."""

import pytest
from policy_drafting.models.policy_generator import PolicyGenerator


class TestPolicyGenerator:
    """Test policy generator functionality."""
    
    def test_initialization(self):
        """Test generator initialization."""
        generator = PolicyGenerator(model_name="gpt-4")
        assert generator.model_name == "gpt-4"
        assert generator.policy_templates is not None
    
    def test_generate_policy_draft(self):
        """Test policy draft generation."""
        generator = PolicyGenerator()
        
        evidence_synthesis = {
            "topic": "Diabetes Management",
            "total_articles": 15,
            "high_quality_count": 8,
            "key_findings": [
                "Early intervention improves outcomes",
                "Patient education is crucial"
            ],
            "summary": "Strong evidence supports comprehensive diabetes management.",
            "evidence_base": {
                "high_quality": [
                    {
                        "pmid": "12345",
                        "title": "Diabetes Study 1",
                        "findings": ["Key finding 1"]
                    }
                ],
                "supporting_evidence": []
            }
        }
        
        draft = generator.generate_policy_draft(evidence_synthesis)
        
        assert draft["policy_type"] == "clinical_policy"
        assert "content" in draft
        assert "metadata" in draft
        assert "components" in draft
        assert draft["components"]["title"]
        assert draft["components"]["policy_number"]
    
    def test_generate_title(self):
        """Test title generation."""
        generator = PolicyGenerator()
        
        evidence = {"topic": "Hypertension"}
        title = generator._generate_title(evidence)
        
        assert "Hypertension" in title
    
    def test_generate_policy_number(self):
        """Test policy number generation."""
        generator = PolicyGenerator()
        
        policy_num = generator._generate_policy_number()
        
        assert policy_num.startswith("POL-")
        assert len(policy_num) > 10


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
