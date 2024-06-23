from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Add this middleware to enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    # allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Disable automatic redirecting for trailing slashes
app.router.redirect_slashes = False

# Example data (in-memory database)
tasks_db = []

# Pydantic model for Task
class Task(BaseModel):
    title: str
    description: str = None

@app.get("/")
async def read_root():
    return {"message": "Hello, this is the root of the API!"}

# Create a new task
@app.post("/tasks/", response_model=Task)
async def create_task(task: Task):
    # Append the new task to the in-memory database
    tasks_db.append(task)
    return task

# Get all tasks
@app.get("/tasks/", response_model=List[Task])
async def read_tasks():
    # Return all tasks in the in-memory database
    return tasks_db

# Get a specific task by ID
@app.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: int):
    # Check if the task_id is within valid bounds
    if task_id < 0 or task_id >= len(tasks_db):
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Return the specific task by ID
    return tasks_db[task_id]

# Update a task by ID
@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, updated_task: Task):
    # Check if the task_id is within valid bounds
    if task_id < 0 or task_id >= len(tasks_db):
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update the task in the in-memory database
    tasks_db[task_id] = updated_task
    return updated_task

# Delete a task by ID
@app.delete("/tasks/{task_id}", response_model=Task)
async def delete_task(task_id: int):
    # Check if the task_id is within valid bounds
    if task_id < 0 or task_id >= len(tasks_db):
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Pop (remove and return) the task from the in-memory database
    deleted_task = tasks_db.pop(task_id)
    return deleted_task