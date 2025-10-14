import pandas as pd

def analyze_data(state: dict):
    """Generate statistical summaries and check missing values."""
    df: pd.DataFrame = state.get("df")
    if df is None:
        return {"error": "No dataframe available for analysis"}
    
    summary = df.describe(include="all").transpose().to_dict()
    missing = df.isnull().sum().to_dict()
    
    return {
        "status": "analyzed",
        "summary": summary,
        "missing": missing,
        "columns_analyzed": len(summary),
        "df": df   # ✅ pass dataframe forward
    }


