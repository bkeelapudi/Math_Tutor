from slack_bolt import App
import sys
import os
import re
import json
from typing import Dict, Any, List

# Add the SDK to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sdk-python/src"))

# Import from the Strands SDK
from strands.agent import Agent
from strands.agent.agent_result import AgentResult
from strands.types.content import ContentBlock

# Pattern to detect math-related questions
MATH_PATTERN = re.compile(
    r"(math|algorithm|complexity|big o|equation|formula|calculus|linear algebra|"
    r"statistics|probability|optimization|function|graph|plot|solve|compute|"
    r"matrix|vector|derivative|integral|theorem|proof)",
    re.IGNORECASE
)

class SlackEventHandlers:
    def __init__(self, app: App, agent: Agent):
        """
        Initialize the Slack event handlers.
        
        Args:
            app: The Slack Bolt app instance
            agent: The Strands Agent instance
        """
        self.app = app
        self.agent = agent
        self.register_handlers()
    
    def register_handlers(self):
        """Register all event handlers with the Slack app."""
        self.app.event("message")(self.handle_message_events)
        self.app.event("app_mention")(self.handle_app_mentions)
        self.app.event("reaction_added")(self.handle_reaction_added)
    
    def extract_text_from_result(self, result: AgentResult) -> str:
        """
        Extract text content from an AgentResult.
        
        Args:
            result: The AgentResult from the agent
            
        Returns:
            The extracted text content
        """
        # Extract text from content blocks
        text_parts = []
        
        # Handle different result formats
        if hasattr(result, "content") and isinstance(result.content, str):
            # Simple string content
            return result.content
        
        if hasattr(result, "content") and isinstance(result.content, List):
            # List of content blocks
            for block in result.content:
                if isinstance(block, Dict) and "text" in block:
                    text_parts.append(block["text"])
        
        # If we have text parts, join them
        if text_parts:
            return "\n".join(text_parts)
        
        # Fallback: convert the entire result to a string
        return str(result)
    
    def handle_message_events(self, body: Dict[str, Any], logger: Any):
        """
        Handle message events in channels.
        
        Args:
            body: The event payload
            logger: The logger instance
        """
        event = body["event"]
        
        # Skip messages from the bot itself
        if event.get("bot_id"):
            return
        
        channel_id = event["channel"]
        thread_ts = event.get("thread_ts", event["ts"])
        user_message = event.get("text", "")
        
        # Check if the message contains math-related keywords
        if MATH_PATTERN.search(user_message):
            # React to the message to acknowledge
            try:
                self.app.client.reactions_add(
                    channel=channel_id,
                    timestamp=event["ts"],
                    name="brain"
                )
            except Exception as e:
                logger.error(f"Error adding reaction: {e}")
            
            # Process the message with the Strands Agent
            try:
                result = self.agent(user_message)
                text_response = self.extract_text_from_result(result)
                
                # Check if the response contains a base64 image
                if "image_base64" in text_response:
                    # This is a simplified approach - in a real app, you'd parse the JSON properly
                    # and upload the image to Slack using files_upload
                    text_response = "I've generated a plot for you, but I can't display it directly in Slack. " \
                                  "Here's the textual explanation instead."
                
                # Send the response in a thread
                self.app.client.chat_postMessage(
                    channel=channel_id,
                    thread_ts=thread_ts,
                    text=text_response
                )
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                self.app.client.chat_postMessage(
                    channel=channel_id,
                    thread_ts=thread_ts,
                    text=f"I encountered an error while processing your request: {str(e)}"
                )
    
    def handle_app_mentions(self, body: Dict[str, Any], logger: Any):
        """
        Handle direct mentions of the app.
        
        Args:
            body: The event payload
            logger: The logger instance
        """
        event = body["event"]
        channel_id = event["channel"]
        thread_ts = event.get("thread_ts", event["ts"])
        user_message = event.get("text", "")
        
        # Remove the app mention from the message
        user_message = re.sub(r"<@[A-Z0-9]+>", "", user_message).strip()
        
        # Process the message with the Strands Agent
        try:
            result = self.agent(user_message)
            text_response = self.extract_text_from_result(result)
            
            # Send the response in a thread
            self.app.client.chat_postMessage(
                channel=channel_id,
                thread_ts=thread_ts,
                text=text_response
            )
        except Exception as e:
            logger.error(f"Error processing mention: {e}")
            self.app.client.chat_postMessage(
                channel=channel_id,
                thread_ts=thread_ts,
                text=f"I encountered an error while processing your request: {str(e)}"
            )
    
    def handle_reaction_added(self, body: Dict[str, Any], logger: Any):
        """
        Handle reactions added to messages.
        
        Args:
            body: The event payload
            logger: The logger instance
        """
        event = body["event"]
        
        # Skip reactions from the bot itself
        if event.get("user") == self.app.client.auth_test()["user_id"]:
            return
        
        # Check if the reaction is "question" or "❓"
        if event.get("reaction") in ["question", "grey_question"]:
            channel_id = event["item"]["channel"]
            message_ts = event["item"]["ts"]
            
            # Get the message that was reacted to
            try:
                result = self.app.client.conversations_history(
                    channel=channel_id,
                    latest=message_ts,
                    inclusive=True,
                    limit=1
                )
                
                if result["messages"] and len(result["messages"]) > 0:
                    user_message = result["messages"][0].get("text", "")
                    
                    # Process the message with the Strands Agent
                    agent_result = self.agent(user_message)
                    text_response = self.extract_text_from_result(agent_result)
                    
                    # Send the response in a thread
                    self.app.client.chat_postMessage(
                        channel=channel_id,
                        thread_ts=message_ts,
                        text=text_response
                    )
            except Exception as e:
                logger.error(f"Error processing reaction: {e}")
