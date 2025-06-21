"""
Knowledge base implementation for Hustle Buddy.
This file sets up the PDF knowledge base for the agent.
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.knowledge.pdf import PDFKnowledgeBase
from agno.vectordb.pgvector import PgVector, SearchType
from pathlib import Path

# Configuration
import os

# Use environment variable for database URL, fallback to localhost for development
db_url = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5532/ai-assistant")
docs_folder = Path("docs")

# Initialize the knowledge base
knowledge_base = PDFKnowledgeBase(
    path=docs_folder,
    vector_db=PgVector(table_name="ai-assistant", db_url=db_url, search_type=SearchType.hybrid),
)

def get_knowledge_base():
    """
    Returns the configured knowledge base instance.
    
    Returns:
        PDFKnowledgeBase: The configured knowledge base
    """
    return knowledge_base

def load_knowledge_base(recreate=False):
    """
    Load or reload the knowledge base.
    
    Args:
        recreate (bool): Whether to recreate the vector database
    """
    knowledge_base.load(upsert=recreate)

# Note: The knowledge base is not loaded automatically
# Call load_knowledge_base() when needed

