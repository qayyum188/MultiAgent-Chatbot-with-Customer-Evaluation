# agents/evaluation_agent.py
import google.generativeai as genai
from os import getenv
from dotenv import load_dotenv

load_dotenv()

class EvaluationAgent:
    def __init__(self):
        api_key = getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
            
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
    def evaluate_customer(self, conversation_history):
        try:
            prompt = """Generate a very brief customer evaluation in exactly this format:

• Interest Level: [1-10]
• Purchase Likelihood: [Yes/No]
• Key Requirements: [1-2 key points]

Keep each point on a new line with bullet points. Do not add any other text."""
            
            response = self.model.generate_content(prompt + f"\n\nConversation: {conversation_history}")
            return response.text if response and hasattr(response, 'text') else "Unable to generate evaluation"
            
        except Exception as e:
            print(f"Error in evaluation: {str(e)}")
            return "Unable to generate evaluation"