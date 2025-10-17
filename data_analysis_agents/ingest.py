# import pandas as pd

# def ingest_data(state: dict):
#     """Load CSV into dataframe and validate."""
#     file_path = state.get("file_path")
#     try:
#         df = pd.read_csv(file_path)

#         return {
#             "status": "ingested",
#             "rows": len(df),
#             "columns": list(df.columns),
#             "df": df,   # ✅ persist dataframe in returned dict
#             "preview": df.head(3).to_dict()
#         }
#     except Exception as e:
#         return {"error": f"Ingestion failed: {str(e)}"}



# data_analysis_agents/ingest.py
import pandas as pd
from pathlib import Path

def ingest(state):
    """
    Handles dataset ingestion for data analysis workflow.

    state may be:
      - a dict with 'file_path' or 'file' key (local path)
      - a string path directly

    Returns a dict containing:
      - file_path (absolute path for downstream nodes)
      - dataframe metadata (rows, columns, preview)
      - dataframe object (df)
    """

    # Extract file path
    if isinstance(state, dict):
        fp = state.get("file_path") or state.get("file")
    else:
        fp = state

    if not fp:
        return {"error": "No file path provided."}

    p = Path(fp)
    if not p.exists():
        return {"error": f"Ingestion failed: file not found: {fp}"}

    # Load CSV
    try:
        df = pd.read_csv(p, parse_dates=True)
    except Exception as e:
        return {"error": f"Ingestion failed: {e}"}

    preview = df.head(3).to_dict()

    meta = {
        "status": "ingested",
        "rows": len(df),
        "columns": list(df.columns),
        "preview": preview,
        "file_path": str(p.resolve()),
        "df": df,
    }

    # ✅ Return FLATTENED structure (not nested)
    return {
        "status": "ingested",
        "file_path": meta["file_path"],      # <--- exposed for next node
        "rows": meta["rows"],
        "columns": meta["columns"],
        "preview": meta["preview"],
        "df": meta["df"],
        "ingest": meta,                      # <--- still keep for reference
    }
