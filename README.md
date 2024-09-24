# Brawlhalla Viewership Rewards Bot

This script automates tracking of your progress and refreshing tokens for Brawlhalla Twitch viewership rewards. The bot periodically retrieves your bearer token, ensures you stay active on the reward servers, and tracks your progress.

## Features

- **Automated Token Refresh**: Automatically refreshes your Twitch OAuth token to ensure uninterrupted activity.
- **Reward Tracking**: Monitors progress towards viewership rewards on Brawlhalla.
- **Automated Activity**: Sends periodic requests to ensure you remain active on the server to earn rewards.

## Requirements

- Python 3.8+
- Valid Twitch OAuth token for authentication

## Setup

1. **Install Dependencies**: Run the following command to install the required Python packages:
   ```bash
   pip install -r requirements.txt
2. Authentication: You need to provide a valid Twitch OAuth token. When you run the bot for the first time, it will prompt you to enter your token. The token will be saved in auth-token.txt for subsequent use.
