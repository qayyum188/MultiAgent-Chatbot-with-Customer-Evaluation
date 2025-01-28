# agents/sales_agent.py
import google.generativeai as genai
from os import getenv
from dotenv import load_dotenv

load_dotenv()

class SalesAgent:
    def __init__(self):
        api_key = getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
            
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.conversation_history = []
        self.has_name = False
        self.customer_name = ""
        
        # Quick responses dictionary
        self.quick_responses = {
            "hello": "Hi! I'm the EvrenAI Sales Assistant. May I know your name?",
            "hi": "Hello! I'm the EvrenAI Sales Assistant. May I know your name?",
            "bye": "Thank you for visiting EvrenAI. Please come again!",
            "goodbye": "Thank you for visiting EvrenAI. Please come again!",
            "ok": "Is there anything else I can help you with?"
        }
    
    def get_response(self, user_input):
        try:
            # Check for quick responses first
            lower_input = user_input.lower()
            if lower_input in self.quick_responses and not self.has_name:
                return self.quick_responses[lower_input]
            
            # Add user input to history
            self.conversation_history.append({"role": "user", "content": user_input})
            
            # If we don't have the name yet, assume this is the name
            if not self.has_name:
                self.customer_name = user_input
                self.has_name = True
                return f"Hi {self.customer_name}! How can I assist you today?"
            
            # Create focused prompt
            prompt = f"""You are EvrenAI's Sales Assistant talking to {self.customer_name}.
            Keep responses short, friendly, and focused.
            If user is leaving, thank them and ask them to come again.
            
            Previous messages: {str(self.conversation_history[-3:])}
            Current message: {user_input}
            
            Respond naturally:"""
            
            response = self.model.generate_content(prompt)
            
            if not response or not hasattr(response, 'text'):
                return "I apologize, could you please rephrase that?"
            
            self.conversation_history.append({"role": "assistant", "content": response.text})
            return response.text
            
        except Exception as e:
            print(f"Error in get_response: {str(e)}")
            return "I apologize, could you please rephrase that?"