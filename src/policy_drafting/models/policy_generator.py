"""Policy generator using AI models for drafting healthcare policies."""

import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from loguru import logger


class PolicyGenerator:
    """Generate healthcare policy drafts using AI models."""
    
    def __init__(
        self,
        model_name: str = "gpt-4",
        api_key: Optional[str] = None,
        temperature: float = 0.7
    ):
        """
        Initialize policy generator.
        
        Args:
            model_name: Name of the AI model to use
            api_key: API key for the AI service
            temperature: Temperature for generation (0.0-1.0)
        """
        self.model_name = model_name
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.temperature = temperature
        self.policy_templates = self._load_templates()
        logger.info(f"Policy generator initialized with model: {model_name}")
    
    def _load_templates(self) -> Dict[str, str]:
        """
        Load policy templates.
        
        Returns:
            Dictionary of templates
        """
        return {
            "clinical_policy": """
# Clinical Policy: {title}

## Policy Number
{policy_number}

## Effective Date
{effective_date}

## Policy Statement
{policy_statement}

## Rationale
{rationale}

## Evidence Base
{evidence_base}

## Clinical Guidelines
{clinical_guidelines}

## Compliance Requirements
{compliance_requirements}

## References
{references}

## Approval and Review
- Last Reviewed: {review_date}
- Next Review: {next_review_date}
- Approved By: Medical Affairs Committee
""",
            "coverage_policy": """
# Coverage Policy: {title}

## Policy Overview
{overview}

## Coverage Criteria
{criteria}

## Evidence Summary
{evidence_summary}

## Regulatory Alignment
{regulatory_alignment}

## Implementation Guidelines
{implementation}

## References
{references}
""",
        }
    
    def generate_policy_draft(
        self,
        evidence_synthesis: Dict,
        policy_type: str = "clinical_policy",
        additional_context: Optional[Dict] = None
    ) -> Dict:
        """
        Generate a policy draft based on evidence synthesis.
        
        Args:
            evidence_synthesis: Synthesized evidence data
            policy_type: Type of policy to generate
            additional_context: Additional context for generation
            
        Returns:
            Generated policy draft
        """
        logger.info(f"Generating {policy_type} draft")
        
        # Prepare context
        context = {
            "evidence": evidence_synthesis,
            "additional": additional_context or {},
            "generation_date": datetime.now().isoformat(),
        }
        
        # Generate policy components
        policy_content = {
            "title": self._generate_title(evidence_synthesis),
            "policy_number": self._generate_policy_number(),
            "effective_date": datetime.now().strftime("%Y-%m-%d"),
            "policy_statement": self._generate_policy_statement(evidence_synthesis),
            "rationale": self._generate_rationale(evidence_synthesis),
            "evidence_base": self._format_evidence_base(evidence_synthesis),
            "clinical_guidelines": self._generate_clinical_guidelines(evidence_synthesis),
            "compliance_requirements": self._generate_compliance_requirements(evidence_synthesis),
            "references": self._format_references(evidence_synthesis),
            "review_date": datetime.now().strftime("%Y-%m-%d"),
            "next_review_date": self._calculate_next_review_date(),
        }
        
        # Fill template
        template = self.policy_templates.get(policy_type, self.policy_templates["clinical_policy"])
        draft_text = template.format(**policy_content)
        
        draft = {
            "policy_type": policy_type,
            "content": draft_text,
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "model": self.model_name,
                "evidence_count": evidence_synthesis.get("total_articles", 0),
                "high_quality_evidence": evidence_synthesis.get("high_quality_count", 0),
            },
            "components": policy_content,
            "raw_evidence": evidence_synthesis,
        }
        
        logger.info(f"Policy draft generated successfully")
        return draft
    
    def _generate_title(self, evidence_synthesis: Dict) -> str:
        """Generate policy title based on evidence topic."""
        topic = evidence_synthesis.get("topic", "Healthcare Policy")
        return f"{topic} - Clinical Guidelines and Coverage Policy"
    
    def _generate_policy_number(self) -> str:
        """Generate a unique policy number."""
        timestamp = datetime.now().strftime("%Y%m%d")
        return f"POL-{timestamp}-001"
    
    def _generate_policy_statement(self, evidence_synthesis: Dict) -> str:
        """
        Generate the main policy statement.
        
        Args:
            evidence_synthesis: Synthesized evidence
            
        Returns:
            Policy statement text
        """
        topic = evidence_synthesis.get("topic", "the specified condition")
        total_articles = evidence_synthesis.get("total_articles", 0)
        high_quality = evidence_synthesis.get("high_quality_count", 0)
        
        statement = f"""
This policy establishes clinical guidelines for {topic} based on comprehensive 
evidence review of {total_articles} peer-reviewed studies, including {high_quality} 
high-quality research articles. The policy aims to ensure evidence-based, safe, 
and effective care delivery while maintaining compliance with regulatory standards.
"""
        return statement.strip()
    
    def _generate_rationale(self, evidence_synthesis: Dict) -> str:
        """
        Generate rationale section.
        
        Args:
            evidence_synthesis: Synthesized evidence
            
        Returns:
            Rationale text
        """
        summary = evidence_synthesis.get("summary", "")
        findings = evidence_synthesis.get("key_findings", [])
        
        rationale = f"""
{summary}

Key Evidence Supporting This Policy:
"""
        for i, finding in enumerate(findings[:5], 1):
            rationale += f"\n{i}. {finding}"
        
        return rationale.strip()
    
    def _format_evidence_base(self, evidence_synthesis: Dict) -> str:
        """
        Format evidence base section.
        
        Args:
            evidence_synthesis: Synthesized evidence
            
        Returns:
            Formatted evidence base
        """
        evidence_base = evidence_synthesis.get("evidence_base", {})
        high_quality = evidence_base.get("high_quality", [])
        
        formatted = "## Primary Evidence Sources\n\n"
        
        for i, evidence in enumerate(high_quality, 1):
            formatted += f"{i}. {evidence.get('title', 'Untitled')} (PMID: {evidence.get('pmid', 'N/A')})\n"
            findings = evidence.get('findings', [])
            if findings:
                formatted += "   Key Findings:\n"
                for finding in findings[:3]:
                    formatted += f"   - {finding}\n"
            formatted += "\n"
        
        return formatted.strip()
    
    def _generate_clinical_guidelines(self, evidence_synthesis: Dict) -> str:
        """
        Generate clinical guidelines section.
        
        Args:
            evidence_synthesis: Synthesized evidence
            
        Returns:
            Clinical guidelines text
        """
        guidelines = """
Based on the evidence reviewed, the following clinical guidelines are recommended:

1. **Assessment and Diagnosis**
   - Utilize evidence-based diagnostic criteria
   - Consider patient-specific factors and comorbidities
   - Document all clinical findings comprehensively

2. **Treatment Approach**
   - Follow evidence-based treatment protocols
   - Monitor patient response and adjust as needed
   - Consider alternative options for non-responders

3. **Monitoring and Follow-up**
   - Establish regular monitoring schedule
   - Track outcomes and adverse events
   - Adjust treatment plan based on clinical response

4. **Documentation Requirements**
   - Maintain complete clinical records
   - Document rationale for treatment decisions
   - Record patient consent and education
"""
        return guidelines.strip()
    
    def _generate_compliance_requirements(self, evidence_synthesis: Dict) -> str:
        """
        Generate compliance requirements section.
        
        Args:
            evidence_synthesis: Synthesized evidence
            
        Returns:
            Compliance requirements text
        """
        requirements = """
This policy must comply with:

1. **Regulatory Standards**
   - FDA guidelines for medical devices and medications
   - CMS coverage policies and requirements
   - State-specific healthcare regulations

2. **Quality Standards**
   - Joint Commission standards
   - National Quality Forum measures
   - Evidence-based clinical practice guidelines

3. **Privacy and Security**
   - HIPAA compliance for patient data
   - Secure documentation and communication
   - Patient consent and authorization

4. **Ethical Considerations**
   - Informed consent procedures
   - Patient autonomy and shared decision-making
   - Equitable access to care
"""
        return requirements.strip()
    
    def _format_references(self, evidence_synthesis: Dict) -> str:
        """
        Format references section.
        
        Args:
            evidence_synthesis: Synthesized evidence
            
        Returns:
            Formatted references
        """
        evidence_base = evidence_synthesis.get("evidence_base", {})
        high_quality = evidence_base.get("high_quality", [])
        supporting = evidence_base.get("supporting_evidence", [])
        
        references = ""
        ref_num = 1
        
        for evidence in high_quality:
            references += f"{ref_num}. {evidence.get('title', 'Untitled')} - PMID: {evidence.get('pmid', 'N/A')}\n"
            ref_num += 1
        
        for evidence in supporting[:5]:
            references += f"{ref_num}. {evidence.get('title', 'Untitled')} - PMID: {evidence.get('pmid', 'N/A')}\n"
            ref_num += 1
        
        return references.strip()
    
    def _calculate_next_review_date(self) -> str:
        """Calculate next policy review date (1 year from now)."""
        next_review = datetime.now() + timedelta(days=365)
        return next_review.strftime("%Y-%m-%d")
    
    def refine_policy_draft(
        self,
        draft: Dict,
        feedback: List[str]
    ) -> Dict:
        """
        Refine policy draft based on feedback.
        
        Args:
            draft: Original policy draft
            feedback: List of feedback items
            
        Returns:
            Refined policy draft
        """
        logger.info("Refining policy draft based on feedback")
        
        # In a real implementation, this would use AI to incorporate feedback
        # For now, we add feedback as a revision note
        
        refined = draft.copy()
        refined["metadata"]["revised_at"] = datetime.now().isoformat()
        refined["metadata"]["revision_feedback"] = feedback
        
        return refined
