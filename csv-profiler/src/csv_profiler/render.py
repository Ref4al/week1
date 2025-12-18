
from __future__ import annotations
import json
from pathlib import Path

def render_markdown(report: dict) -> str:
   """
   Convert profiling report dict to Markdown text
   """
   lines = []
   lines.append("# CSV Profiling Report\n")
   lines.append(f"## Rows\n- Total rows: **{report.get('rows', 0)}**\n")
   columns = report.get("columns", {})
   for col, info in columns.items():
       lines.append(f"## Column: `{col}`")
       lines.append(f"- Type: **{info.get('type')}**")
       lines.append(f"- Missing: **{info.get('missing')}**")
       lines.append(f"- Unique: **{info.get('unique')}**")
       if info.get("type") == "number":
           lines.append(f"- Min: {info.get('min')}")
           lines.append(f"- Max: {info.get('max')}")
           lines.append(f"- Mean: {info.get('mean')}")
       else:
           top = info.get("top", [])
           if top:
               lines.append("- Top values:")
               for v, c in top:
                   lines.append(f"  - {v}: {c}")
       lines.append("")
   return "\n".join(lines)

def write_json(report: dict, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def write_markdown(report: dict, path: str | Path) -> None:
 
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    lines.append("# CSV Profiling Report\n")
    lines.append(f"- Rows: **{report.get('rows', 0)}**\n")
    for col, info in report["columns"].items():
       lines.append(f"\n## {col}\n")
       for k, v in info.items():
           lines.append(f"- **{k}**: {v}\n")
    path.write_text("".join(lines), encoding="utf-8")
    