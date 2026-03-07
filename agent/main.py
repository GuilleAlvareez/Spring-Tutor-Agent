from fastapi import FastAPI, Request
from pydantic import BaseModel
from agent import get_response

# Crea la aplicación FastAPI, equivalente al @SpringBootApplication de Spring
app = FastAPI()

# Modelo de entrada, equivalente al ChatRequest.java de Spring
class ChatRequest(BaseModel):
    message: str

# Modelo de salida, equivalente al ChatResponse.java de Spring
class ChatResponse(BaseModel):
    response: str

# Endpoint de salud, equivalente al @GetMapping("/health") de Spring
@app.get("/health")
def health():
    return {"status": "Agent is running!"}

# Endpoint principal, equivalente al @PostMapping("/message") de Spring
@app.post("/chat")
def chat(request: ChatRequest):
    response = get_response(request.message)
    return ChatResponse(response=response)