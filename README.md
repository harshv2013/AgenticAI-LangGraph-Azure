# 🤖 AgenticAI: Multi-Agent AI Framework

<div align="center">

**A powerful, unified multi-agent AI framework for research, data analysis, and real-time information retrieval**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Azure OpenAI](https://img.shields.io/badge/Azure-OpenAI-0078D4.svg)](https://azure.microsoft.com/en-us/products/ai-services/openai-service/)
[![LangGraph](https://img.shields.io/badge/Built%20with-LangGraph-blueviolet.svg)](https://github.com/langchain-ai/langgraph)

[Features](#-features) • [Quick Start](#-quick-start) • [Installation](#-installation) • [Documentation](#-documentation)

</div>

---

## ✨ What is AgenticAI?

AgenticAI is an intelligent multi-agent orchestration framework that leverages **LangGraph**, **Azure OpenAI**, and **Tavily API** to automate complex workflows. Whether you need to conduct in-depth research, analyze data, or fetch real-time information, AgenticAI handles it all through a sleek, unified interface.

Built with production-grade architecture, it combines autonomous agents with collaborative workflows to deliver insights faster and smarter.

---

## 🎯 Features

### 🧠 Research & Report Generation
AI-driven multi-step reasoning that expands queries, searches comprehensively, synthesizes findings, and generates polished literature-style reports with citations and insights.

### 📊 Data Analysis & Visualization
Upload CSVs and let autonomous agents handle exploratory data analysis (EDA), generate Python code, create beautiful visualizations, and deliver natural language insights.

### 🌍 Real-Time Information Retrieval
Live weather updates, breaking news, price tracking, and market data—all fetched and summarized intelligently through Tavily's powerful search API.

### 🎮 Seamless User Experience
Single Gradio interface combining all capabilities. No switching between tools, no context loss. Everything you need in one place.

---

## 🚀 Quick Start

Get AgenticAI up and running in under 5 minutes:

```bash
# 1. Clone the repository
git clone https://github.com/harshv2013/AgenticAI-LangGraph-Azure.git
cd AgenticAI-LangGraph-Azure

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env with your Azure OpenAI & Tavily credentials

# 5. Launch the app
python gradio_app.py
```

Open your browser to **http://127.0.0.1:7863** and start exploring! 🎉

---

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.10+** installed ([download here](https://www.python.org/downloads/))
- **pip** package manager
- **Azure OpenAI Account** with a deployed GPT-4o model
- **Tavily API Key** ([get one free here](https://tavily.com/))
- *(Optional)* **Git** for version control

---

## 🔧 Installation & Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/harshv2013/AgenticAI-LangGraph-Azure.git
cd AgenticAI-LangGraph-Azure
```

### Step 2: Virtual Environment Setup

```bash
# Create environment
python -m venv .venv

# Activate environment
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root:

```env
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://<your-resource-name>.openai.azure.com/
AZURE_OPENAI_API_KEY=<your-api-key>
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o

# Tavily API Configuration
TAVILY_API_KEY=<your-tavily-api-key>
```

> 💡 **Tip:** Reference `.env.example` for a complete configuration template.

---

## ▶️ Running the Application

### Option 1: Web Interface (Recommended)

Launch the full-featured Gradio interface:

```bash
python gradio_app.py
```

Then open **http://127.0.0.1:7863** in your browser.

### Option 2: Command Line (Development & Testing)

Run individual workflows directly:

```bash
# Research workflow
python main.py --prompt "Impact of AI on Healthcare"

# Data analysis workflow
python main.py --file "sales_data.csv"

# Real-time data fetching
python main.py --prompt "What's the weather in Delhi?"
```

---

## 📁 Project Structure

```
AgenticAI-LangGraph-Azure/
├── .env                           # Environment variables (create from .env.example)
├── .env.example                   # Template for environment setup
├── .gitignore                     # Git ignore rules
├── requirements.txt               # Python dependencies
│
├── main.py                        # CLI entry point
├── gradio_app.py                  # Web interface entry point
│
├── sales_data.csv                 # Sample data file
├── charts_*.png                   # Generated visualization outputs
│
├── 📂 data_analysis_agents/       # CSV analysis & visualization agents
│   ├── analyzer.py                # EDA & statistical analysis
│   ├── ingest.py                  # CSV ingestion pipeline
│   ├── insight_writer.py          # Natural language insights
│   ├── report_builder.py          # Report generation
│   └── visualizer.py              # Chart generation
│
├── 📂 realtime_agents/            # Real-time data retrieval agents
│   ├── delivery.py                # Output formatting
│   ├── fetch.py                   # Data fetching
│   ├── query.py                   # Query formulation
│   └── summarizer.py              # Data summarization
│
├── 📂 research_agents/            # Research workflow agents
│   ├── delivery.py                # Final report delivery
│   ├── email_tool.py              # Email integration
│   ├── planner.py                 # Research planning
│   ├── reviewer.py                # Content review & refinement
│   ├── search.py                  # Search execution
│   ├── synthesizer.py             # Findings synthesis
│   └── writer.py                  # Report writing
│
├── 📂 services/                   # Core services & utilities
│   ├── azure_client.py            # Azure OpenAI integration
│   ├── data_fetchers.py           # Data retrieval helpers
│   ├── router_llm.py              # Workflow routing logic
│   ├── storage.py                 # Data storage utilities
│   ├── tavily_client.py           # Tavily API integration
│   └── vector_store.py            # Vector database operations
│
└── 📂 workflows/                  # LangGraph workflow definitions
    ├── data_analysis_graph.py     # CSV → Analysis → Report pipeline
    ├── general_manager_graph.py   # Intelligent workflow router
    ├── realtime_graph.py          # Real-time data retrieval pipeline
    └── research_graph.py          # Multi-step research pipeline
```

---

## 🔌 Workflows & Capabilities

| Workflow | Purpose | Use Case |
|----------|---------|----------|
| **Research Graph** | Multi-agent reasoning & synthesis | Generate comprehensive reports on complex topics |
| **Data Analysis Graph** | CSV ingestion, EDA, visualization | Analyze datasets and generate charts automatically |
| **Realtime Graph** | Live data fetching & summarization | Get current weather, news, prices, market data |
| **Manager Graph** | Intelligent workflow routing | Automatically routes to the appropriate pipeline |

---

## 💡 Example Prompts

Try these to experience AgenticAI's capabilities:

**Research Mode**
```
Explain how Agentic AI is transforming modern industries with specific use cases and business impact.
```

**Real-Time Mode**
```
What's the current temperature and weather forecast in Gorakhpur for the next 3 days?
```

**Data Analysis Mode**
```
Show me the top 5 most profitable regions from the sales data and create a comparison chart.
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Workflow Orchestration** | LangGraph |
| **LLM Engine** | Azure OpenAI (GPT-4o) |
| **Search API** | Tavily |
| **Web Interface** | Gradio |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Matplotlib, Seaborn |
| **Vector Operations** | LangChain, FAISS |

---

## 🎓 Development Guide

### Local Development Setup

```bash
# Always run in a fresh terminal with venv activated
source .venv/bin/activate

# Run with auto-reload
python gradio_app.py
```

### Debugging Tips

- Use `print()` statements or Python `logging` module for workflow debugging
- Check the Gradio console output for real-time logs
- Keep `.env` file private—never commit credentials to version control
- For UI changes, restart the Gradio server (Ctrl+C, then re-run)

### Best Practices

- **Modular Agent Design:** Keep agents focused on single responsibilities
- **Error Handling:** Wrap external API calls with try-catch blocks
- **Logging:** Use structured logging for production monitoring
- **Testing:** Write unit tests for critical agent functions

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License**—feel free to use, modify, and distribute it. See the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Built with ❤️ by **Harsh Vardhan**

Empowering intelligent automation through collaborative AI agents.

---

## 📞 Support & Feedback

- **Issues:** Found a bug? [Create an issue](https://github.com/harshv2013/AgenticAI-LangGraph-Azure/issues)
- **Discussions:** Have questions? [Start a discussion](https://github.com/harshv2013/AgenticAI-LangGraph-Azure/discussions)
- **Email:** [harsh2013@gmail.com]

---

<div align="center">

**Made with ❤️ for the AI community**

⭐ If you find this helpful, please consider giving it a star!

</div>