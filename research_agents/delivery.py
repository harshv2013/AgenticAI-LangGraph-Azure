def deliver_report(state: dict):
    print(f"deliver_report called: {state}\n\n")
    report = state["report"]
    review = state["review"]

    if review["status"] == "approved":
        print("\n=== Delivering Report ===")
        print(report)
    else:
        print("\n⚠️ Report requires review:", review["comments"])
    
    print(f"deliver_report end: {state}\n\n")
    return state
