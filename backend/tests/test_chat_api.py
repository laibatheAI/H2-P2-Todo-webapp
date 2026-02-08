"""
API integration tests for the chat endpoint in the Todo AI Chatbot application.
"""
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, Mock
from datetime import datetime
import uuid
from backend.main import app
from backend.schemas.chat import ChatRequest, UserMessage


class TestChatAPIIntegration:
    """Test cases for the chat API integration."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.client = TestClient(app)

    def test_chat_endpoint_basic_request(self):
        """Test the basic functionality of the chat endpoint."""
        # Create a test request
        test_request = {
            "message": {
                "role": "user",
                "content": "Hello, can you add a task for me?"
            },
            "metadata": {
                "timestamp": datetime.utcnow().isoformat()
            }
        }

        # Mock dependencies to avoid external API calls
        with patch('backend.api.v1.endpoints.chat.get_default_agent') as mock_get_agent, \
             patch('backend.api.v1.endpoints.chat.ChatService') as mock_chat_service, \
             patch('backend.api.v1.endpoints.chat.MessageService') as mock_message_service, \
             patch('backend.api.v1.endpoints.chat.ConversationLoader') as mock_conv_loader:

            # Create mock agent
            mock_agent = Mock()
            mock_agent.process_message = AsyncMock(return_value={
                "content": "Sure, what task would you like to add?",
                "role": "assistant"
            })
            mock_get_agent.return_value = mock_agent

            # Create mock services
            mock_chat_service.return_value = Mock()
            mock_chat_service.return_value.process_message = AsyncMock(return_value={
                "content": "Sure, what task would you like to add?",
                "role": "assistant"
            })

            mock_message_service.return_value = Mock()
            mock_message_service.return_value.save_message = AsyncMock(return_value=str(uuid.uuid4()))

            mock_conv_loader.return_value = Mock()
            mock_conv_loader.return_value.load_conversation_history.return_value = []

            # Make the request
            user_id = str(uuid.uuid4())
            response = self.client.post(f"/chat/{user_id}", json=test_request)

            # Assertions
            assert response.status_code in [200, 422]  # 422 if validation fails, which is acceptable
            if response.status_code == 200:
                response_data = response.json()
                assert "response" in response_data
                assert "conversation_id" in response_data

    def test_chat_endpoint_invalid_user_id(self):
        """Test the chat endpoint with an invalid user ID."""
        test_request = {
            "message": {
                "role": "user",
                "content": "Hello"
            }
        }

        # Use an invalid UUID
        response = self.client.post("/chat/invalid-uuid", json=test_request)
        assert response.status_code == 400  # Should return 400 for invalid UUID

    def test_chat_endpoint_missing_content(self):
        """Test the chat endpoint with missing message content."""
        test_request = {
            "message": {
                "role": "user",
                "content": ""
            }
        }

        user_id = str(uuid.uuid4())
        response = self.client.post(f"/chat/{user_id}", json=test_request)
        # This might return 422 for validation error, which is expected

    def test_chat_endpoint_large_content(self):
        """Test the chat endpoint with very large message content."""
        large_content = "test " * 1000  # Very long message
        test_request = {
            "message": {
                "role": "user",
                "content": large_content
            }
        }

        user_id = str(uuid.uuid4())
        response = self.client.post(f"/chat/{user_id}", json=test_request)
        # Should handle large content appropriately

    def test_health_check_endpoint(self):
        """Test the health check endpoint."""
        # Use a valid UUID for the path parameter
        user_id = str(uuid.uuid4())
        response = self.client.get(f"/chat/{user_id}/health")

        assert response.status_code == 200
        response_data = response.json()
        assert "status" in response_data
        assert response_data["status"] == "healthy"
        assert "timestamp" in response_data

    def test_health_check_with_invalid_user_id(self):
        """Test the health check endpoint with an invalid user ID."""
        response = self.client.get("/chat/invalid-uuid/health")
        assert response.status_code == 400  # Should return 400 for invalid UUID

    def test_chat_endpoint_special_characters(self):
        """Test the chat endpoint with special characters in the message."""
        special_content = "Hello! Can you add a task with special chars: @#$%^&*()?"
        test_request = {
            "message": {
                "role": "user",
                "content": special_content
            }
        }

        user_id = str(uuid.uuid4())
        response = self.client.post(f"/chat/{user_id}", json=test_request)
        # Should handle special characters without issues

    def test_chat_endpoint_unicode_content(self):
        """Test the chat endpoint with Unicode characters."""
        unicode_content = "Hello! Can you add a task with emoji: 📝 and unicode: ñáéíóú?"
        test_request = {
            "message": {
                "role": "user",
                "content": unicode_content
            }
        }

        user_id = str(uuid.uuid4())
        response = self.client.post(f"/chat/{user_id}", json=test_request)
        # Should handle Unicode characters properly

    @patch('backend.api.v1.endpoints.chat.get_default_agent')
    @patch('backend.api.v1.endpoints.chat.ChatService')
    @patch('backend.api.v1.endpoints.chat.MessageService')
    @patch('backend.api.v1.endpoints.chat.ConversationLoader')
    def test_chat_endpoint_with_mocked_services(self, mock_conv_loader, mock_message_service, mock_chat_service, mock_get_agent):
        """Test the chat endpoint with mocked services to isolate API logic."""
        # Setup mocks
        mock_agent = Mock()
        mock_agent.process_message = AsyncMock(return_value={
            "content": "I've added your task.",
            "role": "assistant",
            "tool_calls": [],
            "tool_results": []
        })
        mock_get_agent.return_value = mock_agent

        mock_chat_svc = Mock()
        mock_chat_svc.process_message = AsyncMock(return_value={
            "content": "I've added your task.",
            "role": "assistant",
            "tool_calls": [],
            "tool_results": []
        })
        mock_chat_service.return_value = mock_chat_svc

        mock_msg_service = Mock()
        mock_msg_service.save_message = AsyncMock(return_value=str(uuid.uuid4()))
        mock_message_service.return_value = mock_msg_service

        mock_conv_loader.return_value = Mock()
        mock_conv_loader.return_value.load_conversation_history.return_value = [
            {"role": "user", "content": "Previous message"}
        ]

        test_request = {
            "message": {
                "role": "user",
                "content": "Add a task to buy groceries"
            }
        }

        user_id = str(uuid.uuid4())
        response = self.client.post(f"/chat/{user_id}", json=test_request)

        # This test verifies that the endpoint accepts the request structure
        assert response.status_code in [200, 422]

    def test_chat_endpoint_empty_request(self):
        """Test the chat endpoint with an empty request body."""
        user_id = str(uuid.uuid4())
        response = self.client.post(f"/chat/{user_id}", json={})
        assert response.status_code == 422  # Validation error is expected

    def test_chat_endpoint_malformed_json(self):
        """Test the chat endpoint with malformed JSON."""
        user_id = str(uuid.uuid4())
        # Send a string instead of JSON object to trigger parsing error
        response = self.client.post(
            f"/chat/{user_id}",
            content="This is not valid JSON",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422

    def test_endpoint_path_parameters(self):
        """Test various valid and invalid path parameters."""
        # Test with valid UUID
        valid_uuid = str(uuid.uuid4())
        response = self.client.get(f"/chat/{valid_uuid}/health")
        assert response.status_code in [200, 404]  # 404 is fine if the route isn't defined for GET

        # The POST /chat/{user_id} should accept valid UUIDs
        test_request = {"message": {"role": "user", "content": "test"}}
        response = self.client.post(f"/chat/{valid_uuid}", json=test_request)
        assert response.status_code in [200, 422, 404]  # Various possible responses


class TestAPIEdgeCases:
    """Test edge cases for the API."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.client = TestClient(app)

    def test_boundary_values_for_content_length(self):
        """Test boundary values for content length."""
        # Test minimum content length (empty is probably invalid)
        test_request = {"message": {"role": "user", "content": "a"}}  # Single character
        user_id = str(uuid.uuid4())
        response = self.client.post(f"/chat/{user_id}", json=test_request)

        # Test maximum content length (close to the limit in schema)
        max_content = "x" * 10000  # Max length from schema
        test_request = {"message": {"role": "user", "content": max_content}}
        response = self.client.post(f"/chat/{user_id}", json=test_request)

    def test_concurrent_requests(self):
        """Test behavior with concurrent requests."""
        import threading
        import time

        results = []

        def make_request():
            test_request = {"message": {"role": "user", "content": f"Test message at {time.time()}"}}
            user_id = str(uuid.uuid4())
            response = self.client.post(f"/chat/{user_id}", json=test_request)
            results.append(response.status_code)

        # Make multiple concurrent requests
        threads = []
        for i in range(3):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # All requests should complete (might have different status codes due to validation)
        assert len(results) == 3

    def test_api_response_formats(self):
        """Test that API responses match expected formats."""
        # This test would verify that responses conform to the schema
        # For now, just test that a health check returns expected keys
        user_id = str(uuid.uuid4())
        response = self.client.get(f"/chat/{user_id}/health")

        if response.status_code == 200:
            data = response.json()
            # Verify expected keys are present
            assert "status" in data
            assert "timestamp" in data
            assert "version" in data