# ELAI Intent Engine API

RESTful API for Machine Learning (Random Forest) model inference. Developed with **FastAPI**, **Beanie** (asynchronous MongoDB ODM), and **Loguru**.

## 📖 Documentation

The project documentation is organized into focused guides:

1.  **[Implementation Decisions](docs/implementation_decisions.md)**: Architectural patterns, technical stack choices, project structure, and data integrity designs.
2.  **[Ubuntu Setup Guide](docs/ubuntu_setup_guide.md)**: System prerequisites, installation steps for `uv` and MongoDB, local execution, and Docker Compose management (if all the prerequisites are met use directly the Makefile)

---

## 🛠 Usage with Makefile

The repository includes a `Makefile` to simplify common development and deployment tasks.

### 0. Setup
Initialise the environment, sync dependencies (including test groups), and install the package in editable mode:
```bash
make setup
```

### 1. Local Development
Start the MongoDB container and run the FastAPI application with `uvicorn` and reload enabled:
```bash
make start
```

Stop the application and the MongoDB container:
```bash
make stop
```

### 2. Docker Deployment
Deploy the entire stack (API + MongoDB) in the background:
```bash
make deploy
```

Run the stack in the foreground to see logs:
```bash
make run-docker
```

Cleanup Docker containers and volumes:
```bash
make stop-docker
```

---

## 🧪 Testing

### Automated Tests (Pytest)
Ensure you have run `make setup` first. Then run the full test suite (17 tests):
```bash
uv run pytest -v
```

### Manual Testing (Bruno)
You can find API request collections in the `bruno/` directory. Use [Bruno](https://www.usebruno.com/) to import the collection and test the endpoints:
-   **Predict - Single**: Single record prediction (`POST /predict`).
-   **Predict - Batch**: Multi-record batch prediction (`POST /predict`).

Default local API endpoint: `http://localhost:5000`
