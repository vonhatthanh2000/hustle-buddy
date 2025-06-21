# 🚀 HustleBuddy - Simple Docker Setup

## Quick Start (For Your Friend! 😊)

Getting HustleBuddy running is super easy with Docker. Just follow these 3 steps:

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed on your machine
- [Docker Compose](https://docs.docker.com/compose/install/) (usually comes with Docker Desktop)
- An OpenAI API key ([get one here](https://platform.openai.com/api-keys))

### Step 1: Clone and Setup

```bash
git clone <your-repo-url>
cd hustle-buddy
```

### Step 2: Configure Your API Key

```bash
# Copy the environment template
cp .env.template .env

# Edit the .env file and add your OpenAI API key
# Replace 'your_openai_api_key_here' with your actual API key
```

### Step 3: Run Everything!

```bash
# Option A: Use the automated script (recommended)
./docker-run.sh

# Option B: Manual Docker Compose
docker-compose up --build
```

That's it! 🎉

### What Gets Started:

- **Frontend**: http://localhost:3000 (the web interface)
- **Backend**: http://localhost:8000 (the API)
- **Database**: PostgreSQL automatically initialized
- **API Docs**: http://localhost:8000/docs (interactive API documentation)

### Using the Application:

1. Open your browser to http://localhost:3000
2. Enter a prompt and three AI model responses
3. Click "Evaluate Models" to get the comparison analysis
4. View the detailed markdown-formatted results

### Useful Commands:

```bash
# View live logs
docker-compose logs -f

# Stop everything
docker-compose down

# Restart a specific service
docker-compose restart backend

# Rebuild and restart everything (if you make changes)
docker-compose up --build

# Check service status
docker-compose ps
```

### Troubleshooting:

- **Port conflicts**: If ports 3000 or 8000 are in use, edit `docker-compose.yml` to change the port mappings
- **OpenAI API errors**: Make sure your API key is correct in the `.env` file
- **Container issues**: Try `docker-compose down` then `docker-compose up --build`

### What's Running:

- **hustle-buddy-frontend**: React web app (nginx)
- **hustle-buddy-backend**: FastAPI Python service
- **hustle-buddy-db**: PostgreSQL with pgvector extension

The entire stack is automatically configured to work together - no manual setup needed! 🚀

---

Need help? Check out the main README.md for more detailed information about the project.
