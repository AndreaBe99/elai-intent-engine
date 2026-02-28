# Implementation Decisions

This document outlines the architectural patterns, design principles, and technical choices made for the AI Predictive API.

## 1. Technical Stack

- **FastAPI**: From requirements.
- **Beanie (MongoDB ODM)**: Chosen to leverage MongoDB's flexibility with Pydantic's powerful validation. It provides an asynchronous interface consistent with the rest of the stack.
- **Loguru**: Implemented for structured logging.
- **uv**: Utilized as the package and environment manager.

## 2. Architectural Design & SOLID Principles

The application follows a **Modular Layered Architecture** designed to respect **SOLID** principles and ensure long-term maintainability.

### Layered Responsibility (SRP)
Each component has a single, well-defined responsibility:
1.  **API Layer (`/api`)**: Manages HTTP entry points, request/response schemas, and uses **Dependency Injection** to access business services.
2.  **Service Layer (`/services/api`)**: The `PredictionService` acts as an **Orchestrator**, coordinating the flow between the ML engine and the persistence layer.
3.  **ML Service Layer (`/services`)**:
    *   `MLService`: Encapsulates model lifecycle (loading/inference). Implemented as a **Singleton** to optimize performance by loading the model only once.
    *   `FeatureEngineeringService`: Strictly dedicated to data transformation and preprocessing, isolating this logic from the inference process.
4.  **Repository Layer (`/repositories`)**: Encapsulates data persistence details using the **Repository Pattern**, providing a clean interface for the service layer and decoupling business logic from the specific database implementation (Beanie/MongoDB).

### Dependency Inversion (DI)
The application extensively uses **Dependency Injection**:
- `PredictionService` receives its dependencies (like `PredictionRepository`) via its constructor.
- FastAPI's `Depends` mechanism in `dependencies.py` handles the wiring, making the system highly testable via mocks.

## 3. Design Patterns Applied

- **Singleton Pattern**: Used in `MLService` to ensure the ML model is loaded into memory only once during application startup, preventing I/O overhead on requests.
- **Repository Pattern**: Abstrates the data access logic, allowing the service layer to interact with data without knowing the underlying storage technology.
- **Service Layer Pattern**: Orchestrates complex business processes and coordinates multiple services or repositories.
- **Dependency Injection**: Manages the instantiation and lifecycle of components, promoting loose coupling.

## 4. Project Structure

```text
src/elai_intent_engine/
├── api/
│   ├── routers/
│   │   └── prediction.py       # Endpoint definitions
│   └── dependencies.py         # DI wiring (get_service, get_repo)
├── models/
│   ├── api/                    # Pydantic request/reponse schemas
│   └── database/               # Beanie Document models
├── repositories/
│   └── prediction.py           # Persistence logic (PredictionRepository)
├── services/
│   ├── api/
│   │   └── prediction.py       # High-level orchestration (PredictionService)
│   ├── database.py             # Database initialization
│   ├── feature_engineering.py  # Data transformation (FeatureEngineeringService)
│   └── ml.py                   # Model lifecycle & inference (MLService)
├── utils/
│   ├── config.py               # Configuration management
│   ├── enums.py                # Enum definitions
│   └── logging.py              # Structured logging setup
└── main.py                     # Application entry point and lifespan
```

## 5. Data Integrity and Validation

- **Pydantic Schemas**: Strict validation is applied at the edge. Invalid data is rejected before reaching the service layer.
- **Feature Engineering Visibility**: Preprocessing steps are explicitly isolated in `FeatureEngineeringService`, ensuring clear visibility and logging of transformations defined in the training report.

## 6. Deployment and Quality Assurance

- **Multi-stage Docker Build**: Optimized images separating build-time dependencies from runtime requirements.
- **Testing Strategy**: Hybrid approach using unit tests for specialized services (ML/Feature Engineering) and functional tests for the API layer with database mocking.

## 7. Logging configuration

| Sink | Level | Format | Location | Rotation | Retention |
| --- | --- | --- | --- | --- | --- |
| Console | DEBUG | Human-readable | `stderr` | — | — |
| File | INFO | JSON (structured) | `logs/api.log` | 10 MB | 30 days |
