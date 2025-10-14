import pandas as pd

def ingest_data(state: dict):
    """Load CSV into dataframe and validate."""
    file_path = state.get("file_path")
    try:
        df = pd.read_csv(file_path)

        return {
            "status": "ingested",
            "rows": len(df),
            "columns": list(df.columns),
            "df": df,   # ✅ persist dataframe in returned dict
            "preview": df.head(3).to_dict()
        }
    except Exception as e:
        return {"error": f"Ingestion failed: {str(e)}"}

