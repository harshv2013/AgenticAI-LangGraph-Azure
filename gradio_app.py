import asyncio
import gradio as gr

# import the compiled LangGraph app
from workflows.research_graph import research_graph

async def run_workflow_stream(prompt: str):
    """
    Async generator that yields (logs, report) tuples for Gradio streaming.
    Each yield updates the UI: left = logs, right = report.
    """
    logs = ""
    final_report = ""

    # astream yields state snapshots (one top-level key == node name)
    async for state in research_graph.astream(prompt):
        # state is like {"planner": {...}} or {"search": {...}}
        # get node name and its data
        node = list(state.keys())[0]
        node_data = state[node]

        # append only the new part for readability
        logs += f"=== {node} ===\n{node_data}\n\n"

        # update final report if produced
        if isinstance(node_data, dict) and "report" in node_data:
            final_report = node_data["report"]
        elif "report" in state:
            final_report = state["report"]

        # yield (logs_text, report_text)
        yield logs, final_report

    # ensure a final yield so Gradio shows last state
    yield logs, final_report


def launch_gradio():
    with gr.Blocks(title="AgenticAI Research (LangGraph)") as app:
        gr.Markdown("## AgenticAI Research — Planner → Search → Synthesizer → Writer → Reviewer → Delivery")
        with gr.Row():
            prompt_in = gr.Textbox(label="Research prompt", placeholder="e.g. Major health issues and their impact on the Indian economy", lines=2)
            # keep email optional; delivery currently prints to console in agent
            email_in = gr.Textbox(label="Email (optional)", placeholder="(not required for demo)", lines=1)

        with gr.Row():
            logs_out = gr.Textbox(label="Workflow logs (streaming)", interactive=False, lines=20)
            report_out = gr.Textbox(label="Final report", interactive=False, lines=20)

        run_btn = gr.Button("Run Research Workflow")

        # attach the async generator to the button click — streaming outputs to two components
        run_btn.click(fn=run_workflow_stream, inputs=[prompt_in], outputs=[logs_out, report_out])

    app.launch(server_name="127.0.0.1", server_port=7860, share=False)


if __name__ == "__main__":
    launch_gradio()
