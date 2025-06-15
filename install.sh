#!/bin/bash

echo "Installing Math Tutor Slack Bot..."

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from template if it doesn't exist
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file from template. Please edit it with your credentials."
fi

# Create necessary directories if they don't exist
mkdir -p src
mkdir -p config

echo "Installation complete!"
echo "Please edit the .env file with your Slack credentials and API keys."
echo "Then run ./start-bot.sh to start the bot."
