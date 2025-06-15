import os
import logging
import sys
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Add the SDK to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sdk-python/src"))

# Import from the Strands SDK
from strands.agent import Agent
from strands.models.bedrock import BedrockModel
from strands.agent.conversation_manager import SlidingWindowConversationManager
from strands.handlers.callback_handler import PrintingCallbackHandler

from src.tools import MathTools
from src.handlers import SlackEventHandlers
from src.utils import setup_logging
from config.system_prompt import MATH_TUTOR_SYSTEM_PROMPT

def main():
    # Load environment variables
    load_dotenv()
    
    # Set up logging
    logger = setup_logging()
    logger.info("Starting Math Tutor Slack Bot")
    
    # Initialize the Slack app
    app = App(
        token=os.environ["SLACK_BOT_TOKEN"],
        signing_secret=os.environ["SLACK_SIGNING_SECRET"],
        logger=logger
    )
    
    # Create the model with proper configuration
    model = BedrockModel(
        model_id=os.environ.get("MODEL_NAME", "anthropic.claude-3-sonnet-20240229-v1:0"),
        system_prompt=MATH_TUTOR_SYSTEM_PROMPT,
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    
    # Initialize math tools
    math_tools = MathTools()
    
    # Create a list of tools to pass to the Agent constructor
    tools = [
        {"name": "solve_equation", "function": math_tools.solve_equation},
        {"name": "calculate_statistics", "function": math_tools.calculate_statistics},
        {"name": "calculate_complexity", "function": math_tools.calculate_complexity},
        {"name": "plot_function", "function": math_tools.plot_function}
    ]
    
    # Initialize the Strands Agent with proper configuration
    math_agent = Agent(
        model=model,
        system_prompt=MATH_TUTOR_SYSTEM_PROMPT,
        conversation_manager=SlidingWindowConversationManager(),
        callback_handler=PrintingCallbackHandler() if os.environ.get("LOG_LEVEL") == "DEBUG" else None,
        tools=tools  # Pass the tools here
    )
    
    # Register Slack event handlers
    handlers = SlackEventHandlers(app, math_agent)
    
    # Start the app using Socket Mode
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    logger.info("Math Tutor Bot is running!")
    handler.start()

if __name__ == "__main__":
    main()
