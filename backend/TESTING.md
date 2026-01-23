# Backend Testing Guide

## Prerequisites
Ensure validation of python dependencies:
```bash
pip install -r requirements.txt
```

## Running Tests

### 1. Database Integration Tests
Verifies that SQLAlchemy models work correctly with SQLite, tables are created, and data is persisted.
```bash
python3 -m unittest tests/test_database.py
```

### 2. API Integration Tests
Verifies the FastAPI endpoints using mocked services but real Pydantic validation and Request/Response flow.
```bash
python3 -m unittest tests/test_api_integration.py
```

### 3. Run All Tests
```bash
python3 -m unittest discover tests
```

## Test Coverage
- **Persistence:** `AnalysisJob` creation, retrieval, updates.
- **API:** `/analyze` (POST), `/jobs/{job_id}` (GET).
- **Services:** Emotion Detector, Visual Mapper, Parsers (via unit tests).
