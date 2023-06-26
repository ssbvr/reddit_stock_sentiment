import os
from dotenv import load_dotenv

load_dotenv()

# Reddit API Configurations
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_SECRET = os.getenv("REDDIT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

# working directory
WORK_DIR = os.getenv("WORK_DIR")