from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.knowledge.pdf import PDFKnowledgeBase
from agno.vectordb.pgvector import PgVector, SearchType

db_url = "postgresql+psycopg://postgres:postgres@localhost:5532/ai-assistant"
knowledge_base = PDFKnowledgeBase(
    path="./docs",
    vector_db=PgVector(table_name="ai-assistant", db_url=db_url, search_type=SearchType.hybrid),
)
# Load the knowledge base: Comment after first run
knowledge_base.load(upsert=True)

