"""
Skill implementations for the Todo AI Chatbot application.
"""
from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
from enum import Enum
from pydantic import BaseModel


class SkillResult(BaseModel):
    """Result from a skill execution."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
    error: Optional[str] = None


class Skill(ABC):
    """Abstract base class for all skills."""

    @abstractmethod
    def execute(self, params: Dict[str, Any]) -> SkillResult:
        """Execute the skill with the given parameters."""
        pass


class TaskManagementSkill(Skill):
    """
    Skill for managing user tasks through MCP tools.
    Maps to the MCP tool implementations for CRUD operations.
    """

    def execute(self, params: Dict[str, Any]) -> SkillResult:
        """
        Execute task management operations.

        Args:
            params: Contains 'operation' (add, list, update, complete, delete)
                   and relevant task parameters

        Returns:
            SkillResult with operation outcome
        """
        operation = params.get('operation')

        try:
            if operation == 'add':
                return self._add_task(params)
            elif operation == 'list':
                return self._list_tasks(params)
            elif operation == 'update':
                return self._update_task(params)
            elif operation == 'complete':
                return self._complete_task(params)
            elif operation == 'delete':
                return self._delete_task(params)
            else:
                return SkillResult(
                    success=False,
                    error=f"Unknown operation: {operation}. Supported operations: add, list, update, complete, delete"
                )
        except Exception as e:
            return SkillResult(
                success=False,
                error=f"Error executing task operation {operation}: {str(e)}"
            )

    def _add_task(self, params: Dict[str, Any]) -> SkillResult:
        """Add a new task."""
        # In a real implementation, this would call the MCP add_task tool
        # For now, we'll simulate the operation
        task_data = {
            "id": params.get('task_id', 'mock-task-id'),
            "title": params.get('title'),
            "description": params.get('description'),
            "due_date": params.get('due_date'),
            "priority": params.get('priority', 'medium'),
            "category": params.get('category'),
            "completed": False
        }

        return SkillResult(
            success=True,
            data=task_data,
            message=f"Task '{params.get('title', 'Untitled')}' added successfully"
        )

    def _list_tasks(self, params: Dict[str, Any]) -> SkillResult:
        """List tasks with optional filtering."""
        # In a real implementation, this would call the MCP list_tasks tool
        # For now, we'll simulate the operation
        filters = {
            'status': params.get('status', 'all'),
            'priority': params.get('priority'),
            'category': params.get('category'),
            'limit': params.get('limit', 50),
            'offset': params.get('offset', 0)
        }

        # Mock task list
        mock_tasks = [
            {
                "id": "mock-task-1",
                "title": "Sample task 1",
                "description": "This is a sample task",
                "due_date": "2026-02-10T10:00:00.000Z",
                "priority": "medium",
                "category": "work",
                "completed": False
            },
            {
                "id": "mock-task-2",
                "title": "Sample task 2",
                "description": "Another sample task",
                "due_date": "2026-02-15T14:00:00.000Z",
                "priority": "high",
                "category": "personal",
                "completed": True
            }
        ]

        # Apply filters
        status_filter = filters['status']
        if status_filter == 'completed':
            mock_tasks = [t for t in mock_tasks if t['completed']]
        elif status_filter == 'pending':
            mock_tasks = [t for t in mock_tasks if not t['completed']]

        priority_filter = filters['priority']
        if priority_filter:
            mock_tasks = [t for t in mock_tasks if t['priority'] == priority_filter]

        category_filter = filters['category']
        if category_filter:
            mock_tasks = [t for t in mock_tasks if t['category'] == category_filter]

        limit = filters['limit']
        mock_tasks = mock_tasks[:limit]

        return SkillResult(
            success=True,
            data={
                "total_count": len(mock_tasks),
                "returned_count": len(mock_tasks),
                "tasks": mock_tasks,
                "filters_applied": filters
            }
        )

    def _update_task(self, params: Dict[str, Any]) -> SkillResult:
        """Update an existing task."""
        # In a real implementation, this would call the MCP update_task tool
        # For now, we'll simulate the operation
        task_id = params.get('task_id')
        if not task_id:
            return SkillResult(success=False, error="task_id is required for update operation")

        updated_fields = {k: v for k, v in params.items()
                         if k in ['title', 'description', 'due_date', 'priority', 'category', 'completed']}

        return SkillResult(
            success=True,
            data={
                "task_id": task_id,
                "updated_fields": updated_fields
            },
            message=f"Task {task_id} updated successfully"
        )

    def _complete_task(self, params: Dict[str, Any]) -> SkillResult:
        """Mark a task as completed."""
        # In a real implementation, this would call the MCP complete_task tool
        # For now, we'll simulate the operation
        task_id = params.get('task_id')
        if not task_id:
            return SkillResult(success=False, error="task_id is required for complete operation")

        return SkillResult(
            success=True,
            data={
                "task_id": task_id,
                "completed": True,
                "completed_at": "2026-02-05T12:00:00.000Z"
            },
            message=f"Task {task_id} marked as completed"
        )

    def _delete_task(self, params: Dict[str, Any]) -> SkillResult:
        """Delete a task."""
        # In a real implementation, this would call the MCP delete_task tool
        # For now, we'll simulate the operation
        task_id = params.get('task_id')
        if not task_id:
            return SkillResult(success=False, error="task_id is required for delete operation")

        return SkillResult(
            success=True,
            data={
                "task_id": task_id
            },
            message=f"Task {task_id} deleted successfully"
        )


class IntentClassificationSkill(Skill):
    """
    Skill for classifying user intent from natural language input.
    Maps user language to specific actions based on keywords and context.
    """

    # Define intent categories with keywords
    INTENT_KEYWORDS = {
        'add_task': [
            'add', 'create', 'new', 'make', 'add a task', 'create a task',
            'i want to add', 'please add', 'remind me to', 'i need to'
        ],
        'list_tasks': [
            'show', 'list', 'view', 'see', 'display', 'what', 'give me',
            'show me', 'list my', 'view my', 'see my', 'what are my'
        ],
        'complete_task': [
            'complete', 'done', 'finish', 'mark as done', 'finish up',
            'i finished', 'i completed', 'mark complete', 'check off'
        ],
        'delete_task': [
            'delete', 'remove', 'cancel', 'get rid of', 'eliminate',
            'remove this', 'delete this', 'get rid of this'
        ],
        'update_task': [
            'update', 'change', 'modify', 'edit', 'rename', 'alter',
            'change to', 'update to', 'modify to'
        ],
        'help': [
            'help', 'what can you do', 'how', 'instructions', 'guide'
        ]
    }

    def execute(self, params: Dict[str, Any]) -> SkillResult:
        """
        Classify the intent of the user's message.

        Args:
            params: Contains 'message' (the user's input message)

        Returns:
            SkillResult with identified intent and extracted entities
        """
        message = params.get('message', '').lower().strip()

        if not message:
            return SkillResult(
                success=False,
                error="Message is required for intent classification"
            )

        # Classify intent based on keywords
        intent = self._classify_intent(message)

        # Extract relevant entities
        entities = self._extract_entities(message, intent)

        return SkillResult(
            success=True,
            data={
                "intent": intent,
                "confidence": 0.9,  # High confidence for keyword matching
                "entities": entities,
                "original_message": params.get('message')
            }
        )

    def _classify_intent(self, message: str) -> str:
        """Classify the intent of the message based on keywords."""
        for intent, keywords in self.INTENT_KEYWORDS.items():
            for keyword in keywords:
                if keyword in message:
                    return intent

        # Default to help if no intent matched
        return 'help'

    def _extract_entities(self, message: str, intent: str) -> Dict[str, Any]:
        """Extract entities like task titles, dates, priorities, etc. from the message."""
        entities = {}

        # Extract potential task title (everything after intent-indicating words)
        if intent == 'add_task':
            # Look for common patterns in add_task requests
            for keyword in self.INTENT_KEYWORDS['add_task']:
                if keyword in message:
                    # Extract what comes after the keyword
                    parts = message.split(keyword, 1)
                    if len(parts) > 1:
                        task_desc = parts[1].strip()
                        if task_desc:
                            entities['title'] = task_desc
                        break

        elif intent == 'update_task':
            # Look for common patterns in update_task requests
            for keyword in self.INTENT_KEYWORDS['update_task']:
                if keyword in message:
                    parts = message.split(keyword, 1)
                    if len(parts) > 1:
                        desc = parts[1].strip()
                        entities['update_details'] = desc
                        break

        # Extract potential dates
        import re
        date_patterns = [
            r'\b\d{4}-\d{2}-\d{2}\b',  # YYYY-MM-DD
            r'\b\d{1,2}/\d{1,2}/\d{4}\b',  # MM/DD/YYYY or DD/MM/YYYY
            r'\b\d{1,2}-\d{1,2}-\d{4}\b',  # MM-DD-YYYY or DD-MM-YYYY
            r'\btoday\b', r'\btomorrow\b', r'\bnext week\b', r'\bthis weekend\b'
        ]

        for pattern in date_patterns:
            matches = re.findall(pattern, message)
            if matches:
                entities['potential_dates'] = matches
                break

        # Extract potential priorities
        priority_words = ['low', 'medium', 'high', 'urgent', 'important']
        for word in priority_words:
            if word in message:
                entities['potential_priority'] = word
                break

        # Extract potential categories
        category_words = ['work', 'personal', 'shopping', 'health', 'finance', 'home']
        for word in category_words:
            if word in message:
                entities['potential_category'] = word
                break

        return entities


class ConversationContextSkill(Skill):
    """
    Skill for managing conversation context and persistence.
    Handles loading/saving conversation history to/from database.
    """

    def execute(self, params: Dict[str, Any]) -> SkillResult:
        """
        Handle conversation context operations like loading history.

        Args:
            params: Contains 'operation' (load_history, save_message, etc.)
                   and relevant context parameters

        Returns:
            SkillResult with conversation context
        """
        operation = params.get('operation')

        try:
            if operation == 'load_history':
                return self._load_conversation_history(params)
            elif operation == 'save_message':
                return self._save_message(params)
            elif operation == 'create_conversation':
                return self._create_conversation(params)
            else:
                return SkillResult(
                    success=False,
                    error=f"Unknown operation: {operation}. Supported: load_history, save_message, create_conversation"
                )
        except Exception as e:
            return SkillResult(
                success=False,
                error=f"Error executing conversation context operation: {str(e)}"
            )

    def _load_conversation_history(self, params: Dict[str, Any]) -> SkillResult:
        """Load conversation history for a user."""
        user_id = params.get('user_id')
        limit = params.get('limit', 50)

        if not user_id:
            return SkillResult(success=False, error="user_id is required to load conversation history")

        # In a real implementation, this would query the database
        # For now, we'll simulate with mock data
        mock_history = [
            {
                "id": "msg-1",
                "role": "user",
                "content": "Can you add a task to buy groceries?",
                "timestamp": "2026-02-05T10:00:00.000Z"
            },
            {
                "id": "msg-2",
                "role": "assistant",
                "content": "Sure, I've added the task 'buy groceries'.",
                "timestamp": "2026-02-05T10:00:10.000Z"
            }
        ]

        return SkillResult(
            success=True,
            data={
                "user_id": user_id,
                "history": mock_history[-limit:],  # Return last 'limit' messages
                "total_messages": len(mock_history)
            }
        )

    def _save_message(self, params: Dict[str, Any]) -> SkillResult:
        """Save a message to the conversation history."""
        user_id = params.get('user_id')
        conversation_id = params.get('conversation_id')
        role = params.get('role')
        content = params.get('content')

        if not all([user_id, conversation_id, role, content]):
            return SkillResult(
                success=False,
                error="user_id, conversation_id, role, and content are required to save message"
            )

        # In a real implementation, this would save to the database
        # For now, we'll simulate the operation
        message_data = {
            "id": params.get('message_id', 'mock-msg-id'),
            "user_id": user_id,
            "conversation_id": conversation_id,
            "role": role,
            "content": content,
            "timestamp": "2026-02-05T12:00:00.000Z"
        }

        return SkillResult(
            success=True,
            data=message_data,
            message="Message saved successfully"
        )

    def _create_conversation(self, params: Dict[str, Any]) -> SkillResult:
        """Create a new conversation record."""
        user_id = params.get('user_id')

        if not user_id:
            return SkillResult(success=False, error="user_id is required to create conversation")

        # In a real implementation, this would create in the database
        # For now, we'll simulate the operation
        conversation_data = {
            "id": params.get('conversation_id', 'mock-conv-id'),
            "user_id": user_id,
            "title": params.get('title', f"Conversation with {user_id[:8]}"),
            "created_at": "2026-02-05T12:00:00.000Z"
        }

        return SkillResult(
            success=True,
            data=conversation_data,
            message="Conversation created successfully"
        )


class ConfirmationUXSkill(Skill):
    """
    Skill for handling human-friendly confirmations and UX interactions.
    Manages confirmations for destructive operations and user-friendly responses.
    """

    def execute(self, params: Dict[str, Any]) -> SkillResult:
        """
        Handle confirmation and UX operations.

        Args:
            params: Contains 'operation' (needs_confirmation, format_response, etc.)
                   and relevant parameters

        Returns:
            SkillResult with UX elements
        """
        operation = params.get('operation')

        try:
            if operation == 'needs_confirmation':
                return self._check_needs_confirmation(params)
            elif operation == 'format_response':
                return self._format_response(params)
            elif operation == 'generate_confirmation':
                return self._generate_confirmation(params)
            else:
                return SkillResult(
                    success=False,
                    error=f"Unknown operation: {operation}. Supported: needs_confirmation, format_response, generate_confirmation"
                )
        except Exception as e:
            return SkillResult(
                success=False,
                error=f"Error executing UX operation: {str(e)}"
            )

    def _check_needs_confirmation(self, params: Dict[str, Any]) -> SkillResult:
        """Check if an operation needs user confirmation."""
        action = params.get('action')
        item_type = params.get('item_type', 'item')
        item_id = params.get('item_id')

        # Determine if confirmation is needed based on action type
        needs_confirmation = action in ['delete', 'complete', 'permanent_remove']

        return SkillResult(
            success=True,
            data={
                "action": action,
                "item_type": item_type,
                "item_id": item_id,
                "needs_confirmation": needs_confirmation,
                "confirmation_reason": "Destructive operation" if needs_confirmation else "Routine operation"
            }
        )

    def _format_response(self, params: Dict[str, Any]) -> SkillResult:
        """Format a response in a user-friendly way."""
        data = params.get('data', {})
        action = params.get('action', 'perform')
        success = params.get('success', True)

        if success:
            if action == 'add':
                title = data.get('title', 'the task')
                message = f"✓ Successfully added {title}"
            elif action == 'list':
                count = data.get('returned_count', 0)
                message = f"📋 Here are your tasks ({count} total)"
            elif action == 'update':
                message = "✅ Task updated successfully"
            elif action == 'complete':
                message = "🎉 Task marked as completed!"
            elif action == 'delete':
                message = "🗑️ Task deleted successfully"
            else:
                message = data.get('message', 'Operation completed successfully')
        else:
            error_msg = data.get('error', 'An error occurred')
            message = f"❌ {error_msg}"

        return SkillResult(
            success=True,
            data={"formatted_message": message},
            message=message
        )

    def _generate_confirmation(self, params: Dict[str, Any]) -> SkillResult:
        """Generate a confirmation message for user approval."""
        action = params.get('action')
        item_description = params.get('item_description', 'this item')

        if action == 'delete':
            message = f"Are you sure you want to permanently delete {item_description}? This action cannot be undone."
        elif action == 'complete':
            message = f"Mark {item_description} as completed? You can still undo this later."
        elif action == 'update':
            message = f"Apply these changes to {item_description}? This will update the existing item."
        else:
            message = f"Confirm {action} action on {item_description}?"

        return SkillResult(
            success=True,
            data={
                "confirmation_message": message,
                "action": action,
                "item_description": item_description
            },
            message=message
        )


class ErrorHandlingSkill(Skill):
    """
    Skill for handling errors and providing recovery behavior.
    Manages task not found, invalid input, authentication issues, etc.
    """

    def execute(self, params: Dict[str, Any]) -> SkillResult:
        """
        Handle error conditions and recovery.

        Args:
            params: Contains 'error_type', 'context', and other error-related parameters

        Returns:
            SkillResult with error handling outcome
        """
        error_type = params.get('error_type')

        try:
            if error_type == 'task_not_found':
                return self._handle_task_not_found(params)
            elif error_type == 'invalid_input':
                return self._handle_invalid_input(params)
            elif error_type == 'auth_error':
                return self._handle_auth_error(params)
            elif error_type == 'system_error':
                return self._handle_system_error(params)
            else:
                return self._handle_generic_error(params)
        except Exception as e:
            return SkillResult(
                success=False,
                error=f"Error in error handling skill: {str(e)}"
            )

    def _handle_task_not_found(self, params: Dict[str, Any]) -> SkillResult:
        """Handle when a task is not found."""
        task_id = params.get('task_id')
        suggestion = params.get('suggestion', 'list your tasks to see what is available')

        message = f"I couldn't find a task with ID {task_id}. Would you like to {suggestion}?"

        return SkillResult(
            success=True,
            data={
                "error_type": "task_not_found",
                "task_id": task_id,
                "suggested_action": suggestion
            },
            message=message
        )

    def _handle_invalid_input(self, params: Dict[str, Any]) -> SkillResult:
        """Handle invalid input from the user."""
        input_value = params.get('input_value')
        expected_format = params.get('expected_format', 'the correct format')
        suggestion = params.get('suggestion', 'try rephrasing your request')

        message = f"I didn't understand '{input_value}'. Please provide {expected_format}. Could you {suggestion}?"

        return SkillResult(
            success=True,
            data={
                "error_type": "invalid_input",
                "input_value": input_value,
                "expected_format": expected_format,
                "suggested_action": suggestion
            },
            message=message
        )

    def _handle_auth_error(self, params: Dict[str, Any]) -> SkillResult:
        """Handle authentication errors."""
        error_detail = params.get('error_detail', 'authentication failed')

        message = f"Authentication issue: {error_detail}. Please log in again or check your credentials."

        return SkillResult(
            success=True,
            data={
                "error_type": "auth_error",
                "error_detail": error_detail
            },
            message=message
        )

    def _handle_system_error(self, params: Dict[str, Any]) -> SkillResult:
        """Handle system-level errors."""
        error_detail = params.get('error_detail', 'an unexpected error occurred')

        message = f"I'm sorry, but I encountered a technical issue: {error_detail}. Please try again in a moment."

        return SkillResult(
            success=True,
            data={
                "error_type": "system_error",
                "error_detail": error_detail
            },
            message=message
        )

    def _handle_generic_error(self, params: Dict[str, Any]) -> SkillResult:
        """Handle generic errors."""
        error_msg = params.get('error', 'an error occurred')
        context = params.get('context', 'the operation')

        message = f"An error occurred while processing {context}: {error_msg}. Please try again."

        return SkillResult(
            success=True,
            data={
                "error_type": "generic",
                "error_message": error_msg,
                "context": context
            },
            message=message
        )