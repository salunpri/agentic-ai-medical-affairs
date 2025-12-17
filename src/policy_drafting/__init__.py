"""
Agentic AI Medical Affairs - Healthcare Policy Drafting System

This package provides tools for automating healthcare policy drafting
and validation using GenAI techniques.
"""

__version__ = "0.1.0"
__author__ = "Agentic AI Team"

from .evidence.pubmed_client import PubMedClient
from .evidence.evidence_processor import EvidenceProcessor
from .models.policy_generator import PolicyGenerator
from .compliance.validator import ComplianceValidator
from .explainability.audit_logger import AuditLogger
from .integration.dashboard_exporter import DashboardExporter

__all__ = [
    "PubMedClient",
    "EvidenceProcessor",
    "PolicyGenerator",
    "ComplianceValidator",
    "AuditLogger",
    "DashboardExporter",
]
