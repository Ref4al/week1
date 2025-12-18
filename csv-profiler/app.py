from __future__ import annotations
import csv
import json
from io import StringIO
from pathlib import Path
import streamlit as st
from src.csv_profiler.profile import basic_profile
from src.csv_profiler import render_markdown

def parse_csv_text(text: str) -> list[dict[str, str]]:
   f = StringIO(text)
   reader = csv.DictReader(f)
   rows: list[dict[str, str]] = []
   for row in reader:
       rows.append({k: (v if v is not None else "") for k, v in row.items()})
   return rows

st.set_page_config(page_title="CSV Profiler", layout="wide")
st.title("CSV Profiler")
st.caption("Upload CSV → Profile → Export JSON + Markdown")
st.sidebar.header("Inputs")
uploaded = st.sidebar.file_uploader("Upload a CSV", type=["csv"])
show_preview = st.sidebar.checkbox("Show preview", value=True)
rows: list[dict[str, str]] = []
report: dict | None = None
if uploaded is not None:
   text = uploaded.getvalue().decode("utf-8", errors="replace")
   rows = parse_csv_text(text)
   if len(rows) == 0:
       st.error("CSV has no data rows (or parsing failed).")
       st.stop()
   if len(rows[0].keys()) == 0:
       st.warning("CSV has no headers (no columns detected).")
   if show_preview:
       st.subheader("Preview")
       st.write(rows[:5])
   if st.button("Generate report"):
       report = basic_profile(rows)
       st.session_state["report"] = report
       st.success("Report generated!")
report = st.session_state.get("report")
if report is not None:
   st.subheader("Summary")
   st.write(
       {
           "rows": report.get("rows"),
           "num_columns": len(report.get("columns", {})),
       }
   )
   st.subheader("Report (Markdown)")
   md = render_markdown(report)
   st.markdown(md)
   st.divider()
   st.subheader("Export")
   report_name = st.text_input("Report name", value="report")
   json_bytes = (json.dumps(report, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
   md_bytes = (md + "\n").encode("utf-8")
   c1, c2, c3 = st.columns(3)
   with c1:
       st.download_button(
           "Download JSON",
           data=json_bytes,
           file_name=f"{report_name}.json",
           mime="application/json",
       )
   with c2:
       st.download_button(
           "Download Markdown",
           data=md_bytes,
           file_name=f"{report_name}.md",
           mime="text/markdown",
       )
   with c3:
       if st.button("Save to outputs/"):
           out_dir = Path("outputs")
           out_dir.mkdir(parents=True, exist_ok=True)
           (out_dir / f"{report_name}.json").write_bytes(json_bytes)
           (out_dir / f"{report_name}.md").write_bytes(md_bytes)
           st.success(f"Saved to {out_dir}/")