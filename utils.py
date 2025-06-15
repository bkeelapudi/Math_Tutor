import os
import logging
from typing import Dict, Any, Optional

def setup_logging() -> logging.Logger:
    """
    Set up logging configuration.
    
    Returns:
        Configured logger instance.
    """
    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        level=getattr(logging, log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger("math_tutor_bot")

def parse_tool_response(response: Dict[str, Any]) -> str:
    """
    Parse and format the response from a tool for better readability in Slack.
    
    Args:
        response: The raw response from a tool.
        
    Returns:
        Formatted string for Slack.
    """
    if not response.get("success", False):
        return f"Error: {response.get('error', 'Unknown error')}"
    
    if "solution" in response:
        # Format equation solution
        result = f"*Solution:* {response['solution']}\n\n"
        
        if "steps" in response and response["steps"]:
            result += "*Step-by-step solution:*\n"
            for i, step in enumerate(response["steps"], 1):
                result += f"{i}. {step}\n"
        
        return result
    
    elif "mean" in response:
        # Format statistics
        return (
            f"*Statistical Analysis:*\n"
            f"• Count: {response['count']}\n"
            f"• Mean: {response['mean']:.4f}\n"
            f"• Median: {response['median']:.4f}\n"
            f"• Standard Deviation: {response['std_dev']:.4f}\n"
            f"• Range: {response['min']:.4f} to {response['max']:.4f}\n"
            f"• Interquartile Range: {response['iqr']:.4f}"
        )
    
    elif "complexity" in response:
        # Format algorithm complexity
        complexity = response["complexity"]
        result = f"*Algorithm:* {response['algorithm']}\n\n"
        
        if isinstance(complexity.get("time"), dict):
            result += "*Time Complexity:*\n"
            result += f"• Best case: {complexity['time']['best']}\n"
            result += f"• Average case: {complexity['time']['average']}\n"
            result += f"• Worst case: {complexity['time']['worst']}\n"
        else:
            result += f"*Time Complexity:* {complexity.get('time', 'Unknown')}\n"
        
        result += f"*Space Complexity:* {complexity.get('space', 'Unknown')}\n"
        
        if "stable" in complexity:
            result += f"*Stable:* {'Yes' if complexity['stable'] else 'No'}\n"
        
        if "description" in complexity:
            result += f"\n*Description:*\n{complexity['description']}"
        
        return result
    
    # Default formatting
    return str(response)
