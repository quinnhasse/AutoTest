import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
EXA_API_KEY = os.getenv('EXA_API_KEY')
REPO_NAME = os.getenv('REPO_NAME')

if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN not set in environment variables")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not set in environment variables")
if not EXA_API_KEY:
    raise ValueError("EXA_API_KEY not set in environment variables")
if not REPO_NAME:
    raise ValueError("REPO_NAME not set in environment variables")