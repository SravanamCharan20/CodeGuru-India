# CodeGuru India Tests

This directory contains tests for the Intent-Driven Repository Analysis System.

## Test Structure

```
tests/
├── integration/          # Integration tests
│   ├── test_end_to_end_flow.py      # Complete workflow tests
│   ├── test_ai_integration.py        # AI service integration tests
│   └── test_session_persistence.py   # Session management tests
└── README.md
```

## Running Tests

### Run all tests
```bash
pytest
```

### Run specific test file
```bash
pytest tests/integration/test_end_to_end_flow.py
```

### Run with verbose output
```bash
pytest -v
```

### Run specific test
```bash
pytest tests/integration/test_end_to_end_flow.py::TestEndToEndFlow::test_complete_workflow_english
```

### Run tests by marker
```bash
pytest -m integration
pytest -m ai
```

## Test Categories

### Integration Tests
- **test_end_to_end_flow.py**: Tests complete workflow from upload to artifact generation
- **test_ai_integration.py**: Tests LangChain orchestrator and AI service integration
- **test_session_persistence.py**: Tests session state management and persistence

## Requirements

Install test dependencies:
```bash
pip install pytest pytest-cov
```

## Notes

- Integration tests use mocked AI services to avoid external dependencies
- Tests create temporary directories for sample repositories
- Session tests verify state persistence across workflow steps
- Multi-language tests verify English, Hindi, and Telugu support
