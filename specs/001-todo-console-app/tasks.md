# Implementation Tasks: Todo In-Memory Python Console App

**Feature**: 001-todo-console-app
**Created**: 2025-12-30
**Status**: Draft
**Total Tasks**: 35

## Phase 1: Setup

### Goal
Initialize project structure and create basic files required for the application.

### Independent Test
Project structure is created with all necessary files and directories in place.

### Tasks
- [x] T001 Create project directory structure (src/, specs/, history/, etc.)
- [x] T002 [P] Create pyproject.toml with Python 3.13+ requirement and basic metadata
- [x] T003 [P] Create src/ directory and subdirectories if they don't exist
- [x] T004 [P] Create README.md with project overview and setup instructions
- [x] T005 [P] Create CLAUDE.md with Claude Code usage instructions

## Phase 2: Foundational Components

### Goal
Implement the core data model and storage layer that will be used by all user stories.

### Independent Test
Task data model and TaskManager class are implemented with all required functionality and can be instantiated.

### Tasks
- [x] T006 [P] [US1] Create Task dataclass in src/models.py with id, title, description, completed, created_at fields
- [x] T007 [P] [US1] Add validation to Task dataclass to ensure title is not empty after stripping whitespace
- [x] T008 [P] [US1] Implement TaskManager class in src/storage.py with private task list and ID counter
- [x] T009 [P] [US1] Implement add_task method in TaskManager with title validation and auto-ID assignment
- [x] T010 [P] [US1] Implement list_tasks method in TaskManager to return all tasks sorted by creation order
- [x] T011 [P] [US1] Implement get_task method in TaskManager with ValueError for invalid IDs
- [x] T012 [P] [US1] Implement update_task method in TaskManager with field validation
- [x] T013 [P] [US1] Implement toggle_complete method in TaskManager to flip completion status
- [x] T014 [P] [US1] Implement delete_task method in TaskManager with ValueError for invalid IDs
- [x] T015 [P] [US1] Add comprehensive docstrings to all TaskManager methods

## Phase 3: User Story 1 - Interactive Menu Navigation (Priority: P1)

### Goal
Implement the main menu system that allows users to navigate between different functions of the app.

### Independent Test
User can launch the app and see a clear menu with numbered options, and can select options that correspond to different functions.

### Tasks
- [x] T016 [US1] Create display_menu function in src/cli.py to print formatted menu options
- [x] T017 [US1] Implement main menu loop in src/main.py with menu display and option selection
- [x] T018 [US1] Add menu option handling for all 6 menu choices (1-6)
- [x] T019 [US1] Implement basic option execution without full functionality (print "not implemented" for now)
- [x] T020 [US1] Add graceful exit functionality when user selects option 6

## Phase 4: User Story 2 - Task Management Operations (Priority: P1)

### Goal
Implement all 5 core task management operations: add, view, update, mark complete, delete.

### Independent Test
Each operation can be tested individually - adding tasks, viewing tasks, updating tasks, marking completion, deleting tasks.

### Tasks
- [x] T021 [US2] Implement prompt_add_task function in src/cli.py to get title and description from user
- [x] T022 [US2] Connect add task menu option to TaskManager.add_task method
- [x] T023 [US2] Implement display_tasks function in src/cli.py to format and print task table
- [x] T024 [US2] Connect view tasks menu option to TaskManager.list_tasks method
- [x] T025 [US2] Implement prompt_task_id function in src/cli.py with input validation
- [x] T026 [US2] Implement prompt_update_fields function in src/cli.py for optional title/description updates
- [x] T027 [US2] Connect update task menu option to TaskManager.update_task method
- [x] T028 [US2] Connect toggle complete menu option to TaskManager.toggle_complete method
- [x] T029 [US2] Implement confirm_delete function in src/cli.py with confirmation prompt
- [x] T030 [US2] Connect delete task menu option to TaskManager.delete_task method with confirmation

## Phase 5: User Story 3 - Safe Application Exit (Priority: P2)

### Goal
Ensure the application terminates gracefully when the user chooses to exit.

### Independent Test
User can select the exit option and verify the application terminates without errors.

### Tasks
- [x] T031 [US3] Enhance exit functionality in main loop to ensure clean termination
- [x] T032 [US3] Add any necessary cleanup operations before exit

## Phase 6: Error Handling & Edge Cases

### Goal
Implement proper error handling for all edge cases and invalid inputs.

### Independent Test
The application handles invalid inputs gracefully without crashing and displays user-friendly error messages.

### Tasks
- [x] T033 [P] [US2] Add input validation to prevent crashes on non-integer IDs
- [x] T034 [P] [US2] Implement error messages for invalid task IDs in update/delete operations
- [x] T035 [P] [US2] Display friendly message when no tasks exist in view operation

## Phase 7: Polish & Cross-Cutting Concerns

### Goal
Final improvements including formatting, user experience enhancements, and code quality.

### Independent Test
Application has polished UI with consistent formatting, clear error messages, and good user experience.

### Tasks
- [x] T036 [P] Format task display with proper column alignment and status indicators [x]/[ ]
- [x] T037 [P] Ensure consistent date formatting as YYYY-MM-DD HH:MM
- [x] T038 [P] Add proper truncation for long descriptions in task display
- [x] T039 [P] Improve error message clarity throughout the application
- [x] T040 [P] Ensure all functions have proper type hints and docstrings
- [x] T041 [P] Add PEP 8 compliance check and fix any issues
- [x] T042 [P] Test complete workflow and fix any remaining issues

## Dependencies

- US1 (User Story 1) must be completed before US2 can be fully tested
- Foundational components (Phase 2) must be completed before any user stories
- All user stories depend on the foundational TaskManager implementation

## Parallel Execution Examples

- Tasks T002-T005 can be executed in parallel (setup tasks in different files)
- Tasks T006-T015 can be executed in parallel (foundational components in different files)
- Tasks T021, T023, T025, T026, T029 can be developed in parallel (CLI functions)
- Tasks T022, T024, T027, T028, T030 can be developed in parallel (connecting CLI to TaskManager)

## Implementation Strategy

1. **MVP Scope**: Complete Phase 1 (Setup) + Phase 2 (Foundational) + Phase 3 (User Story 1) to have a working menu system
2. **Incremental Delivery**: After MVP, add core functionality one user story at a time
3. **Testing**: Each phase should be independently testable before moving to the next
4. **Quality**: Final phase focuses on polish and edge cases to ensure robustness