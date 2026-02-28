# Ubuntu Setup Guide

This guide provides step-by-step instructions to install and run the AI Predictive API on Ubuntu 22.04 LTS or newer.

## 1. System Prerequisites

Update your package list and install basic utilities:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git curl build-essential
```

## 2. Install Python 3.11

Ensure Python 3.11 and the virtual environment module are installed:

```bash
sudo apt install -y python3.11 python3.11-venv python3-pip
```

## 3. Install uv

The project uses `uv` for lightning-fast dependency management. Install it via the official script:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env
```

## 4. Install MongoDB

### Choice A: Docker (Recommended)
Install Docker and Docker Compose to run MongoDB in a container:

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add your user to the docker group
sudo usermod -aG docker $USER
# (Log out and log back in for changes to take effect)
```

### Choice B: Native Installation
Install MongoDB Community Edition directly on the host:

```bash
curl -fsSL https://www.mongodb.org/static/pgp/server-6.0.asc | \
   sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/mongodb-6.0.gpg

echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu $(lsb_release -cs)/mongodb-org/6.0 multiverse" | \
   sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

sudo apt update
sudo apt install -y mongodb-org

# Start the service
sudo systemctl start mongod
sudo systemctl enable mongod
```

## 5. Project Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd elai
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit the .env file as needed
   ```

### Key Configuration Variables

| Variable | Default Value | Description |
| --- | --- | --- |
| `MONGODB_URI` | `mongodb://localhost:27017/` | Connection string for Motor / Beanie |
| `MONGODB_DB_NAME` | `predictions_db` | MongoDB database name |
| `MODEL_PATH` | `resources/models/model.pkl` | Path to the serialized sklearn model |
| `DECISION_THRESHOLD` | `0.10` | Threshold for binary classification |
| `MAX_BATCH_SIZE` | `1000` | Maximum items per batch request |
| `API_HOST` | `0.0.0.0` | Uvicorn bind host |
| `API_PORT` | `5000` | Uvicorn bind port |

3. **Install dependencies**:
   ```bash
   uv sync

   # Install the project in editable mode
   uv pip install -e .
   ```

## 6. Execution

### Local Mode (Host Execution)
Run the API directly using `uv`:

```bash
uv run uvicorn elai_intent_engine.main:app --host 0.0.0.0 --port 5000 --reload
```

### Containerized Mode (Production Setup)
Run the entire stack (API + MongoDB) via Docker Compose:

```bash
docker compose -f docker/docker-compose.yml up -d --build
```

Access the interactive API documentation at: `http://localhost:5000/docs`

---

## 7. API Usage Examples

### `POST /predict`

Accepts either a **single JSON object** or a **JSON array** (up to 1000 objects per request).

**Single request:**

```bash
curl -X POST http://localhost:5000/predict \
     -H "Content-Type: application/json" \
     -d '{"nome": "Mario", "eta": 30, "cliente_attivo": "SI"}'
```

**Batch request:**

```bash
curl -X POST http://localhost:5000/predict \
     -H "Content-Type: application/json" \
     -d '[
           {"nome": "A", "eta": 20, "cliente_attivo": "NO"},
           {"nome": "B", "eta": 50, "cliente_attivo": "SI"}
         ]'
```

---

## 8. Docker Compose Management

Docker Compose is the primary tool for deploying and managing this application's lifecycle. Below are the essential commands.

### Deploying and Starting

**Build and start the containers in background:**
```bash
docker compose -f docker/docker-compose.yml up -d --build
```

**Start existing containers:**
```bash
docker compose -f docker/docker-compose.yml start
```

### Stopping and Removing

**Stop the containers (preserves state):**
```bash
docker compose -f docker/docker-compose.yml stop
```

**Tear down the environment (Deletes containers):**
```bash
docker compose -f docker/docker-compose.yml down
```

**Tear down AND delete database volumes:**
```bash
docker compose -f docker/docker-compose.yml down -v
```

### Monitoring

**View live logs:**
```bash
docker compose -f docker/docker-compose.yml logs -f
```

---

## 9. Development and QA

### Running Tests

```bash
# Run all tests
uv run pytest tests/ -v

# Run isolated unit tests
uv run pytest tests/test_ml.py -v
```

### Linting and Formatting

```bash
# Analyze code
uv run ruff check src/ tests/

# Automatically resolve errors
uv run ruff check --fix src/ tests/

# Format the codebase
uv run ruff format src/ tests/
```
