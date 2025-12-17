# API Documentation

## Core Classes

### PolicyDraftingWorkflow

Main orchestrator for the policy drafting system.

```python
from policy_drafting.workflow import PolicyDraftingWorkflow

workflow = PolicyDraftingWorkflow(
    pubmed_email="user@example.com",
    openai_api_key="sk-..."
)
```

#### Methods

##### execute_full_workflow

Execute the complete policy drafting workflow.

```python
results = workflow.execute_full_workflow(
    topic="Diabetes Management",
    max_articles=20,
    policy_type="clinical_policy"
)
```

**Parameters:**
- `topic` (str): Medical topic for policy
- `max_articles` (int): Maximum articles to retrieve (default: 20)
- `policy_type` (str): Type of policy (default: "clinical_policy")

**Returns:**
- Dict containing:
  - `status`: Workflow status
  - `policy_draft`: Generated policy
  - `validation_results`: Compliance validation
  - `audit_report`: Audit trail
  - `summary`: Summary statistics

---

### PubMedClient

Client for fetching medical research from PubMed.

```python
from policy_drafting.evidence import PubMedClient

client = PubMedClient(
    email="user@example.com",
    api_key="optional-api-key"
)
```

#### Methods

##### search_articles

Search for articles in PubMed.

```python
ids = client.search_articles(
    query="diabetes treatment",
    max_results=10,
    date_from="2020/01/01",
    date_to="2024/12/31"
)
```

**Parameters:**
- `query` (str): Search query
- `max_results` (int): Maximum results (default: 10)
- `date_from` (str, optional): Start date (YYYY/MM/DD)
- `date_to` (str, optional): End date (YYYY/MM/DD)

**Returns:**
- List[str]: PubMed IDs

##### fetch_article_details

Fetch detailed information for PubMed IDs.

```python
articles = client.fetch_article_details(["12345", "67890"])
```

**Parameters:**
- `pubmed_ids` (List[str]): List of PubMed IDs

**Returns:**
- List[Dict]: Article details

##### search_and_fetch

Convenience method combining search and fetch.

```python
articles = client.search_and_fetch(
    query="hypertension management",
    max_results=15
)
```

---

### EvidenceProcessor

Process and extract evidence from medical articles.

```python
from policy_drafting.evidence import EvidenceProcessor

processor = EvidenceProcessor()
```

#### Methods

##### extract_key_findings

Extract key findings from articles.

```python
processed = processor.extract_key_findings(articles)
```

**Parameters:**
- `articles` (List[Dict]): Article data

**Returns:**
- List[Dict]: Processed evidence with findings

##### synthesize_evidence

Synthesize evidence into structured summary.

```python
synthesis = processor.synthesize_evidence(
    processed_evidence,
    topic="Diabetes Management"
)
```

**Parameters:**
- `processed_evidence` (List[Dict]): Processed evidence
- `topic` (str): Topic for synthesis

**Returns:**
- Dict: Evidence synthesis

##### filter_by_quality

Filter evidence by quality level.

```python
filtered = processor.filter_by_quality(
    processed_evidence,
    min_quality="medium"
)
```

**Parameters:**
- `processed_evidence` (List[Dict]): Evidence to filter
- `min_quality` (str): Minimum quality ("high", "medium", "low")

**Returns:**
- List[Dict]: Filtered evidence

---

### PolicyGenerator

Generate policy drafts using AI models.

```python
from policy_drafting.models import PolicyGenerator

generator = PolicyGenerator(
    model_name="gpt-4",
    api_key="sk-...",
    temperature=0.7
)
```

#### Methods

##### generate_policy_draft

Generate policy draft from evidence.

```python
draft = generator.generate_policy_draft(
    evidence_synthesis,
    policy_type="clinical_policy",
    additional_context={"department": "cardiology"}
)
```

**Parameters:**
- `evidence_synthesis` (Dict): Synthesized evidence
- `policy_type` (str): Policy type (default: "clinical_policy")
- `additional_context` (Dict, optional): Additional context

**Returns:**
- Dict: Policy draft with content and metadata

##### refine_policy_draft

Refine draft based on feedback.

```python
refined = generator.refine_policy_draft(
    draft,
    feedback=["Add more detail on monitoring", "Clarify dosing"]
)
```

**Parameters:**
- `draft` (Dict): Original draft
- `feedback` (List[str]): Feedback items

**Returns:**
- Dict: Refined policy draft

---

### ComplianceValidator

Validate policies against regulatory frameworks.

```python
from policy_drafting.compliance import ComplianceValidator

validator = ComplianceValidator()
```

#### Methods

##### validate_policy

Validate policy draft.

```python
results = validator.validate_policy(policy_draft)
```

**Parameters:**
- `policy_draft` (Dict): Policy to validate

**Returns:**
- Dict: Validation results with status and score

##### validate_evidence_quality

Validate evidence quality.

```python
evidence_validation = validator.validate_evidence_quality(
    evidence_synthesis
)
```

**Parameters:**
- `evidence_synthesis` (Dict): Evidence data

**Returns:**
- Dict: Evidence quality validation

##### check_regulatory_alignment

Check alignment with specific regulations.

```python
alignment = validator.check_regulatory_alignment(
    policy_draft,
    specific_regulations=["FDA", "CMS"]
)
```

**Parameters:**
- `policy_draft` (Dict): Policy to check
- `specific_regulations` (List[str]): Regulations to check

**Returns:**
- Dict: Alignment results

---

### AuditLogger

Maintain audit trails for activities.

```python
from policy_drafting.explainability import AuditLogger

logger = AuditLogger(log_dir="./logs")
```

#### Methods

##### log_evidence_extraction

Log evidence extraction activity.

```python
entry_id = logger.log_evidence_extraction(
    query="diabetes",
    article_count=15,
    source="pubmed"
)
```

##### log_policy_generation

Log policy generation.

```python
entry_id = logger.log_policy_generation(
    policy_type="clinical_policy",
    model_used="gpt-4",
    evidence_count=15,
    policy_id="POL-001"
)
```

##### log_decision

Log a decision.

```python
entry_id = logger.log_decision(
    decision_type="approval",
    decision="approved",
    rationale="Meets all requirements",
    supporting_data={"score": 0.95}
)
```

##### generate_audit_report

Generate audit report.

```python
report = logger.generate_audit_report(session_id="optional")
```

**Returns:**
- Dict: Audit report with all activities

---

### DashboardExporter

Export policies for dashboard integration.

```python
from policy_drafting.integration import DashboardExporter

exporter = DashboardExporter(export_dir="./exports")
```

#### Methods

##### export_policy_draft

Export policy to file.

```python
file_path = exporter.export_policy_draft(
    policy_draft,
    format="markdown",
    include_metadata=True
)
```

**Parameters:**
- `policy_draft` (Dict): Policy to export
- `format` (str): Format ("json", "markdown", "html")
- `include_metadata` (bool): Include metadata (default: True)

**Returns:**
- str: Path to exported file

##### create_dashboard_package

Create complete package with all files.

```python
package_dir = exporter.create_dashboard_package(
    policy_draft,
    validation_results,
    audit_report
)
```

**Parameters:**
- `policy_draft` (Dict): Policy draft
- `validation_results` (Dict): Validation results
- `audit_report` (Dict): Audit report

**Returns:**
- str: Path to package directory

##### generate_api_payload

Generate API payload for integration.

```python
payload = exporter.generate_api_payload(policy_draft)
```

**Parameters:**
- `policy_draft` (Dict): Policy draft

**Returns:**
- Dict: API-ready payload

---

## Data Structures

### Article Dictionary

```python
{
    "pmid": "12345",
    "title": "Article Title",
    "abstract": "Article abstract text",
    "authors": ["Author 1", "Author 2"],
    "publication_date": "2023-01-15",
    "journal": "Journal Name",
    "keywords": ["keyword1", "keyword2"]
}
```

### Evidence Synthesis Dictionary

```python
{
    "topic": "Topic Name",
    "total_articles": 15,
    "high_quality_count": 8,
    "medium_quality_count": 5,
    "low_quality_count": 2,
    "key_findings": ["Finding 1", "Finding 2"],
    "evidence_base": {
        "high_quality": [...],
        "supporting_evidence": [...]
    },
    "summary": "Summary text"
}
```

### Policy Draft Dictionary

```python
{
    "policy_type": "clinical_policy",
    "content": "Full policy text",
    "metadata": {
        "generated_at": "2024-01-01T00:00:00",
        "model": "gpt-4",
        "evidence_count": 15
    },
    "components": {
        "title": "Policy Title",
        "policy_number": "POL-001",
        "policy_statement": "...",
        "rationale": "...",
        ...
    }
}
```

### Validation Results Dictionary

```python
{
    "overall_status": "compliant",
    "compliance_score": 0.92,
    "framework_results": {
        "fda_guidelines": {...},
        "cms_requirements": {...}
    },
    "issues": [],
    "warnings": [],
    "recommendations": []
}
```

## Error Handling

All methods may raise standard Python exceptions:
- `ValueError`: Invalid parameters
- `FileNotFoundError`: File not found
- `requests.exceptions.RequestException`: Network errors
- `json.JSONDecodeError`: JSON parsing errors

Handle errors appropriately:

```python
try:
    results = workflow.execute_full_workflow(topic="diabetes")
except ValueError as e:
    print(f"Invalid input: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```
