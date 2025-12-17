"""Evidence module for medical research extraction and processing."""

from .pubmed_client import PubMedClient
from .evidence_processor import EvidenceProcessor

__all__ = ["PubMedClient", "EvidenceProcessor"]
