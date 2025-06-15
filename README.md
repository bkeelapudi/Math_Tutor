# Math Tutor Slack Bot for Developers

A sophisticated Slack bot that provides expert guidance on mathematical concepts, algorithm complexity, and computational problems for developers. This bot automatically detects math-related questions in channels and provides detailed explanations, step-by-step solutions, and code examples.

## Features

- Automatically detects math-related questions in Slack channels
- Solves mathematical equations with step-by-step explanations
- Calculates statistics for datasets
- Provides algorithm complexity analysis
- Plots mathematical functions
- Explains mathematical concepts with code examples
- Responds in threads to keep channels clean

## Key Topics Covered

- **Discrete Mathematics**: Set theory, combinatorics, graph theory
- **Linear Algebra**: Matrices, vectors, transformations
- **Calculus**: Derivatives, integrals, optimization
- **Statistics & Probability**: Distributions, hypothesis testing, Bayesian methods
- **Algorithm Analysis**: Time and space complexity, Big O notation
- **Computational Geometry**: Algorithms for geometric problems
- **Number Theory**: Prime numbers, modular arithmetic, cryptography
- **Optimization**: Linear programming, gradient descent, evolutionary algorithms

## How It Works

1. Post any math-related question in a Slack channel where the bot is present
2. The bot automatically detects relevant questions and responds with:
   - Detailed explanations of mathematical concepts
   - Step-by-step solutions to problems
   - Code examples in Python
   - Visualizations when appropriate
3. Get comprehensive explanations tailored for developers

## Example Questions

- "What's the time complexity of quicksort?"
- "Can you solve the equation x^2 + 5x + 6 = 0?"
- "How do I calculate the dot product of two vectors in Python?"
- "What's the formula for standard deviation and how do I implement it?"
- "Can you explain how the RSA algorithm works?"

## Installation

1. Clone this repository
2. Run the installation script:
   ```bash
   ./install.sh
   ```
   This will:
   - Create a Python virtual environment
   - Install required dependencies
   - Create a `.env` file from the template

3. Edit the `.env` file with your Slack and AWS credentials:
   ```
   # Slack API Credentials
   SLACK_BOT_TOKEN=xoxb-your-bot-token
   SLACK_APP_TOKEN=xapp-your-app-token
   SLACK_SIGNING_SECRET=your-signing-secret

   # LLM Configuration
   MODEL_NAME=anthropic.claude-3-sonnet-20240229-v1:0

   # AWS Configuration (for Bedrock)
   AWS_REGION=us-east-1
   # AWS_ACCESS_KEY_ID=your-access-key
   # AWS_SECRET_ACCESS_KEY=your-secret-key
   # AWS_PROFILE=your-profile-name
   ```

4. Start the bot:
   ```bash
   ./start-bot.sh
   ```

## Slack App Setup

1. Create a new Slack app at https://api.slack.com/apps
2. Add the following Bot Token Scopes:
   - `app_mentions:read`
   - `channels:history`
   - `channels:read`
   - `chat:write`
   - `reactions:write`
3. Enable Socket Mode
4. Install the app to your workspace
5. Copy the Bot Token, Signing Secret, and App Token to your `.env` file

## Development

For development, you may want to install additional tools:
```bash
pip install pytest black flake8
```

## Configuration

The bot is configured in the `src/main.py` file and `config/system_prompt.py`. You can modify:

- The system prompt for the Math Tutor
- Math-related detection patterns
- Response formatting
- Slack event handling

## Technologies Used

- [Strands Agents SDK](https://github.com/strands-agents/sdk-python)
- Amazon Bedrock Claude for AI capabilities (default)
- Slack Bolt SDK for Slack integration
- NumPy, SymPy, and Matplotlib for mathematical operations
- Python 3.10+

## License

MIT
