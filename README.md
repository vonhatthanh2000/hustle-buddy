# HustleBuddy 🚀

**An intelligent AI model evaluation platform that compares and analyzes AI model responses with comprehensive evaluation frameworks.**

## 🚀 Quick Start (Recommended: Docker)

**⚠️ IMPORTANT: Start with Docker setup first! If Docker doesn't work, follow the manual setup below.**

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- OpenAI API key ([get one here](https://platform.openai.com/api-keys))

### Step 1: Clone the Repository

```bash
git clone <your-repo-url>
cd hustle-buddy
```

### Step 2: Set Up Environment Variables

```bash
# Create environment file
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
# Replace 'your_openai_api_key_here' with your actual OpenAI API key
```

### Step 3: Run with Docker (Recommended)

```bash
# Option A: Use the automated script
./docker-run.sh

# Option B: Manual Docker Compose
docker-compose up --build
```

**That's it! 🎉**

### Access Your Application:

- **Frontend (Web Interface)**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

---

## 🛠️ Manual Setup (If Docker Doesn't Work)

If Docker setup fails or you prefer running services separately, follow these steps:

### Prerequisites for Manual Setup

- Python 3.8+
- Node.js 16+
- PostgreSQL with pgvector extension
- OpenAI API key

### Backend Setup

1. **Navigate to backend directory:**

   ```bash
   cd backend
   ```

2. **Create and activate virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database:**

   ```bash
   # Start PostgreSQL with pgvector (using Docker)
   docker run -d \
     --name hustle-buddy-db \
     -e POSTGRES_DB=ai-assistant \
     -e POSTGRES_USER=postgres \
     -e POSTGRES_PASSWORD=postgres \
     -p 5432:5432 \
     agnohq/pgvector:16
   ```

5. **Set environment variables:**

   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/ai-assistant"
   ```

6. **Start the backend server:**
   ```bash
   python main.py
   ```
   The backend will be available at http://localhost:8000

### Frontend Setup

1. **Open a new terminal and navigate to frontend:**

   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies:**

   ```bash
   npm install
   ```

3. **Start the frontend development server:**
   ```bash
   npm start
   ```
   The frontend will be available at http://localhost:3000

---

## 📋 What is HustleBuddy?

HustleBuddy is an intelligent AI model evaluation platform that compares and analyzes responses from three different AI models. It provides comprehensive analysis using multiple evaluation rubrics to help you understand which model performs better for specific tasks.

### 🌟 Key Features

- **AI Model Response Comparison**: Analyze and compare outputs from three different AI models
- **Comprehensive Evaluation Framework**: 10+ evaluation rubrics (6 critical + 4 non-critical)
- **Knowledge-Enhanced Analysis**: Specialized knowledge base with Ballerina programming documentation
- **RESTful API**: FastAPI backend with comprehensive endpoints
- **Modern Web Interface**: React-based frontend for easy interaction
- **Vector Database Integration**: Hybrid search with PostgreSQL and pgvector

### 🧠 Evaluation Rubrics

#### Critical Rubrics:

1. **Relevance to Prompt** - How well content addresses the given prompt
2. **Clarity of Expression** - Language clarity and readability
3. **Depth of Analysis** - Thoroughness of information provided
4. **Accuracy of Information** - Factual correctness verification
5. **Logical Structure** - Organization and flow of arguments
6. **Engagement Level** - Content engagement quality

#### Non-Critical Rubrics:

1. **Use of Examples** - Support for claims with examples
2. **Tone and Style** - Appropriateness for target audience
3. **Conciseness** - Information presentation efficiency
4. **Originality** - Content uniqueness assessment

---

## 🔧 Technology Stack

### Backend

- **Framework**: FastAPI
- **AI Framework**: Agno
- **Language Model**: OpenAI GPT-4o-mini
- **Vector Database**: PostgreSQL with pgvector
- **PDF Processing**: PyPDF with sentence-transformers

### Frontend

- **Framework**: React 19.1.0
- **Styling**: Modern CSS with responsive design
- **Markdown Rendering**: react-markdown

### Infrastructure

- **Containerization**: Docker & Docker Compose
- **Database**: PostgreSQL with vector extensions

---

## 📖 API Usage

### Core Endpoints

- `POST /evaluate` - Compare AI model responses
- `GET /knowledge-status` - Check knowledge base status
- `POST /load-knowledge` - Load/reload knowledge base
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation

### Example API Request

```json
{
  "prompt": "Explain distributed training in machine learning",
  "model1": "Model 1 response text...",
  "model2": "Model 2 response text...",
  "model3": "Model 3 response text...",
  "use_knowledge": true
}
```

### Example Response

```json
{
  "status": "success",
  "analysis": "## Model 1 Analysis\n\n**Strengths:**\n- Clear explanation...\n\n**Areas for Improvement:**\n- Could provide more examples...",
  "metadata": {
    "prompt_length": 45,
    "knowledge_used": true
  }
}
```
