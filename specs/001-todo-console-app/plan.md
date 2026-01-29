# Implementation Plan: Todo In-Memory Python Console App

**Feature**: 001-todo-console-app
**Created**: 2025-12-30
**Status**: Draft
**Plan Version**: 1.0.0

## Technical Context

**Architecture Overview**:
- Modular, single-user console application built in Python 3.13+
- Strictly in-memory storage (no files or databases)
- REPL-style interactive loop with a persistent main menu
- Clear separation of concerns: data model, business logic/service layer, and CLI presentation layer
- No external dependencies — Python standard library only
- Designed with modularity and clean interfaces to facilitate future phases (e.g., swapping storage layer for database in Phase II)

**Technology Stack**:
- Python 3.13+
- UV for project management
- Python standard library only (no external dependencies)
- Console-based UI (no GUI or web interface)

**Project Structure**:
- `src/models.py` - Data model layer (Task dataclass)
- `src/storage.py` - Storage/Service layer (TaskManager class)
- `src/cli.py` - CLI presentation layer
- `src/main.py` - Main application entry point

**Component Breakdown**:
1. Data Model (src/models.py) - Task dataclass with id, title, description, completed, created_at
2. Storage/Service Layer (src/storage.py) - TaskManager class with CRUD operations
3. CLI Presentation Layer (src/cli.py) - Menu display, task formatting, user prompts
4. Main Application (src/main.py) - Entry point and execution flow control

## Constitution Check

**Principle Compliance**:
- ✅ Spec-Driven Development (SDD) Foundation: Following validated spec, plan, and tasks
- ✅ AI-Native Workflow: Using Claude Code exclusively for implementation
- ✅ Simplicity and MVP Focus: Focusing only on 5 Basic Level features
- ✅ Reusability and Modularity: Designing with clean interfaces for future expansion
- ✅ Transparency and Traceability: All decisions link back to specs
- ✅ Clear and User-Friendly CLI: Providing clear CLI interface with user-friendly feedback

**Constraints Compliance**:
- ✅ Technology Stack: Python 3.13+, UV for project management
- ✅ No Persistence: Strictly in-memory storage
- ✅ Feature Scope: Limited to console CLI (no GUI, web, advanced features)
- ✅ Code Quality: Following PEP 8, using type hints, docstrings

## Phase 0: Research & Analysis

### Research Findings

**Decision**: Use dataclass for Task model
**Rationale**: Dataclasses provide clean, readable code with automatic generation of special methods like __init__, __repr__, etc. They're part of the standard library and appropriate for this use case.
**Alternatives considered**: Regular class, named tuple, attrs library (but avoiding external dependencies)

**Decision**: Use datetime for timestamp handling
**Rationale**: Python's standard library datetime module provides all necessary functionality for timestamp creation and formatting
**Alternatives considered**: time module, third-party libraries (but avoiding external dependencies)

**Decision**: Use simple integer ID system with auto-increment
**Rationale**: Simple, efficient, and appropriate for in-memory storage. Easy to implement and understand.
**Alternatives considered**: UUIDs (more complex than needed for this application)

## Phase 1: Design & Contracts

### Data Model (data-model.md)

#### Task Entity
- **id**: int (auto-incremented, unique identifier)
- **title**: str (required, non-empty after stripping whitespace)
- **description**: str (optional, default empty string)
- **completed**: bool (default False)
- **created_at**: datetime (UTC timestamp when task is created)

#### Validation Rules
- Title must be non-empty after stripping whitespace
- ID must be unique within the task collection
- ID must be positive integer

#### State Transitions
- completed: False → True (when marking complete)
- completed: True → False (when marking incomplete)

### API Contracts

#### TaskManager Class Interface

```python
class TaskManager:
    def __init__(self):
        """Initialize with empty task list and ID counter"""

    def add_task(self, title: str, description: str = "") -> Task:
        """Add new task to collection, return created Task object"""

    def list_tasks(self) -> list[Task]:
        """Return all tasks in collection, sorted by creation order"""

    def get_task(self, task_id: int) -> Task:
        """Return specific task by ID, raises ValueError if not found"""

    def update_task(self, task_id: int, title: str | None = None, description: str | None = None) -> Task:
        """Update specific task fields, return updated Task object"""

    def toggle_complete(self, task_id: int) -> Task:
        """Toggle completion status of task, return updated Task object"""

    def delete_task(self, task_id: int) -> None:
        """Remove task from collection, raises ValueError if not found"""
```

#### CLI Interface Functions

```python
def display_menu():
    """Display the main menu options to the user"""

def display_tasks(tasks: list[Task]):
    """Format and display tasks in a table with status indicators"""

def prompt_add_task() -> tuple[str, str]:
    """Prompt user for task title and description, return as tuple"""

def prompt_task_id() -> int:
    """Prompt user for task ID, validate and return integer"""

def prompt_update_fields() -> tuple[str | None, str | None]:
    """Prompt user for new title/description, return as tuple (can be None)"""

def confirm_delete(task: Task) -> bool:
    """Prompt user for confirmation before deleting task"""
```

### Quickstart Guide

1. Ensure Python 3.13+ and UV are installed
2. Clone the repository
3. Run the application with: `python -m src.main`
4. Follow the on-screen menu prompts to interact with the todo app

### Agent Context Updates

Added the following technology context for Claude Code:
- Python dataclasses for Task model
- datetime module for timestamp handling
- Standard library only (no external dependencies)
- Console-based user interface patterns
- In-memory storage patterns

## Phase 2: Implementation Strategy

### Component Development Order

1. **Task Data Model** (src/models.py)
   - Implement Task dataclass with required fields
   - Add validation for title field
   - Ensure proper string representation

2. **Task Manager Service** (src/storage.py)
   - Implement TaskManager class with in-memory storage
   - Create all required CRUD methods with proper error handling
   - Add input validation for all methods
   - Ensure thread safety if needed

3. **CLI Interface** (src/cli.py)
   - Create functions for menu display and user interaction
   - Implement task formatting for display
   - Add error handling and user-friendly messages
   - Create confirmation prompts where needed

4. **Main Application** (src/main.py)
   - Implement main execution loop
   - Integrate all components
   - Handle graceful exit

### Quality Gates

- All functions must have type hints
- All public functions must have docstrings
- Error handling must be consistent (ValueError for invalid inputs)
- Code must follow PEP 8 style guide
- No external dependencies beyond Python standard library