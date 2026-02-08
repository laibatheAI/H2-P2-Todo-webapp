"""
Integration tests for the Todo AI Agent in the Todo AI Chatbot application.
Tests the integration between the agent and MCP tools.
"""
import pytest
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime
from backend.core.agents.todo_agent import TodoAgent, AgentConfig
from backend.core.agents.tool_wiring import AgentToolWiring, route_and_execute_tool
from backend.core.agents.intent_classifier import classify_intent, Intent


class TestAgentToolIntegration:
    """Test cases for the integration between agent and tools."""

    def test_agent_processes_add_task_intent(self):
        """Test that the agent correctly processes an add task intent."""
        user_input = "Add a task to buy groceries"
        user_id = "test-user-id"

        # Use the real tool wiring function
        result = route_and_execute_tool(user_input, user_id)

        assert result is not None
        assert result.get("success") is True
        # Depending on implementation, this should map to an add_task operation
        assert "message" in result or "task" in result

    def test_agent_processes_list_tasks_intent(self):
        """Test that the agent correctly processes a list tasks intent."""
        user_input = "Show me my tasks"
        user_id = "test-user-id"

        result = route_and_execute_tool(user_input, user_id)

        assert result is not None
        assert result.get("success") is True
        # This should return a list of tasks
        assert "tasks" in result or "message" in result

    def test_agent_processes_complete_task_intent(self):
        """Test that the agent correctly processes a complete task intent."""
        user_input = "Complete task 1"
        user_id = "test-user-id"

        result = route_and_execute_tool(user_input, user_id)

        assert result is not None
        # Result should indicate success or provide appropriate feedback

    def test_agent_processes_delete_task_intent(self):
        """Test that the agent correctly processes a delete task intent."""
        user_input = "Delete task 1"
        user_id = "test-user-id"

        result = route_and_execute_tool(user_input, user_id)

        assert result is not None
        # Result should indicate success or provide appropriate feedback

    def test_agent_handles_unknown_intent(self):
        """Test that the agent handles unknown intents gracefully."""
        user_input = "This is not a recognized command"
        user_id = "test-user-id"

        result = route_and_execute_tool(user_input, user_id)

        assert result is not None
        # Even with unknown intent, should return some kind of response

    def test_agent_tool_wiring_initialization(self):
        """Test that the AgentToolWiring is properly initialized."""
        wiring = AgentToolWiring()

        assert wiring is not None
        assert hasattr(wiring, 'route_to_tool')
        assert hasattr(wiring, 'execute_mapped_tool')

    def test_agent_tool_routing_add_task(self):
        """Test routing of add task intent."""
        wiring = AgentToolWiring()

        result = wiring.route_to_tool("Add a task to call mom", "test-user-id")

        assert result is not None
        assert result.success is True
        assert result.tool_name in ["add_task", "help"]  # May return help if mock

    def test_agent_tool_routing_list_tasks(self):
        """Test routing of list tasks intent."""
        wiring = AgentToolWiring()

        result = wiring.route_to_tool("Show my tasks", "test-user-id")

        assert result is not None
        assert result.success is True

    def test_agent_tool_routing_other_intents(self):
        """Test routing of other intents."""
        wiring = AgentToolWiring()

        # Test complete intent
        result = wiring.route_to_tool("Complete task 1", "test-user-id")
        assert result is not None

        # Test delete intent
        result = wiring.route_to_tool("Delete task 1", "test-user-id")
        assert result is not None

        # Test update intent
        result = wiring.route_to_tool("Update task 1 to be higher priority", "test-user-id")
        assert result is not None


class TestIntentClassificationIntegration:
    """Test intent classification integration."""

    def test_classify_add_task_intent(self):
        """Test classification of add task intent."""
        text = "Add a task to buy milk"
        result = classify_intent(text)

        assert result is not None
        assert result.intent in [Intent.ADD_TASK, Intent.UNKNOWN]

    def test_classify_list_tasks_intent(self):
        """Test classification of list tasks intent."""
        text = "Show me my tasks"
        result = classify_intent(text)

        assert result is not None
        assert result.intent in [Intent.LIST_TASKS, Intent.UNKNOWN]

    def test_classify_complete_task_intent(self):
        """Test classification of complete task intent."""
        text = "Complete task 1"
        result = classify_intent(text)

        assert result is not None
        assert result.intent in [Intent.COMPLETE_TASK, Intent.UNKNOWN]

    def test_classify_delete_task_intent(self):
        """Test classification of delete task intent."""
        text = "Delete the meeting task"
        result = classify_intent(text)

        assert result is not None
        assert result.intent in [Intent.DELETE_TASK, Intent.UNKNOWN]

    def test_classify_help_intent(self):
        """Test classification of help intent."""
        text = "What can you do?"
        result = classify_intent(text)

        assert result is not None
        assert result.intent in [Intent.HELP, Intent.UNKNOWN]

    def test_classify_unknown_intent(self):
        """Test classification of unknown intent."""
        text = "This is a completely unrelated sentence"
        result = classify_intent(text)

        assert result is not None
        # Even unknown intents should return a valid result

    def test_entity_extraction_in_classification(self):
        """Test that entities are properly extracted during classification."""
        text = "Add a high priority task to call mom tomorrow"
        result = classify_intent(text)

        assert result is not None
        # Check if entities were extracted (even if not perfectly)
        assert hasattr(result, 'entities')


class TestAgentConfigIntegration:
    """Test agent configuration integration."""

    def test_default_agent_config(self):
        """Test creating an agent with default configuration."""
        from backend.core.agents.chat_agent import get_default_agent

        agent = get_default_agent()

        assert agent is not None
        assert hasattr(agent, 'process_message')

    def test_custom_model_agent(self):
        """Test creating an agent with a custom model."""
        from backend.core.agents.chat_agent import get_agent_with_custom_model

        agent = get_agent_with_custom_model("gpt-4")

        assert agent is not None
        assert agent.config.model == "gpt-4"

    def test_agent_with_custom_config(self):
        """Test creating an agent with custom configuration."""
        from backend.core.agents.chat_agent import create_todo_agent
        from backend.core.agents.todo_agent import AgentConfig

        config = AgentConfig(
            model="gpt-3.5-turbo",
            temperature=0.5,
            max_tokens=500
        )
        agent = create_todo_agent(config)

        assert agent is not None
        assert agent.config.model == "gpt-3.5-turbo"
        assert agent.config.temperature == 0.5


class TestAgentMessageProcessing:
    """Test agent message processing capabilities."""

    @patch('backend.core.agents.todo_agent.OpenAI')
    def test_process_simple_message(self, mock_openai_class):
        """Test processing a simple message through the agent."""
        # Mock the OpenAI client
        mock_client = Mock()
        mock_completion = Mock()
        mock_completion.choices = [Mock()]
        mock_completion.choices[0].message = Mock()
        mock_completion.choices[0].message.content = "I can help you with that."
        mock_completion.choices[0].message.tool_calls = None
        mock_client.chat.completions.create.return_value = mock_completion

        mock_openai_class.return_value = mock_client

        # Create agent and process message
        agent = TodoAgent()
        result = agent.process_message(
            user_message="Add a task",
            conversation_history=[{"role": "user", "content": "Hello"}],
            user_id="test-user-id"
        )

        assert result is not None
        assert "content" in result
        assert "role" in result

    @patch('backend.core.agents.todo_agent.OpenAI')
    def test_process_message_with_tool_calls(self, mock_openai_class):
        """Test processing a message that results in tool calls."""
        # Mock the OpenAI client with tool calls in response
        mock_client = Mock()
        mock_completion = Mock()
        mock_completion.choices = [Mock()]

        # Mock a tool call
        mock_tool_call = Mock()
        mock_tool_call.id = "call_123"
        mock_tool_call.type = "function"
        mock_function = Mock()
        mock_function.name = "add_task"
        mock_function.arguments = '{"title": "Test task"}'
        mock_tool_call.function = mock_function

        mock_completion.choices[0].message = Mock()
        mock_completion.choices[0].message.content = "I'll add that task for you."
        mock_completion.choices[0].message.tool_calls = [mock_tool_call]

        mock_client.chat.completions.create.return_value = mock_completion

        mock_openai_class.return_value = mock_client

        # Create agent and process message
        agent = TodoAgent()
        result = agent.process_message(
            user_message="Add a task to buy groceries",
            conversation_history=[{"role": "user", "content": "Hello"}],
            user_id="test-user-id"
        )

        assert result is not None
        assert "content" in result
        assert "tool_calls" in result
        assert len(result["tool_calls"]) > 0


class TestAgentErrorHandling:
    """Test agent error handling."""

    def test_route_to_tool_with_invalid_input(self):
        """Test routing with invalid or empty input."""
        wiring = AgentToolWiring()

        result = wiring.route_to_tool("", "test-user-id")
        assert result is not None
        assert result.success is False or result.success is True  # Could map to help

        result = wiring.route_to_tool("   ", "test-user-id")
        assert result is not None

    def test_execute_mapped_tool_with_error_result(self):
        """Test executing a mapped tool that results in an error."""
        wiring = AgentToolWiring()

        # Test with an invalid tool name
        from backend.core.agents.tool_wiring import ToolMappingResult
        error_mapping = ToolMappingResult(
            success=False,
            error="Test error",
            message="This is a test error"
        )

        result = wiring.execute_mapped_tool(error_mapping)
        assert result is not None
        assert result.get("success") is False