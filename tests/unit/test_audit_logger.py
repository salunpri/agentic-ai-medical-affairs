"""Unit tests for audit logger."""

import pytest
import os
import tempfile
from policy_drafting.explainability.audit_logger import AuditLogger


class TestAuditLogger:
    """Test audit logger functionality."""
    
    def test_initialization(self):
        """Test logger initialization."""
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = AuditLogger(log_dir=tmpdir)
            assert logger.log_dir == tmpdir
            assert logger.current_session_id is not None
    
    def test_log_evidence_extraction(self):
        """Test evidence extraction logging."""
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = AuditLogger(log_dir=tmpdir)
            
            entry_id = logger.log_evidence_extraction(
                query="diabetes",
                article_count=10,
                source="pubmed"
            )
            
            assert entry_id.startswith("evidence_extraction_")
    
    def test_log_policy_generation(self):
        """Test policy generation logging."""
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = AuditLogger(log_dir=tmpdir)
            
            entry_id = logger.log_policy_generation(
                policy_type="clinical_policy",
                model_used="gpt-4",
                evidence_count=15,
                policy_id="POL-001"
            )
            
            assert entry_id.startswith("policy_generation_")
    
    def test_get_session_audit_trail(self):
        """Test retrieving audit trail."""
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = AuditLogger(log_dir=tmpdir)
            
            # Log some activities
            logger.log_evidence_extraction("test", 5, "pubmed")
            logger.log_decision("test_decision", "approved", "good evidence")
            
            # Retrieve trail
            trail = logger.get_session_audit_trail()
            
            assert len(trail) == 2
            assert trail[0]["activity_type"] == "evidence_extraction"
            assert trail[1]["activity_type"] == "decision"
    
    def test_generate_audit_report(self):
        """Test audit report generation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = AuditLogger(log_dir=tmpdir)
            
            # Log activities
            logger.log_evidence_extraction("test", 10, "pubmed")
            logger.log_policy_generation("clinical_policy", "gpt-4", 10, "POL-001")
            
            # Generate report
            report = logger.generate_audit_report()
            
            assert "session_id" in report
            assert "total_activities" in report
            assert report["total_activities"] == 2
            assert "activity_summary" in report


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
