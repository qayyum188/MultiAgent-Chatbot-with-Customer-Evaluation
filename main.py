from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from agents.sales_agent import SalesAgent
from agents.evaluation_agent import EvaluationAgent

# Create FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the absolute path to the static directory
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")

# Mount static files with explicit directory
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Initialize templates with explicit directory
templates = Jinja2Templates(directory=templates_dir)

# Initialize agents
sales_agent = SalesAgent()
evaluation_agent = EvaluationAgent()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/chat")
async def chat(message: str = Form(...)):
    try:
        # Special case for evaluation request
        if message == 'evaluate_conversation':
            evaluation = evaluation_agent.evaluate_customer(sales_agent.conversation_history)
            return {
                "response": "Thank you for chatting!",
                "evaluation": evaluation
            }
        
        # Get response from sales agent
        response = sales_agent.get_response(message)
        
        # Check if this might be the end of conversation
        farewell_indicators = ['call', 'discuss', 'forward', 'thank', 'bye']
        is_farewell = any(word in message.lower() or word in response.lower() 
                         for word in farewell_indicators)
        
        # Only include evaluation if it's a farewell message
        evaluation = None
        if is_farewell:
            evaluation = evaluation_agent.evaluate_customer(sales_agent.conversation_history)
            
        return {
            "response": response,
            "evaluation": evaluation
        }
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return {
            "response": "I apologize, could you please try again?",
            "evaluation": None
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)