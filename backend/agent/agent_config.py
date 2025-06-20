"""
Agent configuration loader for Hustle Buddy.
This file loads the agent configuration from agent-config.json.
"""

import json
import os
from pathlib import Path

def load_agent_config():
    """
    Load the agent configuration from the JSON file.
    
    Returns:
        dict: The agent configuration
    """
    config_path = Path(__file__).parent.parent / "agent-config.json"
    
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"Error loading agent configuration: {e}")
        # Return a minimal default configuration
        return {
            "name": "HustleBuddy",
            "description": "AI model response evaluator",
            "instructions": ["Evaluate model responses"],
            "expected_output": "Evaluation results",
            "agent_settings": {
                "add_datetime_to_instructions": True,
                "add_history_to_messages": True,
                "num_history_runs": 3,
                "show_tool_calls": True,
                "markdown": True
            }
        }

# Load the configuration when the module is imported
AGENT_CONFIG = load_agent_config() 