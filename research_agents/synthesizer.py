def synthesize_results(state: dict):
    print(f"synthesize_results called: {state}\n\n")

    notes = "\n".join([r["snippet"] for r in state["results"]])
    state["synthesis"] = {"summary": notes}
    print(f"synthesize_results end: {state}\n\n")

    return state