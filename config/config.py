"""Sample configuration file."""

# API Configuration
PUBMED_EMAIL = "your-email@example.com"
PUBMED_API_KEY = ""  # Optional, for higher rate limits
OPENAI_API_KEY = ""  # Required for policy generation

# Paths
DATA_DIR = "./data"
EXPORT_DIR = "./data/exports"
AUDIT_LOG_DIR = "./data/audit_logs"

# Policy Generation Settings
DEFAULT_MAX_ARTICLES = 20
DEFAULT_POLICY_TYPE = "clinical_policy"
MIN_EVIDENCE_QUALITY = "medium"

# Compliance Settings
MIN_COMPLIANCE_SCORE = 0.7
REQUIRED_FRAMEWORKS = [
    "fda_guidelines",
    "cms_requirements",
    "hipaa_compliance",
    "clinical_standards"
]

# Logging
LOG_LEVEL = "INFO"
ENABLE_AUDIT_TRAIL = True
