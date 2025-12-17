# Agentic AI for Medical Affairs

This repository provides a comprehensive GenAI-powered solution for automating healthcare policy drafting and validation. It leverages evidence synthesis and natural language understanding (NLU) techniques to draft clinical policies aligned with regulatory standards.

## Features

- **Automated Evidence Extraction**: Retrieves relevant medical research from PubMed and other healthcare databases
- **Evidence Synthesis**: Processes and synthesizes medical literature with quality assessment
- **Policy Draft Generation**: Creates comprehensive policy documents using AI models
- **Compliance Validation**: Validates policies against FDA, CMS, HIPAA, and clinical standards
- **Audit Trail**: Maintains complete audit logs for regulatory assurance
- **Dashboard Integration**: Exports to multiple formats for provider analytics dashboards
- **Explainability**: Provides transparent decision-making with evidence traceability

## Architecture

```
src/policy_drafting/
├── evidence/          # Evidence extraction and processing
│   ├── pubmed_client.py
│   └── evidence_processor.py
├── models/            # AI model integration
│   └── policy_generator.py
├── compliance/        # Regulatory validation
│   └── validator.py
├── explainability/    # Audit logging
│   └── audit_logger.py
├── integration/       # Dashboard exports
│   └── dashboard_exporter.py
├── workflow.py        # Main orchestrator
└── cli.py            # Command-line interface
```

## Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/salunpri/agentic-ai-medical-affairs.git
cd agentic-ai-medical-affairs
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install the package:
```bash
pip install -e .
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

## Quick Start

### Using the CLI

Generate a policy draft:
```bash
python src/policy_drafting/cli.py generate "diabetes management" \
    --max-articles 20 \
    --policy-type clinical_policy \
    --output results.json
```

Validate an existing policy:
```bash
python src/policy_drafting/cli.py validate policy_draft.json
```

Export a policy:
```bash
python src/policy_drafting/cli.py export policy_draft.json \
    --format markdown \
    --output-dir ./exports
```

### Using the Python API

```python
from policy_drafting.workflow import PolicyDraftingWorkflow

# Initialize workflow
workflow = PolicyDraftingWorkflow(
    pubmed_email="your-email@example.com"
)

# Execute complete workflow
results = workflow.execute_full_workflow(
    topic="Diabetes Management",
    max_articles=20,
    policy_type="clinical_policy"
)

# Access results
policy_draft = results["policy_draft"]
validation = results["validation_results"]
print(f"Policy ID: {results['summary']['policy_id']}")
print(f"Compliance Score: {validation['compliance_score']:.2%}")
```

## Usage Examples

### Evidence Extraction

```python
from policy_drafting.evidence import PubMedClient, EvidenceProcessor

# Extract evidence
client = PubMedClient(email="your-email@example.com")
articles = client.search_and_fetch("hypertension treatment", max_results=15)

# Process evidence
processor = EvidenceProcessor()
processed = processor.extract_key_findings(articles)
synthesis = processor.synthesize_evidence(processed, "Hypertension Treatment")
```

### Policy Generation

```python
from policy_drafting.models import PolicyGenerator

generator = PolicyGenerator(model_name="gpt-4")
policy_draft = generator.generate_policy_draft(
    evidence_synthesis,
    policy_type="clinical_policy"
)
```

### Compliance Validation

```python
from policy_drafting.compliance import ComplianceValidator

validator = ComplianceValidator()
validation_results = validator.validate_policy(policy_draft)

print(f"Status: {validation_results['overall_status']}")
print(f"Score: {validation_results['compliance_score']:.2%}")
```

### Audit Logging

```python
from policy_drafting.explainability import AuditLogger

logger = AuditLogger()
logger.log_policy_generation(
    policy_type="clinical_policy",
    model_used="gpt-4",
    evidence_count=15,
    policy_id="POL-001"
)

# Generate audit report
report = logger.generate_audit_report()
```

## Testing

Run all tests:
```bash
pytest tests/ -v
```

Run specific test categories:
```bash
# Unit tests only
pytest tests/unit/ -v

# Integration tests only
pytest tests/integration/ -v

# With coverage
pytest tests/ --cov=src/policy_drafting --cov-report=html
```

## Configuration

Configuration can be set via:
1. Environment variables (`.env` file)
2. Configuration file (`config/config.py`)
3. Command-line arguments

### Key Configuration Options

- `PUBMED_EMAIL`: Email for PubMed API (recommended)
- `PUBMED_API_KEY`: API key for higher rate limits (optional)
- `OPENAI_API_KEY`: OpenAI API key for policy generation
- `EXPORT_DIR`: Directory for exports (default: `./data/exports`)
- `AUDIT_LOG_DIR`: Directory for audit logs (default: `./data/audit_logs`)

## Module Documentation

### Evidence Module
- **PubMedClient**: Fetches medical research articles from PubMed
- **EvidenceProcessor**: Extracts key findings and synthesizes evidence

### Models Module
- **PolicyGenerator**: Generates policy drafts using AI models

### Compliance Module
- **ComplianceValidator**: Validates policies against regulatory frameworks

### Explainability Module
- **AuditLogger**: Maintains audit trails for all activities

### Integration Module
- **DashboardExporter**: Exports policies in multiple formats

## Compliance Frameworks

The system validates policies against:
1. **FDA Guidelines**: Medical device and medication requirements
2. **CMS Requirements**: Medicare/Medicaid coverage policies
3. **HIPAA Compliance**: Privacy and security standards
4. **Clinical Standards**: Evidence-based practice guidelines

## Export Formats

Policies can be exported in:
- **JSON**: Structured data with metadata
- **Markdown**: Human-readable format
- **HTML**: Web-ready documents

## Audit Trail

All activities are logged including:
- Evidence extraction and processing
- Policy generation decisions
- Compliance validation results
- Export activities

## Roadmap

- [ ] Support for additional evidence sources (ClinicalTrials.gov, Cochrane Library)
- [ ] Integration with more AI models (Claude, Gemini)
- [ ] Real-time collaboration features
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] REST API for programmatic access

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Create an issue on GitHub
- Contact: medical-affairs@example.com

## Acknowledgments

- PubMed/NCBI for providing access to medical literature
- OpenAI for GPT models
- Healthcare regulatory bodies for guidelines and standards