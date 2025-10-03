# from workflows.research_graph import graph

# if __name__ == "__main__":
#     user_prompt = "Major health issues and their impact on the Indian economy"

#     # Run the graph with initial input
#     result = graph.run(user_prompt)

#     print("\n=== Workflow Completed ===")
#     print(result)


# #####################################################################

# #####################################################################


# from workflows.research_graph import research_graph

# if __name__ == "__main__":
#     user_prompt = "Major health issues and their impact on the Indian economy"

#     # Run the compiled workflow
#     result = research_graph.invoke(user_prompt)

#     print("\n=== Workflow Completed ===")
#     # print(result)
#     print("\n=== Final Workflow State ===")
#     print("Prompt:", result["user_prompt"])
#     print("Queries:", result["queries"])
#     print("Review Status:", result["review"]["status"])
#     print("\n--- Report ---\n")
#     print(result["report"])

    
# #####################################################################

# #####################################################################


# import asyncio
# from workflows.research_graph import research_graph

# async def run_streaming(user_prompt: str):
#     async for state in research_graph.astream(user_prompt):
#         print("\n--- State Update ---")
#         print(state)

# if __name__ == "__main__":
#     prompt = "Major health issues and their impact on the Indian economy"
#     asyncio.run(run_streaming(prompt))


# #######################################################################
# #######################################################################

import asyncio
from workflows.research_graph import research_graph

def diff_keys(old: dict, new: dict):
    """Return only the new/changed keys in state."""
    return {k: v for k, v in new.items() if k not in old}

async def run_streaming(user_prompt: str):
    prev = {}
    async for state in research_graph.astream(user_prompt):
        # Each state dict has a single top-level key (the node name)
        node = list(state.keys())[0]
        new_data = diff_keys(prev, state[node])
        print(f"\n=== Node Finished: {node} ===")
        print(new_data)
        prev = state[node]

if __name__ == "__main__":
    prompt = "Major health issues and their impact on the Indian economy"
    asyncio.run(run_streaming(prompt))
