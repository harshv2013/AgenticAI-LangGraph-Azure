# realtime_data_agents/delivery.py

def delivery(summary_dict):
    """Format and return the final response."""
    if "summary" in summary_dict:
        return {
            "status": "delivered",
            "message": f"📡 Real-time Insight:\n\n{summary_dict['summary']}"
        }
    return {"status": "failed", "message": "No summary available."}
