def run_search(state: dict):
    print(f"run_search called: {state}\n\n")
    queries = state["queries"]
    print(f"queries====: {queries}")
    results = [{"query": q, "snippet": f"Search result for {q}"} for q in queries]
    state["results"] = results
    print(f"run_search end==={state}\n\n")
    return state
