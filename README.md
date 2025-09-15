# 🎓 Smart Student Agent

A Coral-Protocol-powered AI agent that acts as a multi-talented academic assistant, helping students with study plans, concept explanations, and research.

## ✨ Features

*   **🤖 Agentic & Autonomous:** Leverages LangChain and Mistral AI to autonomously select the right tool for each student query.
*   **🛠️ Tool Ecosystem:** Equipped with specialized tools for:
    *   Generating comprehensive study plans (`create_study_plan`)
    *   Explaining complex concepts at different levels (`explain_concept`)
    *   Generating practice questions (`generate_practice_questions`)
    *   Assisting with academic research (`research_assistant`)
*   **🌐 Multi-Agent Ready:** Integrated with Coral Protocol via MCP to discover and collaborate with other agents in the ecosystem.
*   **💬 Dual Interface:** Accessible via a modern web UI or a direct REST API.

## 🏗️ Tech Stack

*   **Frameworks:** LangChain, Flask
*   **AI Models:** Mistral AI, AI/ML API
*   **Multi-Agent Protocol:** Coral Protocol (MCP)
*   **Language:** Python 3.10+

## 🚀 Quick Start

### Prerequisites
*   Python 3.10+
*   `uv` package installer (`pip install uv`)
*   Mistral AI API Key
*   (Optional) AI/ML API Key

### Installation & Running

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/smart-student-agent.git
    cd smart-student-agent
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure environment variables:**
    Copy the `.env.sample` file to `.env` and fill in your API keys.
    ```bash
    cp .env.sample .env
    # Now edit .env with your text editor (nano, vim, code)
    ```

5.  **Run the application:**
    ```bash
    python app.py
    ```
    The web interface will be available at `http://localhost:5000`.

## 🔧 API Usage

The agent can also be used headlessly via its API:

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Explain quantum entanglement to a beginner"}'
