"""
Agent implementation for Hustle Buddy.
This file contains the agent setup and functionality.
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.sqlite import SqliteStorage
from .agent_config import AGENT_CONFIG
from dotenv import load_dotenv
import os
from pathlib import Path

# Load environment variables
load_dotenv()

def create_hustle_buddy_agent(knowledge_base=None):
    """
    Create and configure the Hustle Buddy agent.
    
    Args:
        knowledge_base: Optional knowledge base to use with the agent
        
    Returns:
        Configured Agent instance
    """
    # Initialize OpenAI model
    model = OpenAIChat(id="gpt-4o-mini")
    
    # Create the Hustle Buddy agent using the imported configuration
    hustle_buddy = Agent(
        name=AGENT_CONFIG["name"],
        model=model,
        description=AGENT_CONFIG["description"],
        instructions=AGENT_CONFIG["instructions"],
        expected_output=AGENT_CONFIG["expected_output"],
        knowledge=knowledge_base,
        search_knowledge=True,
        **AGENT_CONFIG["agent_settings"]
    )
    
    return hustle_buddy

# Helper functions for task management
tasks = []

def add_task(task_description):
    tasks.append({"description": task_description, "completed": False})
    return f"Task added: {task_description}"

def list_tasks():
    if not tasks:
        return "No tasks found."
    task_list = "\n".join([f"{i+1}. {task['description']} [{'x' if task['completed'] else ' '}]" for i, task in enumerate(tasks)])
    return f"Current tasks:\n{task_list}"

def complete_task(task_index):
    if 0 <= task_index < len(tasks):
        tasks[task_index]["completed"] = True
        return f"Task {task_index + 1} marked as completed."
    return "Invalid task index."

def productivity_tip():
    tips = [
        "Break tasks into smaller steps to avoid feeling overwhelmed.",
        "Use the Pomodoro technique: Work for 25 minutes, then take a 5-minute break.",
        "Prioritize tasks using the Eisenhower Matrix (Urgent vs. Important)."
    ]
    import random
    return random.choice(tips) 