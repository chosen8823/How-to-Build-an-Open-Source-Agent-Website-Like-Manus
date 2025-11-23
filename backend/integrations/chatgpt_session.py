#!/usr/bin/env python3
"""
🤖 ChatGPT Web Session Integration
Sign in once, use session tokens with auto-refresh
No API keys required - just your regular ChatGPT login
"""

import requests
import json
import time
import logging
from typing import Optional, Dict, List
from datetime import datetime, timedelta
import os

logger = logging.getLogger(__name__)


class ChatGPTSession:
    """
    ChatGPT Web Session Manager
    Uses session tokens from your browser to interact with ChatGPT
    """

    def __init__(self, access_token: Optional[str] = None):
        self.access_token = access_token or os.getenv('CHATGPT_ACCESS_TOKEN')
        self.session = requests.Session()
        self.conversation_id = None
        self.parent_message_id = None
        self.base_url = "https://chat.openai.com"
        self.backend_api_url = "https://chat.openai.com/backend-api"

        # Auto-refresh tracking
        self.token_expiry = None
        self.last_refresh = None

        if self.access_token:
            self._setup_session()

    def _setup_session(self):
        """Setup session headers with access token"""
        self.session.headers.update({
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/event-stream',
        })
        logger.info("✅ ChatGPT session configured with access token")

    def set_access_token(self, token: str):
        """Set access token (from browser cookies)"""
        self.access_token = token
        self._setup_session()
        logger.info("🔑 Access token updated")

    def refresh_token(self) -> bool:
        """
        Refresh the access token
        This happens automatically when using ChatGPT web
        """
        try:
            response = self.session.post(
                f"{self.backend_api_url}/refresh_token",
                json={}
            )

            if response.status_code == 200:
                data = response.json()
                new_token = data.get('access_token')
                if new_token:
                    self.set_access_token(new_token)
                    self.last_refresh = datetime.now()
                    logger.info("🔄 Token refreshed successfully")
                    return True

            logger.warning(f"Token refresh failed: {response.status_code}")
            return False

        except Exception as e:
            logger.error(f"Token refresh error: {e}")
            return False

    def send_message(self, message: str, conversation_id: Optional[str] = None) -> Dict:
        """
        Send a message to ChatGPT and get response

        Args:
            message: Your message to ChatGPT
            conversation_id: Optional conversation ID to continue existing chat

        Returns:
            Response data with ChatGPT's reply
        """
        if not self.access_token:
            raise ValueError("No access token set. Use set_access_token() first")

        # Use provided conversation_id or current one
        conv_id = conversation_id or self.conversation_id

        # Build request payload
        payload = {
            "action": "next",
            "messages": [{
                "id": self._generate_message_id(),
                "author": {"role": "user"},
                "content": {
                    "content_type": "text",
                    "parts": [message]
                },
            }],
            "model": "text-davinci-002-render-sha",
            "parent_message_id": self.parent_message_id or self._generate_message_id(),
        }

        if conv_id:
            payload["conversation_id"] = conv_id

        try:
            response = self.session.post(
                f"{self.backend_api_url}/conversation",
                json=payload,
                stream=True,
                timeout=60
            )

            if response.status_code == 401:
                # Try to refresh token
                logger.info("🔄 Token expired, refreshing...")
                if self.refresh_token():
                    # Retry with new token
                    return self.send_message(message, conversation_id)
                else:
                    raise Exception("Token refresh failed. Please update access token.")

            if response.status_code != 200:
                raise Exception(f"API request failed: {response.status_code} - {response.text}")

            # Parse streaming response
            response_text = ""
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith('data: '):
                        data_str = line_str[6:]  # Remove 'data: ' prefix
                        if data_str == '[DONE]':
                            break
                        try:
                            data = json.loads(data_str)
                            if 'message' in data:
                                msg = data['message']
                                if msg.get('author', {}).get('role') == 'assistant':
                                    response_text = msg.get('content', {}).get('parts', [''])[0]
                                    self.conversation_id = data.get('conversation_id')
                                    self.parent_message_id = msg.get('id')
                        except json.JSONDecodeError:
                            continue

            return {
                "success": True,
                "message": response_text,
                "conversation_id": self.conversation_id,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def new_conversation(self):
        """Start a new conversation"""
        self.conversation_id = None
        self.parent_message_id = None
        logger.info("💬 Started new conversation")

    def _generate_message_id(self) -> str:
        """Generate a random message ID"""
        import uuid
        return str(uuid.uuid4())

    def get_conversations(self) -> List[Dict]:
        """Get list of your ChatGPT conversations"""
        try:
            response = self.session.get(
                f"{self.backend_api_url}/conversations",
                params={"offset": 0, "limit": 28}
            )

            if response.status_code == 200:
                data = response.json()
                return data.get('items', [])

            return []

        except Exception as e:
            logger.error(f"Error fetching conversations: {e}")
            return []

    def delete_conversation(self, conversation_id: str) -> bool:
        """Delete a conversation"""
        try:
            response = self.session.patch(
                f"{self.backend_api_url}/conversation/{conversation_id}",
                json={"is_visible": False}
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error deleting conversation: {e}")
            return False


# Singleton instance
_chatgpt_instance: Optional[ChatGPTSession] = None


def get_chatgpt_session() -> ChatGPTSession:
    """Get or create ChatGPT session singleton"""
    global _chatgpt_instance
    if _chatgpt_instance is None:
        _chatgpt_instance = ChatGPTSession()
    return _chatgpt_instance
