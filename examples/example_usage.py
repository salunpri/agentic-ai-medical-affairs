#!/usr/bin/env python3
"""
Example usage of the Healthcare Policy Drafting System.

This script demonstrates how to use the system to generate
a healthcare policy from medical research.

Note: Run this after installing the package with `pip install -e .`
"""

import sys
from pathlib import Path

# Only add to path if package not installed
try:
    import policy_drafting
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from policy_drafting.workflow import PolicyDraftingWorkflow
from policy_drafting.evidence import PubMedClient, EvidenceProcessor
from policy_drafting.models import PolicyGenerator
from policy_drafting.compliance import ComplianceValidator
from loguru import logger


def example_full_workflow():
    """Example: Execute the complete workflow."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Full Workflow Execution")
    print("="*70)
    
    # Initialize workflow
    workflow = PolicyDraftingWorkflow()
    
    # Note: This example uses mock data since it requires API keys
    # In production, set PUBMED_EMAIL and OPENAI_API_KEY environment variables
    
    print("\nThis example demonstrates the complete workflow:")
    print("1. Extract evidence from PubMed")
    print("2. Process and synthesize evidence")
    print("3. Generate policy draft")
    print("4. Validate compliance")
    print("5. Create audit trail")
    print("6. Export results")
    
    print("\nTo run with real data:")
    print("  export PUBMED_EMAIL=your@email.com")
    print("  export OPENAI_API_KEY=sk-your-key")
    print("  python examples/example_usage.py")


def example_evidence_extraction():
    """Example: Extract and process evidence."""
    print("\n" + "="*70)
    print("EXAMPLE 2: Evidence Extraction and Processing")
    print("="*70)
    
    # Mock data for demonstration
    mock_articles = [
        {
            "pmid": "12345678",
            "title": "Efficacy of Novel Diabetes Treatment",
            "abstract": "BACKGROUND: Diabetes management remains challenging. "
                       "METHODS: We conducted a randomized controlled trial. "
                       "RESULTS: The study showed significant improvement in glycemic control "
                       "with 95% confidence interval. "
                       "CONCLUSION: The treatment demonstrates efficacy and safety.",
            "authors": ["Smith J", "Jones A", "Brown B", "Wilson C", "Davis D"],
            "publication_date": "2023-06-15",
            "journal": "New England Journal of Medicine",
            "keywords": ["diabetes", "glycemic control", "randomized controlled trial", "treatment", "efficacy"]
        },
        {
            "pmid": "87654321",
            "title": "Long-term Outcomes of Diabetes Management Programs",
            "abstract": "Study demonstrated improved patient outcomes with comprehensive diabetes care programs.",
            "authors": ["Johnson M", "Williams R"],
            "publication_date": "2022-03-10",
            "journal": "Diabetes Care",
            "keywords": ["diabetes", "outcomes", "management"]
        }
    ]
    
    # Process evidence
    processor = EvidenceProcessor()
    processed = processor.extract_key_findings(mock_articles)
    
    print("\nProcessed Articles:")
    for evidence in processed:
        print(f"\n  PMID: {evidence['pmid']}")
        print(f"  Quality: {evidence['evidence_quality']}")
        print(f"  Relevance: {evidence['relevance_score']:.2f}")
        print(f"  Key Findings: {len(evidence['key_findings'])}")
    
    # Synthesize evidence
    synthesis = processor.synthesize_evidence(processed, "Diabetes Management")
    
    print(f"\nEvidence Synthesis:")
    print(f"  Total Articles: {synthesis['total_articles']}")
    print(f"  High Quality: {synthesis['high_quality_count']}")
    print(f"  Summary: {synthesis['summary']}")
    
    return synthesis


def example_policy_generation(evidence_synthesis):
    """Example: Generate policy draft."""
    print("\n" + "="*70)
    print("EXAMPLE 3: Policy Generation")
    print("="*70)
    
    # Generate policy
    generator = PolicyGenerator()
    draft = generator.generate_policy_draft(
        evidence_synthesis,
        policy_type="clinical_policy"
    )
    
    print("\nGenerated Policy:")
    print(f"  Policy ID: {draft['components']['policy_number']}")
    print(f"  Title: {draft['components']['title']}")
    print(f"  Type: {draft['policy_type']}")
    print(f"  Evidence Count: {draft['metadata']['evidence_count']}")
    
    print("\nPolicy Statement (excerpt):")
    statement = draft['components']['policy_statement']
    print(f"  {statement[:200]}...")
    
    return draft


def example_compliance_validation(policy_draft):
    """Example: Validate compliance."""
    print("\n" + "="*70)
    print("EXAMPLE 4: Compliance Validation")
    print("="*70)
    
    # Validate policy
    validator = ComplianceValidator()
    results = validator.validate_policy(policy_draft)
    
    print("\nValidation Results:")
    print(f"  Overall Status: {results['overall_status']}")
    print(f"  Compliance Score: {results['compliance_score']:.2%}")
    
    print("\n  Framework Results:")
    for framework, result in results['framework_results'].items():
        print(f"    {framework}: {result['status']}")
        print(f"      Checks Passed: {result['checks_passed']}")
        print(f"      Checks Failed: {result['checks_failed']}")
    
    if results['issues']:
        print(f"\n  Issues Found ({len(results['issues'])}):")
        for issue in results['issues'][:3]:  # Show first 3
            print(f"    - {issue}")
    
    if results['recommendations']:
        print(f"\n  Recommendations:")
        for rec in results['recommendations'][:3]:  # Show first 3
            print(f"    - {rec}")
    
    return results


def example_export(policy_draft):
    """Example: Export policy."""
    print("\n" + "="*70)
    print("EXAMPLE 5: Export Policy")
    print("="*70)
    
    from policy_drafting.integration import DashboardExporter
    import tempfile
    
    # Export in multiple formats
    with tempfile.TemporaryDirectory() as tmpdir:
        exporter = DashboardExporter(export_dir=tmpdir)
        
        # Export as JSON
        json_file = exporter.export_policy_draft(policy_draft, format="json")
        print(f"\n  Exported JSON: {json_file}")
        
        # Export as Markdown
        md_file = exporter.export_policy_draft(policy_draft, format="markdown")
        print(f"  Exported Markdown: {md_file}")
        
        # Generate API payload
        payload = exporter.generate_api_payload(policy_draft)
        print(f"\n  API Payload Generated:")
        print(f"    Policy ID: {payload['policy']['id']}")
        print(f"    Title: {payload['policy']['title']}")
        print(f"    Type: {payload['policy']['type']}")


def main():
    """Run all examples."""
    print("\n" + "="*70)
    print("HEALTHCARE POLICY DRAFTING SYSTEM - EXAMPLES")
    print("="*70)
    
    # Example 1: Full workflow (conceptual)
    example_full_workflow()
    
    # Example 2: Evidence extraction and processing
    synthesis = example_evidence_extraction()
    
    # Example 3: Policy generation
    draft = example_policy_generation(synthesis)
    
    # Example 4: Compliance validation
    validation = example_compliance_validation(draft)
    
    # Example 5: Export
    example_export(draft)
    
    print("\n" + "="*70)
    print("EXAMPLES COMPLETED")
    print("="*70)
    print("\nFor more information, see:")
    print("  - README.md for usage instructions")
    print("  - docs/API_DOCUMENTATION.md for API details")
    print("  - docs/DEVELOPER_GUIDE.md for development guide")
    print()


if __name__ == "__main__":
    main()
