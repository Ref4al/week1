
from __future__ import annotations
from typing import Any
MISSING = {"", "na", "n/a", "null", "none", "nan"}
def is_missing(value: str | None) -> bool:
   if value is None:
       return True
   return value.strip().casefold() in MISSING

def try_float(value: str) -> float | None:
   try:
       return float(value)
   except ValueError:
       return None

def infer_type(values: list[str]) -> str:
   usable = [v for v in values if not is_missing(v)]
   if not usable:
       return "text"
   for v in usable:
       if try_float(v) is None:
           return "text"
   return "number"

def column_values(rows: list[dict[str, str]], col: str) -> list[str]:
   return [row.get(col, "") for row in rows]

def numeric_stats(values: list[str]) -> dict[str, Any]:
   usable = [v for v in values if not is_missing(v)]
   missing = len(values) - len(usable)
   nums: list[float] = []
   for v in usable:
       x = try_float(v)
       if x is None:
           continue
       nums.append(x)
   if not nums:
       return {
           "count": 0,
           "missing": missing,
           "unique": 0,
           "min": None,
           "max": None,
           "mean": None,
       }
   return {
       "count": len(nums),
       "missing": missing,
       "unique": len(set(nums)),
       "min": min(nums),
       "max": max(nums),
       "mean": sum(nums) / len(nums),
   }

def text_stats(values: list[str], top_k: int = 5) -> dict[str, Any]:
   usable = [v for v in values if not is_missing(v)]
   missing = len(values) - len(usable)
   counts: dict[str, int] = {}
   for v in usable:
       counts[v] = counts.get(v, 0) + 1
   top = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:top_k]
   return {
       "count": len(usable),
       "missing": missing,
       "unique": len(counts),
       "top": top,
   }

def basic_profile(rows: list[dict[str, str]]) -> dict:
   if not rows:
       return {"rows": 0, "columns": {}, "notes": ["Empty dataset"]}
   columns = list(rows[0].keys())
   report = {
       "rows": len(rows),
       "columns": {},
       "notes": [],
   }
   for col in columns:
       values = column_values(rows, col)
       col_type = infer_type(values)
       if col_type == "number":
           stats = numeric_stats(values)
       else:
           stats = text_stats(values)
       report["columns"][col] = {
           "type": col_type,
           **stats,
       }
   return report