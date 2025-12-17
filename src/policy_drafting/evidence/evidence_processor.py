"""Evidence processor for extracting and preprocessing medical data."""

from typing import List, Dict, Optional
from datetime import datetime
import re
from loguru import logger


class EvidenceProcessor:
    """Process and extract relevant evidence from medical research articles."""
    
    def __init__(self):
        """Initialize evidence processor."""
        self.evidence_cache = {}
        logger.info("Evidence processor initialized")
    
    def extract_key_findings(self, articles: List[Dict]) -> List[Dict]:
        """
        Extract key findings from articles.
        
        Args:
            articles: List of article dictionaries
            
        Returns:
            List of processed evidence with key findings
        """
        processed_evidence = []
        
        for article in articles:
            try:
                evidence = {
                    "pmid": article.get("pmid", ""),
                    "title": article.get("title", ""),
                    "authors": article.get("authors", []),
                    "publication_date": article.get("publication_date", ""),
                    "journal": article.get("journal", ""),
                    "keywords": article.get("keywords", []),
                    "abstract": article.get("abstract", ""),
                    "key_findings": self._extract_findings_from_abstract(
                        article.get("abstract", "")
                    ),
                    "evidence_quality": self._assess_evidence_quality(article),
                    "relevance_score": self._calculate_relevance(article),
                }
                
                processed_evidence.append(evidence)
                
            except Exception as e:
                logger.warning(f"Error processing article {article.get('pmid', 'unknown')}: {e}")
                continue
        
        logger.info(f"Processed {len(processed_evidence)} articles")
        return processed_evidence
    
    def _extract_findings_from_abstract(self, abstract: str) -> List[str]:
        """
        Extract key findings from abstract text.
        
        Args:
            abstract: Abstract text
            
        Returns:
            List of key findings
        """
        if not abstract:
            return []
        
        findings = []
        
        # Split by common section markers
        sections = re.split(
            r'(?:BACKGROUND:|OBJECTIVE:|METHODS:|RESULTS:|CONCLUSION:|CONCLUSIONS:)',
            abstract,
            flags=re.IGNORECASE
        )
        
        # Focus on results and conclusions
        for section in sections:
            if len(section.strip()) > 50:  # Meaningful content
                # Extract sentences with findings keywords
                sentences = re.split(r'[.!?]', section)
                for sentence in sentences:
                    if any(keyword in sentence.lower() for keyword in [
                        'showed', 'demonstrated', 'found', 'revealed',
                        'indicated', 'suggests', 'associated with',
                        'resulted in', 'significantly', 'effective'
                    ]):
                        findings.append(sentence.strip())
        
        return findings[:5]  # Top 5 findings
    
    def _assess_evidence_quality(self, article: Dict) -> str:
        """
        Assess the quality of evidence based on article metadata.
        
        Args:
            article: Article dictionary
            
        Returns:
            Quality rating (high, medium, low)
        """
        score = 0
        
        # Check for recent publication
        pub_date = article.get("publication_date", "")
        if pub_date:
            try:
                year = int(pub_date.split("-")[0])
                current_year = datetime.now().year
                if current_year - year <= 3:
                    score += 2
                elif current_year - year <= 5:
                    score += 1
            except:
                pass
        
        # Check for abstract completeness
        abstract = article.get("abstract", "")
        if len(abstract) > 500:
            score += 2
        elif len(abstract) > 200:
            score += 1
        
        # Check for keywords
        if len(article.get("keywords", [])) >= 5:
            score += 1
        
        # Check for author count (more authors may indicate larger study)
        if len(article.get("authors", [])) >= 5:
            score += 1
        
        if score >= 5:
            return "high"
        elif score >= 3:
            return "medium"
        else:
            return "low"
    
    def _calculate_relevance(self, article: Dict) -> float:
        """
        Calculate relevance score for the article.
        
        Args:
            article: Article dictionary
            
        Returns:
            Relevance score (0.0 to 1.0)
        """
        score = 0.5  # Base score
        
        # Check for clinical trial or systematic review
        title = article.get("title", "").lower()
        abstract = article.get("abstract", "").lower()
        
        if any(term in title or term in abstract for term in [
            "randomized controlled trial", "rct", "systematic review",
            "meta-analysis", "clinical trial"
        ]):
            score += 0.3
        
        # Check for statistical significance
        if any(term in abstract for term in [
            "p <", "p<", "statistically significant", "confidence interval"
        ]):
            score += 0.2
        
        return min(score, 1.0)
    
    def synthesize_evidence(
        self,
        processed_evidence: List[Dict],
        topic: str
    ) -> Dict:
        """
        Synthesize evidence into a structured summary.
        
        Args:
            processed_evidence: List of processed evidence
            topic: Topic for synthesis
            
        Returns:
            Synthesized evidence summary
        """
        high_quality = [e for e in processed_evidence if e["evidence_quality"] == "high"]
        medium_quality = [e for e in processed_evidence if e["evidence_quality"] == "medium"]
        low_quality = [e for e in processed_evidence if e["evidence_quality"] == "low"]
        
        all_findings = []
        for evidence in processed_evidence:
            all_findings.extend(evidence.get("key_findings", []))
        
        synthesis = {
            "topic": topic,
            "total_articles": len(processed_evidence),
            "high_quality_count": len(high_quality),
            "medium_quality_count": len(medium_quality),
            "low_quality_count": len(low_quality),
            "key_findings": all_findings[:10],  # Top 10 findings
            "evidence_base": {
                "high_quality": [
                    {
                        "pmid": e["pmid"],
                        "title": e["title"],
                        "findings": e["key_findings"]
                    }
                    for e in high_quality[:5]
                ],
                "supporting_evidence": [
                    {
                        "pmid": e["pmid"],
                        "title": e["title"]
                    }
                    for e in (medium_quality + low_quality)[:10]
                ]
            },
            "summary": self._generate_summary(processed_evidence),
        }
        
        logger.info(f"Synthesized evidence for topic: {topic}")
        return synthesis
    
    def _generate_summary(self, processed_evidence: List[Dict]) -> str:
        """
        Generate a text summary of the evidence.
        
        Args:
            processed_evidence: List of processed evidence
            
        Returns:
            Summary text
        """
        if not processed_evidence:
            return "No evidence available."
        
        summary_parts = []
        summary_parts.append(
            f"Analysis based on {len(processed_evidence)} research articles."
        )
        
        high_quality = [e for e in processed_evidence if e["evidence_quality"] == "high"]
        if high_quality:
            summary_parts.append(
                f"High-quality evidence from {len(high_quality)} studies supports the findings."
            )
        
        return " ".join(summary_parts)
    
    def filter_by_quality(
        self,
        processed_evidence: List[Dict],
        min_quality: str = "medium"
    ) -> List[Dict]:
        """
        Filter evidence by minimum quality level.
        
        Args:
            processed_evidence: List of processed evidence
            min_quality: Minimum quality level (high, medium, low)
            
        Returns:
            Filtered evidence list
        """
        quality_order = {"high": 3, "medium": 2, "low": 1}
        min_level = quality_order.get(min_quality, 2)
        
        filtered = [
            e for e in processed_evidence
            if quality_order.get(e["evidence_quality"], 0) >= min_level
        ]
        
        logger.info(f"Filtered to {len(filtered)} articles with quality >= {min_quality}")
        return filtered
