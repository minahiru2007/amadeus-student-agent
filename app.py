from flask import Flask, request, jsonify, render_template
from smart_student_agent import SmartStudentAgent
import asyncio
import json
from datetime import datetime

app = Flask(__name__)
agent = None

# Initialize agent when app starts
with app.app_context():
    agent = SmartStudentAgent()
    print("🤖 Smart Student Agent initialized!")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/tools')
def get_tools():
    """Return available tools for the UI"""
    tools_info = [
        {
            'name': 'Study Plan Creator',
            'description': 'Create comprehensive study plans with time allocation',
            'parameters': ['topic', 'hours', 'learning style'],
            'example': 'Create a 10-hour study plan for calculus for visual learners'
        },
        {
            'name': 'Concept Explainer',
            'description': 'Get detailed explanations of complex concepts',
            'parameters': ['concept', 'difficulty level', 'examples'],
            'example': 'Explain quantum physics to a beginner with 3 examples'
        },
        {
            'name': 'Study Timer',
            'description': 'Set a study timer for focused learning sessions',
            'parameters': ['duration (minutes)', 'subject', 'timer name (optional)'],
            'example': 'Set a 25-minute timer for math practice'
        },
        {
            'name': 'Pomodoro Session',
            'description': 'Start a Pomodoro technique session (25min focus, 5min break)',
            'parameters': ['subject', 'number of sessions (optional)'],
            'example': 'Start a Pomodoro session for physics with 4 sessions'
        },
        {
            'name': 'Practice Questions',
            'description': 'Generate practice questions with answers',
            'parameters': ['topic', 'difficulty', 'count'],
            'example': 'Generate 5 medium difficulty questions about algebra'
        },
        {
            'name': 'Research Assistant',
            'description': 'Get research help and academic resources',
            'parameters': ['topic', 'sources needed'],
            'example': 'Help me research machine learning applications in education'
        }
    ]
    return jsonify(tools_info)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    query = data.get('query', '')
    
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    try:
        response = asyncio.run(agent.run(query))
        return jsonify({
            'response': response,
            'suggestions': get_followup_suggestions(query)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_followup_suggestions(query):
    """Generate follow-up suggestions based on the query"""
    suggestions = []
    
    # Study-related queries
    if any(keyword in query.lower() for keyword in ['study', 'learn', 'subject', 'topic']):
        suggestions.extend([
            "Create a study plan for this topic",
            "Set a timer for focused study",
            "Generate practice questions"
        ])
    
    # Concept explanation queries
    if any(keyword in query.lower() for keyword in ['explain', 'what is', 'how does', 'define']):
        suggestions.extend([
            "Explain this in more detail",
            "Give me examples of this concept",
            "Break this down into simpler terms"
        ])
    
    # Timer-related queries
    if any(keyword in query.lower() for keyword in ['timer', 'pomodoro', 'focus', 'study session']):
        suggestions.extend([
            "Show my active timers",
            "Start a Pomodoro session",
            "Set another timer"
        ])
    
    # Add some general suggestions
    suggestions.extend([
        "Find research papers about this",
        "Help me with a different topic",
        "What other subjects can you help with?"
    ])
    
    return suggestions[:4]  # Return up to 4 suggestions

@app.route('/api/timers', methods=['GET'])
def get_timers():
    """Get active timers"""
    try:
        # Access the agent's active timers
        active_timers = []
        current_time = datetime.now()
        
        for timer_id, timer_info in agent.active_timers.items():
            if timer_info["status"] == "active":
                time_left = timer_info["end_time"] - current_time
                minutes_left = max(0, int(time_left.total_seconds() / 60))
                seconds_left = max(0, int(time_left.total_seconds() % 60))
                
                active_timers.append({
                    "id": timer_id,
                    "name": timer_info["name"],
                    "subject": timer_info["subject"],
                    "duration": timer_info["duration"],
                    "minutes_left": minutes_left,
                    "seconds_left": seconds_left,
                    "end_time": timer_info["end_time"].isoformat()
                })
        
        return jsonify({"timers": active_timers})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/timers/<int:timer_id>', methods=['DELETE'])
def cancel_timer(timer_id):
    """Cancel a specific timer"""
    try:
        # Use the agent's run method to cancel the timer
        response = asyncio.run(agent.run(f"Cancel timer {timer_id}"))
        return jsonify({"message": response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/pomodoro', methods=['GET'])
def get_pomodoro_status():
    """Get current Pomodoro session status"""
    try:
        if agent.pomodoro_session and agent.pomodoro_session["status"] == "active":
            session_info = {
                "subject": agent.pomodoro_session["subject"],
                "current_session": agent.pomodoro_session["current_session"],
                "total_sessions": agent.pomodoro_session["total_sessions"],
                "phase": agent.pomodoro_session["phase"],
                "status": agent.pomodoro_session["status"]
            }
            return jsonify(session_info)
        else:
            return jsonify({"status": "no_active_session"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
