import asyncio
import os
import shutil
from pathlib import Path
import gradio as gr
from workflows.general_manager_graph import general_manager_graph
from workflows.data_analysis_graph import data_analysis_graph


# ======================================================
# 🔁 1. Unified Manager Runner
# ======================================================
async def run_manager(prompt=None, file_path=None):
    """
    Unified execution for Research • Realtime • Data Analysis workflows.
    Automatically routes based on input type.
    """
    charts = {}
    final_output = None

    # --- Auto-route between CSV & Text ---
    if file_path and os.path.exists(file_path):
        graph = data_analysis_graph
        state = {"file_path": file_path, "question": prompt or ""}
        print("📊 Routing → data_analysis_graph")
    else:
        graph = general_manager_graph
        state = {"input": prompt, "file_path": None}
        print("🧠 Routing → general_manager_graph")

    # --- Stream updates ---
    async for update in graph.astream(state):
        node = list(update.keys())[0]
        data = update[node]

        # Data Analysis
        if graph is data_analysis_graph:
            if node == "executor" and isinstance(data, dict):
                charts = data.get("charts", {})
            elif node == "report" and isinstance(data, dict):
                final_output = (
                    data.get("report")
                    or data.get("summary")
                    or "⚠️ No report generated."
                )

        # Research / Realtime
        elif graph is general_manager_graph:
            if node == "executor" and isinstance(data, dict):
                result = data.get("result", {})
                final_output = (
                    result.get("report")
                    or result.get("message")
                    or result.get("summary")
                    or "⚠️ No result generated."
                )
                charts = result.get("charts", {})

    return final_output or "⚠️ No output generated.", charts


# ======================================================
# 🚀 2. Unified Runner Wrapper for Gradio
# ======================================================
def run_unified(prompt, file):
    """
    Synchronous Gradio wrapper that runs the async LangGraph workflow,
    serves chart files, and returns results dynamically.
    """
    async def _async_run():
        return await run_manager(prompt=prompt, file_path=file)

    try:
        result, charts = asyncio.run(_async_run())
    except RuntimeError:
        loop = asyncio.get_event_loop()
        result, charts = loop.run_until_complete(_async_run())

    # ✅ Copy chart files into Gradio-served directory
    serve_dir = Path("gradio_charts")
    serve_dir.mkdir(exist_ok=True)

    served_charts = []
    for _, path in charts.items():
        if path and os.path.exists(path):
            new_path = serve_dir / Path(path).name
            shutil.copy2(path, new_path)
            served_charts.append(str(new_path))

    print(f"✅ Served {len(served_charts)} chart(s): {served_charts}")

    # Return Markdown report + dynamic chart list
    return result, served_charts


# ======================================================
# 🎨 3. Gradio Interface
# =======================================================
def launch_app():
    with gr.Blocks(
        theme=gr.themes.Soft(primary_hue="blue"),
        title="AgenticAI General Manager",
        css="""
        /* ====== Custom Gallery Styling ====== */
        #gallery-box {
            display: grid !important;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr)) !important;
            gap: 24px !important;
            justify-items: center;
            align-items: start;
            padding: 20px !important;
        }

        /* Override internal gallery image containers */
        #gallery-box .thumbnail-item, 
        #gallery-box .image-container, 
        #gallery-box img {
            width: 100% !important;
            height: auto !important;
            max-height: 480px !important;
            object-fit: contain !important;
            border-radius: 10px !important;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.15) !important;
            transition: transform 0.2s ease-in-out !important;
        }

        #gallery-box img:hover {
            transform: scale(1.02);
        }

        /* Center report */
        #report-box {
            max-width: 900px;
            margin: 0 auto;
        }

        /* Hide scrollbar in gallery */
        #gallery-box::-webkit-scrollbar {
            display: none;
        }
        """
    ) as app:
        # --- Header ---
        gr.HTML(
            """
            <div style="text-align: center; padding: 14px; 
                        # background: linear-gradient(90deg, #93C5FD, #60A5FA);
                        background: #93C5FD; 
                        color: white; border-radius: 12px; margin-bottom: 14px;">
                <h1>🤖 AgenticAI General Manager</h1>
                <p>Unified Multi-Agent Workflow — Research • Data Analysis • Realtime</p>
            </div>
            """
        )

        # --- Input Section ---
        gr.Markdown("### 💬 Ask a Question or Upload a CSV File")

        with gr.Row():
            with gr.Column(scale=8):
                input_box = gr.Textbox(
                    label="Your Query",
                    placeholder="e.g. 'Show revenue trends' or 'Impact of AI on education'",
                    lines=2,
                )
            with gr.Column(scale=2):
                file_upload = gr.File(
                    label="📂 Upload CSV",
                    type="filepath",
                    file_types=[".csv"],
                    interactive=True,
                )

        run_button = gr.Button("🚀 Run Agent", variant="primary")

        # --- Output Section ---
        output_md = gr.Markdown(label="📄 Analysis Report", elem_id="report-box")

        # ✅ Gallery: clean, responsive grid
        gallery = gr.Gallery(
            label="📊 Generated Charts",
            elem_id="gallery-box",
            columns=[2],
            height="auto",
            show_label=True,
            visible=False,
            allow_preview=True,  # zoom on click
        )

        # --- Run Logic ---
        def _run(prompt, file):
            result, served_charts = run_unified(prompt, file)
            return result, gr.update(value=served_charts, visible=bool(served_charts))

        run_button.click(
            fn=_run,
            inputs=[input_box, file_upload],
            outputs=[output_md, gallery],
        )

        # --- Footer ---
        gr.HTML(
            """
            <div style="text-align: center; padding: 10px; margin-top: 30px; 
                        font-size: 14px; color: gray;">
                Built with ❤️ using <b>LangGraph</b> + <b>Azure OpenAI</b>  
                <br>© 2025 AgenticAI
            </div>
            """
        )

    app.launch(server_name="127.0.0.1", server_port=7863, share=False)

# =======================================================

# ======================================================
if __name__ == "__main__":
    launch_app()
