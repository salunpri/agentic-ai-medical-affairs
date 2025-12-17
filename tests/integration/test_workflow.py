"""Integration tests for the complete policy drafting workflow."""

import pytest
from unittest.mock import Mock, patch
from policy_drafting.workflow import PolicyDraftingWorkflow


class TestPolicyDraftingWorkflow:
    """Test complete workflow integration."""
    
    @patch('policy_drafting.evidence.pubmed_client.PubMedClient.search_and_fetch')
    def test_full_workflow_execution(self, mock_search_fetch):
        """Test complete workflow execution."""
        # Mock PubMed response
        mock_search_fetch.return_value = [
            {
                "pmid": "12345",
                "title": "Diabetes Management Study",
                "abstract": "RESULTS: Study showed significant improvement in glycemic control. CONCLUSION: Effective treatment approach.",
                "authors": ["Smith J", "Jones A", "Brown B", "Wilson C", "Davis D"],
                "publication_date": "2023-06-15",
                "journal": "Diabetes Care",
                "keywords": ["diabetes", "glycemic control", "treatment", "clinical trial", "evidence-based"]
            },
            {
                "pmid": "67890",
                "title": "Long-term Diabetes Outcomes",
                "abstract": "Study demonstrated improved patient outcomes with comprehensive care.",
                "authors": ["Johnson M", "Williams R"],
                "publication_date": "2022-03-10",
                "journal": "Medical Journal",
                "keywords": ["diabetes", "outcomes", "care"]
            }
        ]
        
        workflow = PolicyDraftingWorkflow()
        results = workflow.execute_full_workflow(
            topic="Diabetes Management",
            max_articles=10,
            policy_type="clinical_policy"
        )
        
        assert results["status"] == "completed"
        assert results["topic"] == "Diabetes Management"
        assert "policy_draft" in results
        assert "validation_results" in results
        assert "audit_report" in results
        assert "summary" in results
        
        # Check policy draft
        policy_draft = results["policy_draft"]
        assert policy_draft["policy_type"] == "clinical_policy"
        assert "content" in policy_draft
        assert "components" in policy_draft
        
        # Check validation
        validation = results["validation_results"]
        assert "overall_status" in validation
        assert "compliance_score" in validation
        
        # Check summary
        summary = results["summary"]
        assert summary["articles_found"] == 2
        assert "policy_id" in summary
    
    def test_generate_policy_from_evidence(self):
        """Test generating policy from pre-synthesized evidence."""
        workflow = PolicyDraftingWorkflow()
        
        evidence_synthesis = {
            "topic": "Hypertension Management",
            "total_articles": 15,
            "high_quality_count": 8,
            "key_findings": ["Blood pressure control is essential", "Lifestyle modifications help"],
            "summary": "Strong evidence for comprehensive hypertension management.",
            "evidence_base": {
                "high_quality": [
                    {"pmid": "11111", "title": "Study 1", "findings": ["Finding 1"]}
                ],
                "supporting_evidence": []
            }
        }
        
        results = workflow.generate_policy_from_evidence(evidence_synthesis)
        
        assert "policy_draft" in results
        assert "validation_results" in results
        assert results["policy_draft"]["components"]["title"]
    
    def test_validate_existing_policy(self):
        """Test validating an existing policy."""
        workflow = PolicyDraftingWorkflow()
        
        policy_draft = {
            "content": "Policy with FDA approved guidelines and patient safety measures.",
            "components": {
                "policy_statement": "Statement",
                "rationale": "Rationale",
                "evidence_base": "Evidence",
                "clinical_guidelines": "Guidelines",
                "references": "References"
            }
        }
        
        validation_results = workflow.validate_existing_policy(policy_draft)
        
        assert "overall_status" in validation_results
        assert "compliance_score" in validation_results
        assert validation_results["compliance_score"] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
