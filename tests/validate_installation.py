#!/usr/bin/env python3
"""
Quick validation script to test core functionality.
This script runs basic tests without requiring external API keys.

Note: Run this after installing the package with `pip install -e .`
"""

import sys
from pathlib import Path

# Only add to path if package not installed
try:
    import policy_drafting
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from policy_drafting.evidence import EvidenceProcessor
from policy_drafting.models import PolicyGenerator
from policy_drafting.compliance import ComplianceValidator
from policy_drafting.explainability import AuditLogger
from policy_drafting.integration import DashboardExporter


def test_evidence_processor():
    """Test evidence processor."""
    print("Testing EvidenceProcessor...")
    processor = EvidenceProcessor()
    
    # Mock article data
    articles = [{
        "pmid": "12345",
        "title": "Test Study",
        "abstract": "RESULTS: Significant findings. CONCLUSION: Effective.",
        "authors": ["Smith J", "Jones A"],
        "publication_date": "2023-01-15",
        "journal": "Test Journal",
        "keywords": ["test", "study"]
    }]
    
    processed = processor.extract_key_findings(articles)
    assert len(processed) == 1
    assert "evidence_quality" in processed[0]
    print("  ✓ Evidence processor working correctly")


def test_policy_generator():
    """Test policy generator."""
    print("Testing PolicyGenerator...")
    generator = PolicyGenerator()
    
    evidence_synthesis = {
        "topic": "Test Topic",
        "total_articles": 10,
        "high_quality_count": 5,
        "key_findings": ["Finding 1", "Finding 2"],
        "summary": "Test summary",
        "evidence_base": {
            "high_quality": [{"pmid": "123", "title": "Test", "findings": []}],
            "supporting_evidence": []
        }
    }
    
    draft = generator.generate_policy_draft(evidence_synthesis)
    assert "content" in draft
    assert "components" in draft
    assert draft["components"]["policy_number"]
    print("  ✓ Policy generator working correctly")


def test_compliance_validator():
    """Test compliance validator."""
    print("Testing ComplianceValidator...")
    validator = ComplianceValidator()
    
    policy_draft = {
        "content": "Policy with FDA approved guidelines and patient safety.",
        "components": {
            "policy_statement": "Statement",
            "rationale": "Rationale",
            "evidence_base": "Evidence",
            "clinical_guidelines": "Guidelines",
            "references": "References"
        }
    }
    
    results = validator.validate_policy(policy_draft)
    assert "overall_status" in results
    assert "compliance_score" in results
    assert 0.0 <= results["compliance_score"] <= 1.0
    print("  ✓ Compliance validator working correctly")


def test_audit_logger():
    """Test audit logger."""
    print("Testing AuditLogger...")
    import tempfile
    
    with tempfile.TemporaryDirectory() as tmpdir:
        logger = AuditLogger(log_dir=tmpdir)
        
        entry_id = logger.log_evidence_extraction("test", 5, "pubmed")
        assert entry_id.startswith("evidence_extraction_")
        
        trail = logger.get_session_audit_trail()
        assert len(trail) == 1
        print("  ✓ Audit logger working correctly")


def test_dashboard_exporter():
    """Test dashboard exporter."""
    print("Testing DashboardExporter...")
    import tempfile
    
    with tempfile.TemporaryDirectory() as tmpdir:
        exporter = DashboardExporter(export_dir=tmpdir)
        
        policy_draft = {
            "content": "Test content",
            "policy_type": "clinical_policy",
            "components": {"policy_number": "POL-001", "title": "Test"},
            "metadata": {"generated_at": "2024-01-01"}
        }
        
        file_path = exporter.export_policy_draft(policy_draft, format="json")
        assert Path(file_path).exists()
        print("  ✓ Dashboard exporter working correctly")


def main():
    """Run all validation tests."""
    print("\n" + "="*70)
    print("VALIDATION TESTS")
    print("="*70 + "\n")
    
    try:
        test_evidence_processor()
        test_policy_generator()
        test_compliance_validator()
        test_audit_logger()
        test_dashboard_exporter()
        
        print("\n" + "="*70)
        print("ALL TESTS PASSED ✓")
        print("="*70 + "\n")
        return 0
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
