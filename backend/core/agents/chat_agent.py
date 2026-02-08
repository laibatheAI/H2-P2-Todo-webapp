"""
Agent initialization logic for the Todo AI Chatbot application.
"""
from typing import Optional
from backend.core.agents.todo_agent import TodoAgent, AgentConfig


def create_todo_agent(config: Optional[AgentConfig] = None) -> TodoAgent:
    """
    Create and initialize a TodoAgent instance with the specified configuration.

    Args:
        config: Optional agent configuration. If None, uses default configuration.

    Returns:
        Initialized TodoAgent instance
    """
    if config is None:
        config = AgentConfig()

    agent = TodoAgent(config=config)
    return agent


def get_default_agent() -> TodoAgent:
    """
    Get a TodoAgent instance with default configuration.

    Returns:
        TodoAgent instance with default settings
    """
    return create_todo_agent()


def get_agent_with_custom_model(model_name: str) -> TodoAgent:
    """
    Get a TodoAgent instance with a custom model.

    Args:
        model_name: Name of the model to use (e.g., 'gpt-4', 'gpt-3.5-turbo')

    Returns:
        TodoAgent instance configured with the specified model
    """
    config = AgentConfig(model=model_name)
    return create_todo_agent(config)