import os
import asyncio
import requests
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, initialize_agent, AgentType
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI
from langchain_mcp_adapters.client import MultiServerMCPClient
import time
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

class SmartStudentAgent:
    def __init__(self):
        self.coral_sse_url = os.getenv("CORAL_SSE_URL", "http://localhost:5555/devmode/exampleApplication/privkey/session1/sse")
        self.agent_id = os.getenv("CORAL_AGENT_ID", "smart_student_agent")
        
        # Initialize AI services
        self.mistral_model = ChatMistralAI(
            model="mistral-small-latest",
            api_key=os.getenv("MISTRAL_API_KEY")
        )
        
        self.ai_ml_api_key = os.getenv("AI_ML_API_KEY")
        
        self.client = None
        self.agent_executor = None
        self.active_timers = {}  # Dictionary to track active timers
        self.timer_id_counter = 1  # Counter for timer IDs
        self.pomodoro_session = None  # Track Pomodoro sessions
        
    async def initialize(self):
        """Initialize the agent with enhanced capabilities"""
        # Coral Server connection
        server_url = f"{self.coral_sse_url}?agentId={self.agent_id}&agentDescription=Smart+Student+Assistant"
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                self.client = MultiServerMCPClient(server_url)
                print("✅ Connected to Coral Server successfully!")
                
                try:
                    coral_tools = await self.client.get_tools()
                    print(f"🛠️  Retrieved {len(coral_tools)} Coral tools")
                except Exception as e:
                    print(f"⚠️  Coral tools error: {e}")
                    coral_tools = []
                
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"Connection attempt {attempt + 1} failed: {e}. Retrying...")
                    await asyncio.sleep(2)
                else:
                    print(f"Using fallback mode without Coral Server: {e}")
                    self.client = None
                    coral_tools = []
                    break
        
        # Enhanced tools with better error handling
        student_tools = self._create_enhanced_tools()
        all_tools = coral_tools + student_tools
        
        # Use structured chat agent for multi-input tools
        self.agent_executor = initialize_agent(
            all_tools, 
            self.mistral_model,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=5
        )
    
    def _call_ai_ml_api(self, prompt: str, model: str = "llama3") -> str:
        """Call AI/ML API without stop parameter"""
        if not self.ai_ml_api_key:
            return "AI/ML API not configured"
            
        try:
            headers = {
                "Authorization": f"Bearer {self.ai_ml_api_key}",
                "Content-Type": "application/json"
            }
            
            # Payload without stop parameter
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 1000,
                "temperature": 0.7
            }
            
            response = requests.post(
                "https://api.aimlapi.com/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                return f"AI/ML API Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"AI/ML API Call Failed: {str(e)}"
    
    def _create_enhanced_tools(self):
        """Create enhanced tools for student assistance including timer functionality"""
        from langchain.tools import tool
        
        @tool
        def create_study_plan(topic: str, hours_available: int, learning_style: str = "visual"):
            """Create a detailed study plan - autonomous goal achievement"""
            prompt = f"""Create a comprehensive {hours_available}-hour study plan for {topic} 
            for {learning_style} learners. Include learning objectives, time allocation, 
            resources, practice exercises, and assessment methods."""
            
            return self._call_ai_ml_api(prompt, "llama3")
        
        @tool
        def explain_concept(concept: str, level: str = "beginner"):
            """Explain a academic concept at appropriate level"""
            prompt = f"""Explain {concept} to a {level} level student. Use analogies and simple language.
            Structure the explanation with:
            1. Basic definition
            2. Key principles
            3. Real-world applications
            4. Common misconceptions
            5. Summary"""
            
            return self._call_ai_ml_api(prompt, "llama3")
        
        @tool
        def set_study_timer(duration_minutes: int, subject: str, timer_name: str = "Study Session"):
            """Set a study timer for a specific duration and subject"""
            timer_id = self.timer_id_counter
            self.timer_id_counter += 1
            
            # Store timer information
            end_time = datetime.now() + timedelta(minutes=duration_minutes)
            self.active_timers[timer_id] = {
                "subject": subject,
                "duration": duration_minutes,
                "end_time": end_time,
                "name": timer_name,
                "status": "active"
            }
            
            # Start the timer in the background
            asyncio.create_task(self._run_timer(timer_id, duration_minutes * 60))
            
            return f"⏰ Timer set for {duration_minutes} minutes for {subject}. Timer ID: {timer_id}"
        
        @tool
        def list_active_timers():
            """List all currently active timers"""
            if not self.active_timers:
                return "No active timers."
            
            timer_list = []
            for timer_id, timer_info in self.active_timers.items():
                if timer_info["status"] == "active":
                    time_left = timer_info["end_time"] - datetime.now()
                    minutes_left = max(0, int(time_left.total_seconds() / 60))
                    timer_list.append(
                        f"ID {timer_id}: {timer_info['name']} - {timer_info['subject']} "
                        f"({minutes_left} minutes remaining)"
                    )
            
            return "\n".join(timer_list) if timer_list else "No active timers."
        
        @tool
        def cancel_timer(timer_id: int):
            """Cancel an active timer by its ID"""
            if timer_id in self.active_timers:
                self.active_timers[timer_id]["status"] = "cancelled"
                return f"Timer {timer_id} has been cancelled."
            else:
                return f"No timer found with ID {timer_id}."
        
        @tool
        def start_pomodoro_session(subject: str, sessions: int = 4):
            """Start a Pomodoro technique session (25min focus, 5min break)"""
            self.pomodoro_session = {
                "subject": subject,
                "total_sessions": sessions,
                "current_session": 1,
                "phase": "focus",  # or "break"
                "status": "active"
            }
            
            # Start the first focus session
            asyncio.create_task(self._run_pomodoro_session())
            
            return (f"🍅 Starting Pomodoro session for {subject}: {sessions} cycles of "
                   f"25min focus + 5min breaks. Session 1/{sessions} started.")
        
        return [
            create_study_plan,
            explain_concept,
            set_study_timer,
            list_active_timers,
            cancel_timer,
            start_pomodoro_session
        ]
    
    async def _run_timer(self, timer_id, duration_seconds):
        """Background task to handle timer expiration"""
        await asyncio.sleep(duration_seconds)
        
        if (timer_id in self.active_timers and 
            self.active_timers[timer_id]["status"] == "active"):
            timer_info = self.active_timers[timer_id]
            
            # Timer completed successfully
            self.active_timers[timer_id]["status"] = "completed"
            
            # Here you could integrate with Coral's notification system
            print(f"⏰ Timer completed: {timer_info['name']} for {timer_info['subject']}")
            
            # If you have access to the Coral client, you could send a notification
            if self.client:
                try:
                    await self.client.call_tool(
                        "send_message", 
                        {
                            "content": f"Timer completed: {timer_info['name']} for {timer_info['subject']}",
                            "mentions": ["user"]
                        }
                    )
                except Exception as e:
                    print(f"Failed to send Coral notification: {e}")
    
    async def _run_pomodoro_session(self):
        """Background task to handle Pomodoro sessions"""
        while (self.pomodoro_session and 
               self.pomodoro_session["status"] == "active"):
            
            if self.pomodoro_session["phase"] == "focus":
                # 25-minute focus session
                await asyncio.sleep(25 * 60)
                
                if not self.pomodoro_session or self.pomodoro_session["status"] != "active":
                    break
                    
                # Notify end of focus session
                print(f"🍅 Focus session {self.pomodoro_session['current_session']} completed!")
                
                # Check if all sessions are done
                if self.pomodoro_session["current_session"] >= self.pomodoro_session["total_sessions"]:
                    self.pomodoro_session["status"] = "completed"
                    print("🎉 Pomodoro session completed!")
                    break
                
                # Switch to break phase
                self.pomodoro_session["phase"] = "break"
                print("☕ Take a 5-minute break")
                
                # 5-minute break
                await asyncio.sleep(5 * 60)
                
                if not self.pomodoro_session or self.pomodoro_session["status"] != "active":
                    break
                    
                # Switch back to focus and increment session
                self.pomodoro_session["phase"] = "focus"
                self.pomodoro_session["current_session"] += 1
                print(f"🎯 Starting focus session {self.pomodoro_session['current_session']}")
    
    async def run(self, query):
        """Run the agent with a student query"""
        if not self.agent_executor:
            await self.initialize()
        
        try:
            result = self.agent_executor.run(query)
            return result
        except Exception as e:
            return f"Error: {str(e)}"

# Test the agent directly
if __name__ == "__main__":
    async def test_agent():
        agent = SmartStudentAgent()
        
        # Test timer functionality
        response = await agent.run("Set a 1-minute timer for math practice")
        print(response)
        
        # Test listing timers
        response = await agent.run("Show my active timers")
        print(response)
        
        # Test concept explanation
        response = await agent.run("Explain quantum physics to a beginner")
        print(response)
    
    asyncio.run(test_agent())
