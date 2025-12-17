"""Audit logger for tracking policy generation and validation decisions."""

import json
import os
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path
from loguru import logger


class AuditLogger:
    """Maintain audit trails for all policy generation and validation activities."""
    
    def __init__(self, log_dir: Optional[str] = None):
        """
        Initialize audit logger.
        
        Args:
            log_dir: Directory for audit logs
        """
        self.log_dir = log_dir or os.getenv(
            "AUDIT_LOG_DIR",
            "./data/audit_logs"
        )
        Path(self.log_dir).mkdir(parents=True, exist_ok=True)
        self.current_session_id = self._generate_session_id()
        logger.info(f"Audit logger initialized with session: {self.current_session_id}")
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID."""
        return f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def log_evidence_extraction(
        self,
        query: str,
        article_count: int,
        source: str = "pubmed"
    ) -> str:
        """
        Log evidence extraction activity.
        
        Args:
            query: Search query used
            article_count: Number of articles retrieved
            source: Data source
            
        Returns:
            Audit entry ID
        """
        entry = {
            "entry_id": self._generate_entry_id("evidence_extraction"),
            "session_id": self.current_session_id,
            "timestamp": datetime.now().isoformat(),
            "activity_type": "evidence_extraction",
            "details": {
                "query": query,
                "article_count": article_count,
                "source": source,
            },
        }
        
        self._write_audit_entry(entry)
        logger.info(f"Logged evidence extraction: {entry['entry_id']}")
        return entry["entry_id"]
    
    def log_evidence_processing(
        self,
        articles_processed: int,
        high_quality_count: int,
        synthesis_topic: str
    ) -> str:
        """
        Log evidence processing activity.
        
        Args:
            articles_processed: Number of articles processed
            high_quality_count: Number of high-quality articles
            synthesis_topic: Topic of synthesis
            
        Returns:
            Audit entry ID
        """
        entry = {
            "entry_id": self._generate_entry_id("evidence_processing"),
            "session_id": self.current_session_id,
            "timestamp": datetime.now().isoformat(),
            "activity_type": "evidence_processing",
            "details": {
                "articles_processed": articles_processed,
                "high_quality_count": high_quality_count,
                "synthesis_topic": synthesis_topic,
            },
        }
        
        self._write_audit_entry(entry)
        logger.info(f"Logged evidence processing: {entry['entry_id']}")
        return entry["entry_id"]
    
    def log_policy_generation(
        self,
        policy_type: str,
        model_used: str,
        evidence_count: int,
        policy_id: str
    ) -> str:
        """
        Log policy generation activity.
        
        Args:
            policy_type: Type of policy generated
            model_used: AI model used for generation
            evidence_count: Number of evidence articles used
            policy_id: Generated policy ID
            
        Returns:
            Audit entry ID
        """
        entry = {
            "entry_id": self._generate_entry_id("policy_generation"),
            "session_id": self.current_session_id,
            "timestamp": datetime.now().isoformat(),
            "activity_type": "policy_generation",
            "details": {
                "policy_type": policy_type,
                "model_used": model_used,
                "evidence_count": evidence_count,
                "policy_id": policy_id,
            },
        }
        
        self._write_audit_entry(entry)
        logger.info(f"Logged policy generation: {entry['entry_id']}")
        return entry["entry_id"]
    
    def log_compliance_validation(
        self,
        policy_id: str,
        validation_status: str,
        compliance_score: float,
        issues_count: int
    ) -> str:
        """
        Log compliance validation activity.
        
        Args:
            policy_id: Policy ID being validated
            validation_status: Validation status
            compliance_score: Compliance score
            issues_count: Number of issues found
            
        Returns:
            Audit entry ID
        """
        entry = {
            "entry_id": self._generate_entry_id("compliance_validation"),
            "session_id": self.current_session_id,
            "timestamp": datetime.now().isoformat(),
            "activity_type": "compliance_validation",
            "details": {
                "policy_id": policy_id,
                "validation_status": validation_status,
                "compliance_score": compliance_score,
                "issues_count": issues_count,
            },
        }
        
        self._write_audit_entry(entry)
        logger.info(f"Logged compliance validation: {entry['entry_id']}")
        return entry["entry_id"]
    
    def log_decision(
        self,
        decision_type: str,
        decision: str,
        rationale: str,
        supporting_data: Optional[Dict] = None
    ) -> str:
        """
        Log a decision made during policy generation/validation.
        
        Args:
            decision_type: Type of decision
            decision: The decision made
            rationale: Rationale for the decision
            supporting_data: Additional supporting data
            
        Returns:
            Audit entry ID
        """
        entry = {
            "entry_id": self._generate_entry_id("decision"),
            "session_id": self.current_session_id,
            "timestamp": datetime.now().isoformat(),
            "activity_type": "decision",
            "details": {
                "decision_type": decision_type,
                "decision": decision,
                "rationale": rationale,
                "supporting_data": supporting_data or {},
            },
        }
        
        self._write_audit_entry(entry)
        logger.info(f"Logged decision: {entry['entry_id']}")
        return entry["entry_id"]
    
    def log_export(
        self,
        policy_id: str,
        export_format: str,
        destination: str
    ) -> str:
        """
        Log policy export activity.
        
        Args:
            policy_id: Policy ID being exported
            export_format: Format of export
            destination: Export destination
            
        Returns:
            Audit entry ID
        """
        entry = {
            "entry_id": self._generate_entry_id("export"),
            "session_id": self.current_session_id,
            "timestamp": datetime.now().isoformat(),
            "activity_type": "export",
            "details": {
                "policy_id": policy_id,
                "export_format": export_format,
                "destination": destination,
            },
        }
        
        self._write_audit_entry(entry)
        logger.info(f"Logged export: {entry['entry_id']}")
        return entry["entry_id"]
    
    def _generate_entry_id(self, activity_type: str) -> str:
        """Generate unique entry ID."""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
        return f"{activity_type}_{timestamp}"
    
    def _write_audit_entry(self, entry: Dict[str, Any]) -> None:
        """
        Write audit entry to file.
        
        Args:
            entry: Audit entry to write
        """
        # Write to session-specific log file
        session_log_file = os.path.join(
            self.log_dir,
            f"{self.current_session_id}.jsonl"
        )
        
        try:
            with open(session_log_file, 'a') as f:
                f.write(json.dumps(entry) + '\n')
        except Exception as e:
            logger.error(f"Error writing audit entry: {e}")
    
    def get_session_audit_trail(self, session_id: Optional[str] = None) -> list:
        """
        Retrieve audit trail for a session.
        
        Args:
            session_id: Session ID (defaults to current session)
            
        Returns:
            List of audit entries
        """
        session_id = session_id or self.current_session_id
        log_file = os.path.join(self.log_dir, f"{session_id}.jsonl")
        
        if not os.path.exists(log_file):
            logger.warning(f"No audit log found for session: {session_id}")
            return []
        
        entries = []
        try:
            with open(log_file, 'r') as f:
                for line in f:
                    entries.append(json.loads(line))
        except Exception as e:
            logger.error(f"Error reading audit trail: {e}")
        
        return entries
    
    def generate_audit_report(self, session_id: Optional[str] = None) -> Dict:
        """
        Generate audit report for a session.
        
        Args:
            session_id: Session ID (defaults to current session)
            
        Returns:
            Audit report
        """
        entries = self.get_session_audit_trail(session_id)
        
        if not entries:
            return {
                "session_id": session_id or self.current_session_id,
                "error": "No audit entries found"
            }
        
        # Summarize activities
        activity_counts = {}
        for entry in entries:
            activity_type = entry.get("activity_type", "unknown")
            activity_counts[activity_type] = activity_counts.get(activity_type, 0) + 1
        
        report = {
            "session_id": entries[0].get("session_id"),
            "start_time": entries[0].get("timestamp"),
            "end_time": entries[-1].get("timestamp"),
            "total_activities": len(entries),
            "activity_summary": activity_counts,
            "entries": entries,
        }
        
        logger.info(f"Generated audit report for session: {report['session_id']}")
        return report
    
    def export_audit_report(
        self,
        report: Dict,
        output_file: Optional[str] = None
    ) -> str:
        """
        Export audit report to file.
        
        Args:
            report: Audit report to export
            output_file: Output file path
            
        Returns:
            Path to exported file
        """
        if not output_file:
            session_id = report.get("session_id", "unknown")
            output_file = os.path.join(
                self.log_dir,
                f"{session_id}_report.json"
            )
        
        try:
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2)
            logger.info(f"Exported audit report to: {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"Error exporting audit report: {e}")
            raise
