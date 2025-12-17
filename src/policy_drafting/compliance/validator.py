"""Compliance validator for healthcare policy validation."""

from typing import Dict, List
from datetime import datetime
from loguru import logger


class ComplianceValidator:
    """Validate healthcare policies against regulatory frameworks."""
    
    def __init__(self):
        """Initialize compliance validator."""
        self.validation_rules = self._load_validation_rules()
        logger.info("Compliance validator initialized")
    
    def _load_validation_rules(self) -> Dict:
        """
        Load validation rules for different regulatory frameworks.
        
        Returns:
            Dictionary of validation rules
        """
        return {
            "fda_guidelines": {
                "required_sections": [
                    "policy_statement",
                    "rationale",
                    "evidence_base",
                    "references",
                ],
                "keywords": [
                    "fda approved",
                    "clinical trial",
                    "safety",
                    "efficacy",
                ],
            },
            "cms_requirements": {
                "required_sections": [
                    "coverage_criteria",
                    "evidence_summary",
                    "implementation",
                ],
                "keywords": [
                    "medically necessary",
                    "coverage",
                    "reimbursement",
                ],
            },
            "hipaa_compliance": {
                "required_sections": [
                    "privacy",
                    "security",
                    "patient_consent",
                ],
                "keywords": [
                    "hipaa",
                    "privacy",
                    "protected health information",
                    "phi",
                    "consent",
                ],
            },
            "clinical_standards": {
                "required_sections": [
                    "clinical_guidelines",
                    "evidence_base",
                    "monitoring",
                ],
                "keywords": [
                    "evidence-based",
                    "clinical practice",
                    "patient safety",
                    "quality",
                ],
            },
        }
    
    def validate_policy(self, policy_draft: Dict) -> Dict:
        """
        Validate policy draft against all regulatory frameworks.
        
        Args:
            policy_draft: Policy draft to validate
            
        Returns:
            Validation results
        """
        logger.info("Validating policy draft")
        
        results = {
            "overall_status": "pending",
            "validation_timestamp": datetime.now().isoformat(),
            "framework_results": {},
            "issues": [],
            "warnings": [],
            "recommendations": [],
            "compliance_score": 0.0,
        }
        
        content = policy_draft.get("content", "").lower()
        components = policy_draft.get("components", {})
        
        # Validate against each framework
        for framework_name, rules in self.validation_rules.items():
            framework_result = self._validate_framework(
                framework_name, rules, content, components
            )
            results["framework_results"][framework_name] = framework_result
            
            # Collect issues and warnings
            results["issues"].extend(framework_result.get("issues", []))
            results["warnings"].extend(framework_result.get("warnings", []))
        
        # Calculate overall compliance score
        results["compliance_score"] = self._calculate_compliance_score(
            results["framework_results"]
        )
        
        # Determine overall status
        if results["compliance_score"] >= 0.9:
            results["overall_status"] = "compliant"
        elif results["compliance_score"] >= 0.7:
            results["overall_status"] = "needs_review"
        else:
            results["overall_status"] = "non_compliant"
        
        # Generate recommendations
        results["recommendations"] = self._generate_recommendations(results)
        
        logger.info(
            f"Validation complete. Status: {results['overall_status']}, "
            f"Score: {results['compliance_score']:.2f}"
        )
        
        return results
    
    def _validate_framework(
        self,
        framework_name: str,
        rules: Dict,
        content: str,
        components: Dict
    ) -> Dict:
        """
        Validate against a specific regulatory framework.
        
        Args:
            framework_name: Name of the framework
            rules: Validation rules for the framework
            content: Policy content text
            components: Policy components dictionary
            
        Returns:
            Framework validation result
        """
        result = {
            "framework": framework_name,
            "status": "pass",
            "issues": [],
            "warnings": [],
            "checks_passed": 0,
            "checks_failed": 0,
        }
        
        # Check required sections
        required_sections = rules.get("required_sections", [])
        for section in required_sections:
            if section not in components or not components[section]:
                result["issues"].append(
                    f"Missing required section: {section} for {framework_name}"
                )
                result["checks_failed"] += 1
            else:
                result["checks_passed"] += 1
        
        # Check for required keywords
        keywords = rules.get("keywords", [])
        found_keywords = []
        for keyword in keywords:
            if keyword in content:
                found_keywords.append(keyword)
        
        if found_keywords:
            result["checks_passed"] += 1
        else:
            result["warnings"].append(
                f"No {framework_name} keywords found in policy. "
                f"Consider including: {', '.join(keywords[:3])}"
            )
        
        # Set status
        if result["checks_failed"] > 0:
            result["status"] = "fail"
        elif result["warnings"]:
            result["status"] = "warning"
        
        return result
    
    def _calculate_compliance_score(self, framework_results: Dict) -> float:
        """
        Calculate overall compliance score.
        
        Args:
            framework_results: Results from all framework validations
            
        Returns:
            Compliance score (0.0 to 1.0)
        """
        if not framework_results:
            return 0.0
        
        total_passed = 0
        total_checks = 0
        
        for result in framework_results.values():
            total_passed += result.get("checks_passed", 0)
            total_checks += (
                result.get("checks_passed", 0) + result.get("checks_failed", 0)
            )
        
        if total_checks == 0:
            return 0.0
        
        return total_passed / total_checks
    
    def _generate_recommendations(self, validation_results: Dict) -> List[str]:
        """
        Generate recommendations based on validation results.
        
        Args:
            validation_results: Complete validation results
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Recommendations based on issues
        issues = validation_results.get("issues", [])
        if issues:
            recommendations.append(
                "Address all identified issues to achieve compliance."
            )
            
            # Group issues by type
            missing_sections = [
                issue for issue in issues if "Missing required section" in issue
            ]
            if missing_sections:
                recommendations.append(
                    "Add all required policy sections as specified by regulatory frameworks."
                )
        
        # Recommendations based on warnings
        warnings = validation_results.get("warnings", [])
        if warnings:
            recommendations.append(
                "Review warnings and consider incorporating suggested improvements."
            )
        
        # Recommendations based on score
        score = validation_results.get("compliance_score", 0.0)
        if score < 0.7:
            recommendations.append(
                "Policy requires significant revision to meet compliance standards."
            )
        elif score < 0.9:
            recommendations.append(
                "Policy meets basic requirements but could be strengthened."
            )
        
        # General recommendations
        if not recommendations:
            recommendations.append(
                "Policy meets compliance standards. Proceed with review and approval."
            )
        
        return recommendations
    
    def validate_evidence_quality(self, evidence_synthesis: Dict) -> Dict:
        """
        Validate the quality of evidence used in policy.
        
        Args:
            evidence_synthesis: Synthesized evidence data
            
        Returns:
            Evidence quality validation result
        """
        result = {
            "status": "pass",
            "issues": [],
            "warnings": [],
            "evidence_quality_score": 0.0,
        }
        
        total_articles = evidence_synthesis.get("total_articles", 0)
        high_quality = evidence_synthesis.get("high_quality_count", 0)
        
        if total_articles == 0:
            result["status"] = "fail"
            result["issues"].append("No evidence articles found.")
            return result
        
        # Calculate evidence quality score
        if total_articles > 0:
            result["evidence_quality_score"] = high_quality / total_articles
        
        # Check minimum evidence requirements
        if total_articles < 5:
            result["warnings"].append(
                f"Limited evidence base ({total_articles} articles). "
                "Consider expanding evidence search."
            )
        
        if high_quality == 0:
            result["warnings"].append(
                "No high-quality evidence found. Policy may lack strong support."
            )
        elif high_quality < 3:
            result["warnings"].append(
                f"Only {high_quality} high-quality article(s) found. "
                "Consider seeking additional high-quality evidence."
            )
        
        # Set final status
        if result["evidence_quality_score"] < 0.3 and total_articles < 5:
            result["status"] = "fail"
            result["issues"].append(
                "Insufficient high-quality evidence to support policy."
            )
        elif result["warnings"]:
            result["status"] = "warning"
        
        logger.info(f"Evidence quality validation: {result['status']}")
        return result
    
    def check_regulatory_alignment(
        self,
        policy_draft: Dict,
        specific_regulations: List[str]
    ) -> Dict:
        """
        Check alignment with specific regulations.
        
        Args:
            policy_draft: Policy draft to check
            specific_regulations: List of specific regulations to check
            
        Returns:
            Regulatory alignment result
        """
        result = {
            "aligned": [],
            "not_aligned": [],
            "partial_alignment": [],
        }
        
        content = policy_draft.get("content", "").lower()
        
        for regulation in specific_regulations:
            reg_lower = regulation.lower()
            if reg_lower in content:
                result["aligned"].append(regulation)
            else:
                result["not_aligned"].append(regulation)
        
        logger.info(
            f"Regulatory alignment: {len(result['aligned'])} aligned, "
            f"{len(result['not_aligned'])} not aligned"
        )
        
        return result
