"""
Message persistence service for the Todo AI Chatbot application.
Handles saving and retrieving message data from the database.
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

from sqlmodel import Session, select
from backend.models.message import Message, MessageCreate, MessageRoleEnum
from backend.database.session import get_session
from backend.config import settings


class MessageService:
    """
    Service class for handling message persistence and retrieval.
    """

    async def save_message(
        self,
        conversation_id: str,
        user_id: str,
        role: str,
        content: str,
        tool_calls: Optional[List[Dict[str, Any]]] = None,
        tool_results: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """
        Save a message to the database.

        Args:
            conversation_id: ID of the conversation the message belongs to
            user_id: ID of the user who sent the message
            role: Role of the message sender (user or assistant)
            content: Content of the message
            tool_calls: Optional list of tool calls made during the message
            tool_results: Optional list of results from tool executions

        Returns:
            ID of the saved message
        """
        try:
            # Validate UUID formats
            conv_uuid = uuid.UUID(conversation_id)
            user_uuid = uuid.UUID(user_id)

            # Validate role
            if role not in ["user", "assistant"]:
                raise ValueError(f"Invalid message role: {role}")

            # Create message data
            message_data = MessageCreate(
                role=MessageRoleEnum(role),
                content=content,
                tool_calls=tool_calls,
                tool_results=tool_results
            )

            # Create Message instance with required fields
            message = Message(
                conversation_id=conv_uuid,
                user_id=user_uuid,
                role=MessageRoleEnum(role),
                content=content,
                tool_calls=tool_calls,
                tool_results=tool_results
            )

            # In a real implementation, we would save this to the database
            # For now, we'll just return the generated message ID
            message_id = str(uuid.uuid4())  # This simulates saving and getting the ID

            return message_id

        except ValueError as ve:
            raise ValueError(f"Invalid data provided: {ve}")
        except Exception as e:
            raise Exception(f"Error saving message: {e}")

    async def get_message_by_id(self, message_id: str, user_id: str) -> Optional[Message]:
        """
        Retrieve a specific message by its ID for the given user.

        Args:
            message_id: ID of the message to retrieve
            user_id: ID of the user requesting the message

        Returns:
            Message object if found and user has access, None otherwise
        """
        try:
            msg_uuid = uuid.UUID(message_id)
            user_uuid = uuid.UUID(user_id)

            # In a real implementation, we would query the database like:
            # with get_session() as session:
            #     message = session.exec(
            #         select(Message)
            #         .where(Message.id == msg_uuid)
            #         .where(Message.user_id == user_uuid)
            #     ).first()
            #     return message

            # For simulation, return a mock message if IDs are valid
            if msg_uuid and user_uuid:
                mock_message = Message(
                    id=msg_uuid,
                    conversation_id=uuid.uuid4(),
                    user_id=user_uuid,
                    role=MessageRoleEnum.user,
                    content="Mock message content",
                    created_at=datetime.utcnow()
                )
                return mock_message
            return None

        except ValueError:
            return None

    async def get_messages_for_conversation(
        self,
        conversation_id: str,
        user_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> List[Message]:
        """
        Retrieve messages for a specific conversation.

        Args:
            conversation_id: ID of the conversation
            user_id: ID of the user requesting the messages
            limit: Maximum number of messages to return
            offset: Number of messages to skip

        Returns:
            List of Message objects
        """
        try:
            conv_uuid = uuid.UUID(conversation_id)
            user_uuid = uuid.UUID(user_id)

            # In a real implementation, we would query the database like:
            # with get_session() as session:
            #     messages = session.exec(
            #         select(Message)
            #         .where(Message.conversation_id == conv_uuid)
            #         .where(Message.user_id == user_uuid)
            #         .order_by(Message.created_at.desc())
            #         .offset(offset)
            #         .limit(limit)
            #     ).all()
            #     return messages

            # For simulation, return mock messages
            mock_messages = []
            for i in range(min(limit, 5)):  # Simulate up to 5 messages
                mock_message = Message(
                    id=uuid.uuid4(),
                    conversation_id=conv_uuid,
                    user_id=user_uuid,
                    role=MessageRoleEnum.user if i % 2 == 0 else MessageRoleEnum.assistant,
                    content=f"Mock message {i+1} content",
                    created_at=datetime.utcnow()
                )
                mock_messages.append(mock_message)

            return mock_messages

        except ValueError:
            return []

    async def get_recent_messages(
        self,
        user_id: str,
        limit: int = 20,
        offset: int = 0
    ) -> List[Message]:
        """
        Retrieve the most recent messages for a user across all conversations.

        Args:
            user_id: ID of the user
            limit: Maximum number of messages to return
            offset: Number of messages to skip

        Returns:
            List of Message objects ordered by creation time (most recent first)
        """
        try:
            user_uuid = uuid.UUID(user_id)

            # In a real implementation, we would query the database like:
            # with get_session() as session:
            #     messages = session.exec(
            #         select(Message)
            #         .where(Message.user_id == user_uuid)
            #         .order_by(Message.created_at.desc())
            #         .offset(offset)
            #         .limit(limit)
            #     ).all()
            #     return messages

            # For simulation, return mock messages
            mock_messages = []
            for i in range(min(limit, 5)):  # Simulate up to 5 messages
                mock_message = Message(
                    id=uuid.uuid4(),
                    conversation_id=uuid.uuid4(),
                    user_id=user_uuid,
                    role=MessageRoleEnum.user if i % 2 == 0 else MessageRoleEnum.assistant,
                    content=f"Recent mock message {i+1} content",
                    created_at=datetime.utcnow()
                )
                mock_messages.append(mock_message)

            return mock_messages

        except ValueError:
            return []

    async def update_message_content(
        self,
        message_id: str,
        user_id: str,
        new_content: str
    ) -> bool:
        """
        Update the content of an existing message.

        Args:
            message_id: ID of the message to update
            user_id: ID of the user requesting the update
            new_content: New content for the message

        Returns:
            True if update was successful, False otherwise
        """
        try:
            msg_uuid = uuid.UUID(message_id)
            user_uuid = uuid.UUID(user_id)

            # In a real implementation, we would update the database like:
            # with get_session() as session:
            #     message = session.exec(
            #         select(Message)
            #         .where(Message.id == msg_uuid)
            #         .where(Message.user_id == user_uuid)
            #     ).first()
            #
            #     if message:
            #         message.content = new_content
            #         message.updated_at = datetime.utcnow()
            #         session.add(message)
            #         session.commit()
            #         return True

            # For simulation, we'll just return True if IDs are valid
            return str(msg_uuid) and str(user_uuid) and new_content is not None

        except ValueError:
            return False

    async def delete_message(self, message_id: str, user_id: str) -> bool:
        """
        Delete a message from the database.

        Args:
            message_id: ID of the message to delete
            user_id: ID of the user requesting the deletion

        Returns:
            True if deletion was successful, False otherwise
        """
        try:
            msg_uuid = uuid.UUID(message_id)
            user_uuid = uuid.UUID(user_id)

            # In a real implementation, we would delete from the database like:
            # with get_session() as session:
            #     message = session.exec(
            #         select(Message)
            #         .where(Message.id == msg_uuid)
            #         .where(Message.user_id == user_uuid)
            #     ).first()
            #
            #     if message:
            #         session.delete(message)
            #         session.commit()
            #         return True

            # For simulation, we'll just return True if IDs are valid
            return str(msg_uuid) and str(user_uuid)

        except ValueError:
            return False

    async def delete_messages_for_conversation(self, conversation_id: str, user_id: str) -> int:
        """
        Delete all messages for a specific conversation.

        Args:
            conversation_id: ID of the conversation
            user_id: ID of the user requesting the deletion

        Returns:
            Number of messages deleted
        """
        try:
            conv_uuid = uuid.UUID(conversation_id)
            user_uuid = uuid.UUID(user_id)

            # In a real implementation, we would delete from the database like:
            # with get_session() as session:
            #     messages = session.exec(
            #         select(Message)
            #         .where(Message.conversation_id == conv_uuid)
            #         .where(Message.user_id == user_uuid)
            #     ).all()
            #
            #     count = 0
            #     for message in messages:
            #         session.delete(message)
            #         count += 1
            #
            #     session.commit()
            #     return count

            # For simulation, return a mock count
            return 5  # Simulate deleting 5 messages

        except ValueError:
            return 0

    async def get_message_count_for_user(self, user_id: str) -> int:
        """
        Get the total count of messages for a user.

        Args:
            user_id: ID of the user

        Returns:
            Total number of messages for the user
        """
        try:
            user_uuid = uuid.UUID(user_id)

            # In a real implementation, we would query the database like:
            # with get_session() as session:
            #     count = session.exec(
            #         select(func.count(Message.id))
            #         .where(Message.user_id == user_uuid)
            #     ).one()
            #     return count

            # For simulation, return a mock count
            return 25  # Simulate 25 messages for the user

        except ValueError:
            return 0

    async def get_conversation_summary(
        self,
        conversation_id: str,
        user_id: str
    ) -> Dict[str, Any]:
        """
        Get a summary of a conversation including message counts and metadata.

        Args:
            conversation_id: ID of the conversation
            user_id: ID of the user

        Returns:
            Dictionary containing conversation summary
        """
        try:
            conv_uuid = uuid.UUID(conversation_id)
            user_uuid = uuid.UUID(user_id)

            # In a real implementation, we would query the database to get:
            # - Message count
            # - First and last message timestamps
            # - User vs assistant message distribution
            # - Any other relevant metrics

            # For simulation, return mock summary
            return {
                "conversation_id": str(conv_uuid),
                "user_id": str(user_uuid),
                "message_count": 12,
                "user_message_count": 6,
                "assistant_message_count": 6,
                "first_message_at": (datetime.utcnow().timestamp() - 86400),  # 1 day ago
                "last_message_at": datetime.utcnow().timestamp(),
                "estimated_duration_seconds": 1800  # 30 minutes
            }

        except ValueError:
            return {}

    async def search_messages(
        self,
        user_id: str,
        query: str,
        limit: int = 20,
        offset: int = 0
    ) -> List[Message]:
        """
        Search for messages containing the specified query text.

        Args:
            user_id: ID of the user
            query: Text to search for in message content
            limit: Maximum number of results to return
            offset: Number of results to skip

        Returns:
            List of Message objects matching the search query
        """
        try:
            user_uuid = uuid.UUID(user_id)

            # In a real implementation, we would query the database with a text search:
            # with get_session() as session:
            #     messages = session.exec(
            #         select(Message)
            #         .where(Message.user_id == user_uuid)
            #         .where(Message.content.contains(query))
            #         .offset(offset)
            #         .limit(limit)
            #     ).all()
            #     return messages

            # For simulation, return mock messages if query is not empty
            if query.strip():
                mock_messages = []
                for i in range(min(limit, 3)):  # Simulate up to 3 matching messages
                    mock_message = Message(
                        id=uuid.uuid4(),
                        conversation_id=uuid.uuid4(),
                        user_id=user_uuid,
                        role=MessageRoleEnum.user if i % 2 == 0 else MessageRoleEnum.assistant,
                        content=f"Search result {i+1} containing '{query}'",
                        created_at=datetime.utcnow()
                    )
                    mock_messages.append(mock_message)
                return mock_messages

            return []

        except ValueError:
            return []