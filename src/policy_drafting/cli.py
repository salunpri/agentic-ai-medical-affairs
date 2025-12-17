#!/usr/bin/env python3
"""Command-line interface for the policy drafting system."""

import argparse
import json
import sys
from pathlib import Path

# Only add parent directory to path if package not installed
try:
    import policy_drafting
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent.parent))

from policy_drafting.workflow import PolicyDraftingWorkflow
from policy_drafting.integration.dashboard_exporter import DashboardExporter
from loguru import logger


def setup_logging(verbose: bool = False):
    """Setup logging configuration."""
    logger.remove()
    if verbose:
        logger.add(sys.stderr, level="DEBUG")
    else:
        logger.add(sys.stderr, level="INFO")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Healthcare Policy Drafting System - Generate and validate policy drafts"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Generate policy command
    generate_parser = subparsers.add_parser(
        "generate",
        help="Generate a new policy draft"
    )
    generate_parser.add_argument(
        "topic",
        help="Medical topic for the policy (e.g., 'diabetes management')"
    )
    generate_parser.add_argument(
        "--max-articles",
        type=int,
        default=20,
        help="Maximum number of articles to retrieve (default: 20)"
    )
    generate_parser.add_argument(
        "--policy-type",
        choices=["clinical_policy", "coverage_policy"],
        default="clinical_policy",
        help="Type of policy to generate (default: clinical_policy)"
    )
    generate_parser.add_argument(
        "--pubmed-email",
        help="Email for PubMed API"
    )
    generate_parser.add_argument(
        "--output",
        help="Output file for results (JSON format)"
    )
    
    # Validate policy command
    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate an existing policy draft"
    )
    validate_parser.add_argument(
        "policy_file",
        help="Path to policy draft JSON file"
    )
    
    # Export policy command
    export_parser = subparsers.add_parser(
        "export",
        help="Export policy draft to different formats"
    )
    export_parser.add_argument(
        "policy_file",
        help="Path to policy draft JSON file"
    )
    export_parser.add_argument(
        "--format",
        choices=["json", "markdown", "html"],
        default="markdown",
        help="Export format (default: markdown)"
    )
    export_parser.add_argument(
        "--output-dir",
        help="Output directory for exports"
    )
    
    # Common arguments
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        if args.command == "generate":
            return generate_policy(args)
        elif args.command == "validate":
            return validate_policy(args)
        elif args.command == "export":
            return export_policy(args)
    except Exception as e:
        logger.error(f"Error executing command: {e}")
        if args.verbose:
            raise
        return 1
    
    return 0


def generate_policy(args):
    """Generate a new policy draft."""
    logger.info(f"Generating policy for topic: {args.topic}")
    
    # Initialize workflow
    workflow = PolicyDraftingWorkflow(
        pubmed_email=args.pubmed_email
    )
    
    # Execute workflow
    results = workflow.execute_full_workflow(
        topic=args.topic,
        max_articles=args.max_articles,
        policy_type=args.policy_type
    )
    
    if "error" in results:
        logger.error(f"Workflow failed: {results['error']}")
        return 1
    
    # Display summary
    summary = results["summary"]
    print("\n" + "=" * 70)
    print("POLICY GENERATION COMPLETED")
    print("=" * 70)
    print(f"Topic: {results['topic']}")
    print(f"Policy ID: {summary['policy_id']}")
    print(f"Articles Found: {summary['articles_found']}")
    print(f"High Quality Evidence: {summary['high_quality_evidence']}")
    print(f"Compliance Status: {summary['compliance_status']}")
    print(f"Compliance Score: {summary['compliance_score']:.2%}")
    print(f"Export Location: {results['export_location']}")
    print("=" * 70 + "\n")
    
    # Save results if output file specified
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        logger.info(f"Results saved to: {args.output}")
    
    return 0


def validate_policy(args):
    """Validate an existing policy draft."""
    logger.info(f"Validating policy: {args.policy_file}")
    
    # Load policy
    with open(args.policy_file, 'r') as f:
        policy_draft = json.load(f)
    
    # Initialize workflow
    workflow = PolicyDraftingWorkflow()
    
    # Validate
    validation_results = workflow.validate_existing_policy(policy_draft)
    
    # Display results
    print("\n" + "=" * 70)
    print("VALIDATION RESULTS")
    print("=" * 70)
    print(f"Overall Status: {validation_results['overall_status']}")
    print(f"Compliance Score: {validation_results['compliance_score']:.2%}")
    
    if validation_results["issues"]:
        print(f"\nIssues Found ({len(validation_results['issues'])}):")
        for i, issue in enumerate(validation_results["issues"], 1):
            print(f"  {i}. {issue}")
    
    if validation_results["warnings"]:
        print(f"\nWarnings ({len(validation_results['warnings'])}):")
        for i, warning in enumerate(validation_results["warnings"], 1):
            print(f"  {i}. {warning}")
    
    if validation_results["recommendations"]:
        print(f"\nRecommendations:")
        for i, rec in enumerate(validation_results["recommendations"], 1):
            print(f"  {i}. {rec}")
    
    print("=" * 70 + "\n")
    
    return 0


def export_policy(args):
    """Export policy draft to different formats."""
    logger.info(f"Exporting policy: {args.policy_file}")
    
    # Load policy
    with open(args.policy_file, 'r') as f:
        policy_draft = json.load(f)
    
    # Initialize exporter
    exporter = DashboardExporter(export_dir=args.output_dir)
    
    # Export
    output_file = exporter.export_policy_draft(
        policy_draft,
        format=args.format
    )
    
    print(f"\nPolicy exported to: {output_file}\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
