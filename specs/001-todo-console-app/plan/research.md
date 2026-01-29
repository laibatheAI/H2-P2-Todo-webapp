# Research Summary: Todo In-Memory Python Console App

## Decision: Use dataclass for Task model
**Rationale**: Dataclasses provide clean, readable code with automatic generation of special methods like __init__, __repr__, etc. They're part of the standard library and appropriate for this use case. The @dataclass decorator automatically adds methods like __init__, __repr__, and __eq__ based on the class annotations, reducing boilerplate code while maintaining clarity.

**Alternatives considered**:
- Regular class: Would require manual implementation of __init__ and other special methods
- Named tuple: Immutable but less flexible and doesn't support default values as cleanly
- attrs library: More feature-rich but would require external dependency (against project constraints)

## Decision: Use datetime for timestamp handling
**Rationale**: Python's standard library datetime module provides all necessary functionality for timestamp creation and formatting. The datetime.now() method with timezone.utc can provide UTC timestamps, and strftime() can format them as required (YYYY-MM-DD HH:MM format).

**Alternatives considered**:
- time module: More basic, less formatting options
- Third-party libraries like arrow: Would require external dependencies (against project constraints)

## Decision: Use simple integer ID system with auto-increment
**Rationale**: Simple, efficient, and appropriate for in-memory storage. Easy to implement and understand. An internal counter can be maintained in the TaskManager class that increments with each new task creation.

**Alternatives considered**:
- UUIDs: More complex than needed for this application, and would require additional imports (though still standard library)
- Random integers: Could result in collisions and doesn't provide sequential order

## Decision: Use tabulate-style manual formatting for task display
**Rationale**: Since external libraries are not allowed, manual formatting using string formatting and padding will be used. This maintains compliance with constraints while providing readable output.

**Alternatives considered**:
- tabulate library: Would require external dependency (against project constraints)
- PrettyTable: Would require external dependency (against project constraints)

## Decision: Implement REPL-style loop for main application
**Rationale**: A Read-Evaluate-Print Loop (REPL) pattern is ideal for console applications. It maintains a persistent menu that continues running until the user explicitly chooses to exit, providing a good user experience for this type of application.

**Alternatives considered**:
- Single-run approach: Would require re-running the program for each operation
- Submenu approach: More complex than needed for this simple application

## Decision: Use try-catch patterns for input validation
**Rationale**: Python's exception handling system works well for validating user input. Converting user input to integers with int() will raise ValueError if the input is not a valid number, which can be caught and handled gracefully.

**Alternatives considered**:
- Pre-validation with string methods: More complex for numeric validation
- Regular expressions: Overkill for simple input validation

## Decision: Store tasks in-memory using a list
**Rationale**: Since this is an in-memory application, a simple list will serve as the storage medium. A list of Task objects allows for easy iteration, searching, and modification operations. The TaskManager class can maintain this list as a private attribute.

**Alternatives considered**:
- Dictionary with ID as key: Would provide faster lookups but requires more complex management for auto-incrementing IDs
- Sets: Don't maintain order and don't support indexing