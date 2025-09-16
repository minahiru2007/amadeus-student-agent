🎓 Amadeus Study Agent
An AI-powered academic assistant built with Coral Protocol that helps students with study planning, concept explanations, research assistance, and time management through intelligent timer systems.
✨ Features

    🤖 Intelligent Study Assistance: AI-powered study plan creation and concept explanations

    ⏰ Smart Timer System: Study timers and Pomodoro technique implementation

    🌐 Multi-Agent Ready: Coral Protocol integration for collaborative AI ecosystems

    💬 Interactive Web Interface: Modern, responsive UI inspired by DeepSeek

    🔧 Tool Ecosystem: Specialized tools for different academic tasks

    🎯 Autonomous Decision Making: AI agent that selects appropriate tools based on student needs

🏗️ Tech Stack

    Backend: Python, Flask, LangChain

    AI Models: Mistral AI, AI/ML API

    Multi-Agent Protocol: Coral Protocol (MCP)

    Frontend: HTML5, CSS3, JavaScript

🚀 Quick Start
Prerequisites

    Python 3.11+

    Git

    Mistral AI API Key

    (Optional) AI/ML API Key
Installation

    Clone the repository
    bash

git clone https://github.com/minahiru/smart-student-agent.git
cd smart-student-agent

Create a virtual environment


python -m venv venv
source venv/bin/activate

Install dependencies
bash

pip install -r requirements.txt

Configure environment variables
bash

cp .env.sample .env
# Edit .env with your API keys

Run the application
bash

python app.py

    Access the web interface
    Open your browser and navigate to http://localhost:5000

🪸 Coral Protocol Integration

The Amadeus Study Agent is a Coralized Agent that connects to the Coral Server using the Model Context Protocol (MCP). This enables:

    Multi-Agent Collaboration: Discover and work with other agents in the Coral ecosystem

    Tool Sharing: Make your agent's capabilities available to other Coral-connected agents

    Enhanced Capabilities: Access tools and services from the broader Coral network

Connecting to Coral Server

The agent automatically connects to the Coral Server using the configuration in your .env file:
bash

CORAL_SSE_URL=http://localhost:5555/devmode/exampleApplication/privkey/session1/sse
CORAL_AGENT_ID=amadeus_study_agent

📖 Usage Examples
Study Plan Creation

"Create a 10-hour study plan for quantum physics for visual learners"

Concept Explanation
text

"Explain wave-particle duality to a beginner with practical examples"

Timer Management


"Set a 25-minute timer for calculus practice"
"Start a Pomodoro session for physics with 4 sessions"

Research Assistance

"Help me research applications of machine learning in education"

🔧 API Endpoints

The Amadeus Study Agent provides a RESTful API:

    POST /api/chat - Send queries to the agent

    GET /api/tools - List available tools

    GET /api/timers - Get active timers

    DELETE /api/timers/{id} - Cancel a timer

    GET /api/pomodoro - Check Pomodoro session status

Example API Usage

curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Explain quantum entanglement to a beginner"}'

🎯 Hackathon Alignment

This project fulfills the Agent Builder track requirements for the Coral Protocol hackathon by:

    Creating a Reusable Agent: The Amadeus Study Agent can be discovered and integrated into other systems via the Coral Registry

    Coral Protocol Integration: Full MCP compatibility for multi-agent collaboration

    Practical Application: Solves real-world problems in education and student productivity

    Clean Architecture: Modular, maintainable code that others can build upon

🏆 Team Amadeus

Team Members: Minahil, Maida
Hackathon: Internet Of Agents
Track: Agent Builder

📁 Project Structure

smart-student-agent/
├── app.py                 # Flask application and API routes
├── smart_student_agent.py # Main agent class with Coral integration
├── requirements.txt       # Python dependencies
├── .env.sample           # Environment variables template
├── README.md             # This file
└── templates/
    └── index.html        # Web interface

🤝 Contributing

We welcome contributions! Please feel free to:

    Fork the repository

    Create a feature branch (git checkout -b feature/amazing-feature)

    Commit your changes (git commit -m 'Add amazing feature')

    Push to the branch (git push origin feature/amazing-feature)

    Open a Pull Request

📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
🌐 Resources

    Coral Protocol Documentation

    Mistral AI API

    LangChain Documentation

    Flask Documentation

🆘 Support

If you encounter any issues or have questions:

    Check the GitHub Issues for existing solutions

    Create a new issue with detailed information about your problem

    Contact the development team
