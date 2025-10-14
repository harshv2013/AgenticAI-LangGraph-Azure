def review_report(state: dict):
    print(f"review_report called: {state}\n\n")
    report = state["report"]
    if "TODO" in report:
        state["review"] = {"status": "needs_review", "comments": "Contains TODO placeholders."}
    else:
        state["review"] = {"status": "approved"}
    print(f"review_report end: {state}\n\n")
    return state
