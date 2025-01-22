from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
from typing import Dict, Any
import os
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from autogen_ext.tools.code_execution import PythonCodeExecutionTool
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class TaskRequest(BaseModel):
    task: str

class TaskResponse(BaseModel):
    result: str
    generated_file: str = None

async def process_task(task: str) -> Dict[str, Any]:
    tool = PythonCodeExecutionTool(LocalCommandLineCodeExecutor(work_dir="coding"))
    agent = AssistantAgent(
        "assistant", 
        OpenAIChatCompletionClient(model="gpt-4o-mini"), 
        tools=[tool], 
        reflect_on_tool_use=True, 
        system_message=" generate one code block for the task and execute it."
    )
    
    result = await Console(
        agent.run_stream(task=task)
    )
    
    # Find the most recently created Python file in the coding directory
    generated_file = None
    if os.path.exists("coding"):
        python_files = [f for f in os.listdir("coding") if f.endswith('.py')]
        if python_files:
            # Sort files by creation time, most recent first
            python_files.sort(key=lambda x: os.path.getctime(os.path.join("coding", x)), reverse=True)
            generated_file = python_files[0]

    return {
        "result": result.messages[-1].content,
        "generated_file": generated_file
    }

@app.post("/process", response_model=TaskResponse)
async def process_request(request: TaskRequest) -> TaskResponse:
    try:
        result = await process_task(request.task)
        return TaskResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/code/{filename}")
async def get_code(filename: str):
    try:
        file_path = os.path.join("coding", filename)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        with open(file_path, 'r') as f:
            content = f.read()
        return {"filename": filename, "content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)