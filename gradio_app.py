import asyncio
import os
import gradio as gr
from workflows.general_manager_graph import general_manager_graph


# ===============================
# 🔁 Unified Runner
# ===============================
async def run_manager(prompt=None, file_path=None):
    """
    Unified execution for Research • Realtime • Data Analysis workflows.
    Returns: (text_output, histogram, line, bar, scatter)
    """
    state = {"input": prompt, "file_path": file_path}
    final_output = None
    charts = {}

    async for update in general_manager_graph.astream(state):
        node = list(update.keys())[0]
        data = update[node]

        if node == "executor" and isinstance(data, dict):
            result = data.get("result", {})

            final_output = (
                result.get("report")
                or result.get("message")
                or result.get("summary")
                or "⚠️ No result generated."
            )
            charts = result.get("charts", {})

    return (
        final_output,
        charts.get("histogram"),
        charts.get("line"),
        charts.get("bar"),
        charts.get("scatter"),
    )


# ===============================
# 🧠 Gradio App
# ===============================#004080 
def launch_app():
    with gr.Blocks(theme=gr.themes.Soft(), title="AgenticAI General Manager") as app:
        # --- Header ---
        gr.Markdown(
            """
            <div style="text-align: center; padding: 10px; background-color: #93C5FD; color: white; border-radius: 10px;">
                <h1>🤖 AgenticAI General Manager</h1>
                <h3>Unified Multi-Agent Workflow (Research • Data Analysis • Realtime)</h3>
            </div>
            """
        )

        # --- Unified Input + File Upload (like ChatGPT style) ---
        gr.Markdown("### Type your query or attach a CSV file for analysis")

        with gr.Row():
            with gr.Column(scale=8):
                input_box = gr.Textbox(
                    label="Ask your question",
                    placeholder="e.g. 'Impact of AI on healthcare' or 'What's the weather in Delhi?' or upload a CSV...",
                    lines=2,
                )
            with gr.Column(scale=2, min_width=100):
                file_upload = gr.File(
                    label="➕",
                    type="filepath",
                    file_types=[".csv"],
                    elem_id="upload-btn",
                    interactive=True,
                )

        run_button = gr.Button("🚀 Run Agent", variant="primary")

        # --- Output Section ---
        with gr.Column():
            output_md = gr.Markdown(label="🧾 Result")
            hist_img = gr.Image(label="Histogram", visible=False)
            line_img = gr.Image(label="Revenue Over Time", visible=False)
            bar_img = gr.Image(label="Profit by Region", visible=False)
            scatter_img = gr.Image(label="Revenue vs Profit", visible=False)

        # --- Run Function ---
        def run_unified(prompt, file):
            if file:
                result, hist, line, bar, scatter = asyncio.run(run_manager(file_path=file))
            else:
                result, hist, line, bar, scatter = asyncio.run(run_manager(prompt=prompt))

            return (
                result,
                gr.update(value=hist, visible=bool(hist)),
                gr.update(value=line, visible=bool(line)),
                gr.update(value=bar, visible=bool(bar)),
                gr.update(value=scatter, visible=bool(scatter)),
            )

        run_button.click(
            fn=run_unified,
            inputs=[input_box, file_upload],
            outputs=[output_md, hist_img, line_img, bar_img, scatter_img],
        )

        # --- Footer ---
        gr.Markdown(
            """
            <div style="text-align: center; padding: 10px; margin-top: 20px; font-size: 14px; color: gray;">
                Powered by <b>LangGraph</b> + <b>Azure OpenAI</b> | © 2025 AgenticAI
            </div>
            """
        )

    app.launch(server_name="127.0.0.1", server_port=7863, share=False)


if __name__ == "__main__":
    launch_app()
