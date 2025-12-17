"""Dashboard exporter for integration with provider analytics."""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path
from loguru import logger


class DashboardExporter:
    """Export policy drafts to provider analytic dashboards."""
    
    def __init__(self, export_dir: Optional[str] = None):
        """
        Initialize dashboard exporter.
        
        Args:
            export_dir: Directory for exports
        """
        self.export_dir = export_dir or os.getenv(
            "EXPORT_DIR",
            "./data/exports"
        )
        Path(self.export_dir).mkdir(parents=True, exist_ok=True)
        logger.info(f"Dashboard exporter initialized: {self.export_dir}")
    
    def export_policy_draft(
        self,
        policy_draft: Dict,
        format: str = "json",
        include_metadata: bool = True
    ) -> str:
        """
        Export policy draft to file.
        
        Args:
            policy_draft: Policy draft to export
            format: Export format (json, markdown, html)
            include_metadata: Whether to include metadata
            
        Returns:
            Path to exported file
        """
        policy_id = policy_draft.get("components", {}).get(
            "policy_number",
            f"policy_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        )
        
        if format == "json":
            return self._export_json(policy_draft, policy_id, include_metadata)
        elif format == "markdown":
            return self._export_markdown(policy_draft, policy_id)
        elif format == "html":
            return self._export_html(policy_draft, policy_id)
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def _export_json(
        self,
        policy_draft: Dict,
        policy_id: str,
        include_metadata: bool
    ) -> str:
        """Export policy as JSON."""
        output_file = os.path.join(self.export_dir, f"{policy_id}.json")
        
        export_data = {
            "policy_id": policy_id,
            "content": policy_draft.get("content", ""),
            "policy_type": policy_draft.get("policy_type", ""),
        }
        
        if include_metadata:
            export_data["metadata"] = policy_draft.get("metadata", {})
            export_data["components"] = policy_draft.get("components", {})
        
        try:
            with open(output_file, 'w') as f:
                json.dump(export_data, f, indent=2)
            logger.info(f"Exported policy to JSON: {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"Error exporting to JSON: {e}")
            raise
    
    def _export_markdown(self, policy_draft: Dict, policy_id: str) -> str:
        """Export policy as Markdown."""
        output_file = os.path.join(self.export_dir, f"{policy_id}.md")
        
        content = policy_draft.get("content", "")
        
        try:
            with open(output_file, 'w') as f:
                f.write(content)
            logger.info(f"Exported policy to Markdown: {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"Error exporting to Markdown: {e}")
            raise
    
    def _export_html(self, policy_draft: Dict, policy_id: str) -> str:
        """Export policy as HTML."""
        output_file = os.path.join(self.export_dir, f"{policy_id}.html")
        
        content = policy_draft.get("content", "")
        components = policy_draft.get("components", {})
        metadata = policy_draft.get("metadata", {})
        
        # Convert markdown-style content to HTML
        html_content = self._markdown_to_html(content)
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{components.get('title', 'Policy Document')}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
        }}
        .metadata {{
            background-color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .metadata p {{
            margin: 5px 0;
        }}
    </style>
</head>
<body>
    <div class="metadata">
        <p><strong>Policy ID:</strong> {policy_id}</p>
        <p><strong>Generated:</strong> {metadata.get('generated_at', 'N/A')}</p>
        <p><strong>Evidence Count:</strong> {metadata.get('evidence_count', 'N/A')}</p>
    </div>
    {html_content}
</body>
</html>
"""
        
        try:
            with open(output_file, 'w') as f:
                f.write(html)
            logger.info(f"Exported policy to HTML: {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"Error exporting to HTML: {e}")
            raise
    
    def _markdown_to_html(self, markdown_text: str) -> str:
        """Convert markdown-style text to HTML."""
        html = markdown_text
        
        # Convert headers
        html = html.replace('# ', '<h1>').replace('\n\n', '</h1>\n\n')
        html = html.replace('## ', '<h2>').replace('\n', '</h2>\n')
        
        # Convert lists
        lines = html.split('\n')
        in_list = False
        result = []
        
        for line in lines:
            if line.strip().startswith('- '):
                if not in_list:
                    result.append('<ul>')
                    in_list = True
                result.append(f'<li>{line.strip()[2:]}</li>')
            else:
                if in_list:
                    result.append('</ul>')
                    in_list = False
                result.append(line)
        
        if in_list:
            result.append('</ul>')
        
        html = '\n'.join(result)
        
        # Convert paragraphs
        html = html.replace('\n\n', '</p>\n<p>')
        html = '<p>' + html + '</p>'
        
        # Clean up empty paragraphs
        html = html.replace('<p></p>', '')
        html = html.replace('<p></h1>', '</h1>')
        html = html.replace('<p></h2>', '</h2>')
        html = html.replace('</h1></p>', '</h1>')
        html = html.replace('</h2></p>', '</h2>')
        
        return html
    
    def export_validation_results(
        self,
        validation_results: Dict,
        policy_id: str
    ) -> str:
        """
        Export validation results.
        
        Args:
            validation_results: Validation results to export
            policy_id: Associated policy ID
            
        Returns:
            Path to exported file
        """
        output_file = os.path.join(
            self.export_dir,
            f"{policy_id}_validation.json"
        )
        
        try:
            with open(output_file, 'w') as f:
                json.dump(validation_results, f, indent=2)
            logger.info(f"Exported validation results: {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"Error exporting validation results: {e}")
            raise
    
    def create_dashboard_package(
        self,
        policy_draft: Dict,
        validation_results: Dict,
        audit_report: Dict
    ) -> str:
        """
        Create complete dashboard package with all related files.
        
        Args:
            policy_draft: Policy draft
            validation_results: Validation results
            audit_report: Audit report
            
        Returns:
            Path to package directory
        """
        policy_id = policy_draft.get("components", {}).get(
            "policy_number",
            f"policy_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        )
        
        package_dir = os.path.join(self.export_dir, f"{policy_id}_package")
        Path(package_dir).mkdir(parents=True, exist_ok=True)
        
        # Export policy in multiple formats
        self._export_json(policy_draft, policy_id, True)
        self._export_markdown(policy_draft, policy_id)
        self._export_html(policy_draft, policy_id)
        
        # Export validation results
        validation_file = os.path.join(package_dir, "validation_results.json")
        with open(validation_file, 'w') as f:
            json.dump(validation_results, f, indent=2)
        
        # Export audit report
        audit_file = os.path.join(package_dir, "audit_report.json")
        with open(audit_file, 'w') as f:
            json.dump(audit_report, f, indent=2)
        
        # Create package index
        index = {
            "policy_id": policy_id,
            "package_created": datetime.now().isoformat(),
            "files": {
                "policy_json": f"{policy_id}.json",
                "policy_markdown": f"{policy_id}.md",
                "policy_html": f"{policy_id}.html",
                "validation_results": "validation_results.json",
                "audit_report": "audit_report.json",
            },
            "summary": {
                "policy_type": policy_draft.get("policy_type", ""),
                "validation_status": validation_results.get("overall_status", ""),
                "compliance_score": validation_results.get("compliance_score", 0.0),
            }
        }
        
        index_file = os.path.join(package_dir, "package_index.json")
        with open(index_file, 'w') as f:
            json.dump(index, f, indent=2)
        
        logger.info(f"Created dashboard package: {package_dir}")
        return package_dir
    
    def generate_api_payload(self, policy_draft: Dict) -> Dict:
        """
        Generate API payload for dashboard integration.
        
        Args:
            policy_draft: Policy draft
            
        Returns:
            API payload dictionary
        """
        components = policy_draft.get("components", {})
        metadata = policy_draft.get("metadata", {})
        
        payload = {
            "policy": {
                "id": components.get("policy_number", ""),
                "title": components.get("title", ""),
                "type": policy_draft.get("policy_type", ""),
                "effective_date": components.get("effective_date", ""),
                "status": "draft",
            },
            "content": {
                "policy_statement": components.get("policy_statement", ""),
                "rationale": components.get("rationale", ""),
                "clinical_guidelines": components.get("clinical_guidelines", ""),
                "compliance_requirements": components.get("compliance_requirements", ""),
            },
            "metadata": {
                "generated_at": metadata.get("generated_at", ""),
                "model": metadata.get("model", ""),
                "evidence_count": metadata.get("evidence_count", 0),
                "high_quality_evidence": metadata.get("high_quality_evidence", 0),
            },
            "timestamp": datetime.now().isoformat(),
        }
        
        return payload
