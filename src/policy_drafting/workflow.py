"""Main workflow orchestrator for policy drafting system."""

from typing import Dict, Optional
from loguru import logger

from .evidence.pubmed_client import PubMedClient
from .evidence.evidence_processor import EvidenceProcessor
from .models.policy_generator import PolicyGenerator
from .compliance.validator import ComplianceValidator
from .explainability.audit_logger import AuditLogger
from .integration.dashboard_exporter import DashboardExporter


class PolicyDraftingWorkflow:
    """Orchestrate the complete policy drafting workflow."""
    
    def __init__(
        self,
        pubmed_email: Optional[str] = None,
        openai_api_key: Optional[str] = None
    ):
        """
        Initialize workflow components.
        
        Args:
            pubmed_email: Email for PubMed API
            openai_api_key: API key for OpenAI
        """
        self.pubmed_client = PubMedClient(email=pubmed_email)
        self.evidence_processor = EvidenceProcessor()
        self.policy_generator = PolicyGenerator(api_key=openai_api_key)
        self.compliance_validator = ComplianceValidator()
        self.audit_logger = AuditLogger()
        self.dashboard_exporter = DashboardExporter()
        
        logger.info("Policy drafting workflow initialized")
    
    def execute_full_workflow(
        self,
        topic: str,
        max_articles: int = 20,
        policy_type: str = "clinical_policy"
    ) -> Dict:
        """
        Execute the complete policy drafting workflow.
        
        Args:
            topic: Medical topic for policy
            max_articles: Maximum number of articles to retrieve
            policy_type: Type of policy to generate
            
        Returns:
            Complete workflow results
        """
        logger.info(f"Starting workflow for topic: {topic}")
        
        # Step 1: Extract evidence
        logger.info("Step 1: Extracting evidence from PubMed")
        articles = self.pubmed_client.search_and_fetch(topic, max_articles)
        self.audit_logger.log_evidence_extraction(
            query=topic,
            article_count=len(articles),
            source="pubmed"
        )
        
        if not articles:
            logger.error("No articles found")
            return {"error": "No articles found for the given topic"}
        
        # Step 2: Process evidence
        logger.info("Step 2: Processing and synthesizing evidence")
        processed_evidence = self.evidence_processor.extract_key_findings(articles)
        evidence_synthesis = self.evidence_processor.synthesize_evidence(
            processed_evidence,
            topic
        )
        self.audit_logger.log_evidence_processing(
            articles_processed=len(processed_evidence),
            high_quality_count=evidence_synthesis.get("high_quality_count", 0),
            synthesis_topic=topic
        )
        
        # Step 3: Generate policy draft
        logger.info("Step 3: Generating policy draft")
        policy_draft = self.policy_generator.generate_policy_draft(
            evidence_synthesis,
            policy_type=policy_type
        )
        policy_id = policy_draft["components"]["policy_number"]
        self.audit_logger.log_policy_generation(
            policy_type=policy_type,
            model_used=self.policy_generator.model_name,
            evidence_count=len(articles),
            policy_id=policy_id
        )
        
        # Step 4: Validate compliance
        logger.info("Step 4: Validating compliance")
        validation_results = self.compliance_validator.validate_policy(policy_draft)
        evidence_validation = self.compliance_validator.validate_evidence_quality(
            evidence_synthesis
        )
        validation_results["evidence_validation"] = evidence_validation
        
        self.audit_logger.log_compliance_validation(
            policy_id=policy_id,
            validation_status=validation_results["overall_status"],
            compliance_score=validation_results["compliance_score"],
            issues_count=len(validation_results["issues"])
        )
        
        # Step 5: Generate audit report
        logger.info("Step 5: Generating audit report")
        audit_report = self.audit_logger.generate_audit_report()
        
        # Step 6: Export results
        logger.info("Step 6: Exporting results")
        package_dir = self.dashboard_exporter.create_dashboard_package(
            policy_draft,
            validation_results,
            audit_report
        )
        self.audit_logger.log_export(
            policy_id=policy_id,
            export_format="package",
            destination=package_dir
        )
        
        # Compile results
        workflow_results = {
            "status": "completed",
            "topic": topic,
            "policy_draft": policy_draft,
            "validation_results": validation_results,
            "audit_report": audit_report,
            "export_location": package_dir,
            "summary": {
                "articles_found": len(articles),
                "high_quality_evidence": evidence_synthesis.get("high_quality_count", 0),
                "policy_id": policy_id,
                "compliance_status": validation_results["overall_status"],
                "compliance_score": validation_results["compliance_score"],
            }
        }
        
        logger.info(f"Workflow completed successfully. Policy ID: {policy_id}")
        return workflow_results
    
    def generate_policy_from_evidence(
        self,
        evidence_synthesis: Dict,
        policy_type: str = "clinical_policy"
    ) -> Dict:
        """
        Generate policy from pre-synthesized evidence.
        
        Args:
            evidence_synthesis: Pre-synthesized evidence
            policy_type: Type of policy to generate
            
        Returns:
            Policy draft and validation results
        """
        logger.info("Generating policy from provided evidence")
        
        # Generate policy
        policy_draft = self.policy_generator.generate_policy_draft(
            evidence_synthesis,
            policy_type=policy_type
        )
        
        # Validate
        validation_results = self.compliance_validator.validate_policy(policy_draft)
        
        return {
            "policy_draft": policy_draft,
            "validation_results": validation_results,
        }
    
    def validate_existing_policy(self, policy_draft: Dict) -> Dict:
        """
        Validate an existing policy draft.
        
        Args:
            policy_draft: Policy draft to validate
            
        Returns:
            Validation results
        """
        logger.info("Validating existing policy")
        return self.compliance_validator.validate_policy(policy_draft)
