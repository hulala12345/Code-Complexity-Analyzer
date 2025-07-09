from __future__ import annotations
import json
from pathlib import Path
from typing import Optional

from .analyzer import AnalysisReport

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset='utf-8'>
<title>Code Complexity Report</title>
<style>
body {{font-family: Arial, sans-serif; margin:20px;}}
table {{border-collapse: collapse; width: 100%;}}
th, td {{border: 1px solid #ccc; padding: 8px; text-align: left;}}
tr.high {{background-color: #fdd;}}
tr.medium {{background-color: #ffd;}}
tr.low {{background-color: #dfd;}}
</style>
</head>
<body>
<h1>Code Complexity Report</h1>
<table>
<thead>
<tr><th>Function</th><th>Complexity</th><th>Max Nesting</th></tr>
</thead>
<tbody>
{rows}
</tbody>
</table>
<h2>Duplicate Functions</h2>
<ul>
{dups}
</ul>
</body>
</html>"""

def _severity_class(value: int, threshold_high: int, threshold_med: int) -> str:
    if value >= threshold_high:
        return "high"
    elif value >= threshold_med:
        return "medium"
    return "low"

def generate_html(report: AnalysisReport, out_file: Path, *,
                  complexity_threshold: int = 10,
                  depth_threshold: int = 3) -> None:
    rows = []
    for metric in report.metrics:
        cls = _severity_class(metric.complexity, complexity_threshold, complexity_threshold//2)
        row = f"<tr class='{cls}'><td>{metric.name}</td><td>{metric.complexity}</td><td>{metric.max_depth}</td></tr>"
        rows.append(row)
    dup_items = [f"<li>{a} &amp; {b} ({ratio:.2f})</li>" for a, b, ratio in report.duplicates]
    html = HTML_TEMPLATE.format(rows='\n'.join(rows), dups='\n'.join(dup_items))
    out_file.write_text(html)

