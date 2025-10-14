def plan_research(user_prompt: str):
    queries = [
        f"{user_prompt} background and history",
        f"{user_prompt} latest updates and trends",
        f"{user_prompt} economic impact"
    ]
    
    resp = {"queries": queries, "user_prompt": user_prompt}
    print(f"planner: {resp}\n\n")
    return {"queries": queries, "user_prompt": user_prompt}
