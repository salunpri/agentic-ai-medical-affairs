"""Unit tests for dashboard exporter."""

import pytest
import os
import tempfile
import json
from policy_drafting.integration.dashboard_exporter import DashboardExporter


class TestDashboardExporter:
    """Test dashboard exporter functionality."""
    
    def test_initialization(self):
        """Test exporter initialization."""
        with tempfile.TemporaryDirectory() as tmpdir:
            exporter = DashboardExporter(export_dir=tmpdir)
            assert exporter.export_dir == tmpdir
    
    def test_export_json(self):
        """Test JSON export."""
        with tempfile.TemporaryDirectory() as tmpdir:
            exporter = DashboardExporter(export_dir=tmpdir)
            
            policy_draft = {
                "content": "Policy content",
                "policy_type": "clinical_policy",
                "components": {
                    "policy_number": "POL-001",
                    "title": "Test Policy"
                },
                "metadata": {"generated_at": "2024-01-01"}
            }
            
            output_file = exporter._export_json(policy_draft, "POL-001", True)
            
            assert os.path.exists(output_file)
            
            with open(output_file, 'r') as f:
                data = json.load(f)
                assert data["policy_id"] == "POL-001"
                assert "metadata" in data
    
    def test_export_markdown(self):
        """Test Markdown export."""
        with tempfile.TemporaryDirectory() as tmpdir:
            exporter = DashboardExporter(export_dir=tmpdir)
            
            policy_draft = {
                "content": "# Policy Title\n\nPolicy content here.",
                "components": {"policy_number": "POL-002"}
            }
            
            output_file = exporter._export_markdown(policy_draft, "POL-002")
            
            assert os.path.exists(output_file)
            assert output_file.endswith(".md")
    
    def test_generate_api_payload(self):
        """Test API payload generation."""
        exporter = DashboardExporter()
        
        policy_draft = {
            "policy_type": "clinical_policy",
            "components": {
                "policy_number": "POL-003",
                "title": "Test Policy",
                "effective_date": "2024-01-01",
                "policy_statement": "Statement",
                "rationale": "Rationale",
                "clinical_guidelines": "Guidelines",
                "compliance_requirements": "Requirements"
            },
            "metadata": {
                "generated_at": "2024-01-01",
                "model": "gpt-4",
                "evidence_count": 10,
                "high_quality_evidence": 5
            }
        }
        
        payload = exporter.generate_api_payload(policy_draft)
        
        assert payload["policy"]["id"] == "POL-003"
        assert payload["policy"]["title"] == "Test Policy"
        assert payload["metadata"]["evidence_count"] == 10


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
