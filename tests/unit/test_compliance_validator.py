"""Unit tests for compliance validator."""

import pytest
from policy_drafting.compliance.validator import ComplianceValidator


class TestComplianceValidator:
    """Test compliance validator functionality."""
    
    def test_initialization(self):
        """Test validator initialization."""
        validator = ComplianceValidator()
        assert validator.validation_rules is not None
        assert "fda_guidelines" in validator.validation_rules
        assert "cms_requirements" in validator.validation_rules
    
    def test_validate_policy(self):
        """Test policy validation."""
        validator = ComplianceValidator()
        
        policy_draft = {
            "content": "This policy follows FDA approved guidelines and ensures patient safety.",
            "components": {
                "policy_statement": "Policy statement content",
                "rationale": "Rationale content",
                "evidence_base": "Evidence base content",
                "clinical_guidelines": "Clinical guidelines content",
                "references": "References content"
            }
        }
        
        results = validator.validate_policy(policy_draft)
        
        assert "overall_status" in results
        assert "compliance_score" in results
        assert "framework_results" in results
        assert results["compliance_score"] >= 0.0
        assert results["compliance_score"] <= 1.0
    
    def test_validate_framework(self):
        """Test framework validation."""
        validator = ComplianceValidator()
        
        rules = {
            "required_sections": ["policy_statement", "rationale"],
            "keywords": ["evidence-based", "safety"]
        }
        
        content = "This is an evidence-based policy that ensures safety"
        components = {
            "policy_statement": "Statement",
            "rationale": "Rationale"
        }
        
        result = validator._validate_framework("test_framework", rules, content, components)
        
        assert result["framework"] == "test_framework"
        assert result["checks_passed"] > 0
    
    def test_validate_evidence_quality(self):
        """Test evidence quality validation."""
        validator = ComplianceValidator()
        
        # Good evidence
        evidence = {
            "total_articles": 20,
            "high_quality_count": 10
        }
        
        result = validator.validate_evidence_quality(evidence)
        assert result["status"] in ["pass", "warning"]
        
        # Poor evidence
        evidence = {
            "total_articles": 2,
            "high_quality_count": 0
        }
        
        result = validator.validate_evidence_quality(evidence)
        assert result["status"] in ["fail", "warning"]
    
    def test_calculate_compliance_score(self):
        """Test compliance score calculation."""
        validator = ComplianceValidator()
        
        framework_results = {
            "framework1": {"checks_passed": 8, "checks_failed": 2},
            "framework2": {"checks_passed": 9, "checks_failed": 1}
        }
        
        score = validator._calculate_compliance_score(framework_results)
        
        assert score > 0.0
        assert score <= 1.0
        assert score == 17 / 20  # (8+9) / (10+10)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
