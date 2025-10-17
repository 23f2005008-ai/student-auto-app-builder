import os

class Config:
    # GitHub Configuration
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', 'your_github_token_here')
    GITHUB_USERNAME = os.getenv('GITHUB_USERNAME', 'your_github_username')
    
    # Student Configuration
    STUDENT_EMAIL = os.getenv('STUDENT_EMAIL', 'your_email@example.com')
    STUDENT_SECRET = os.getenv('STUDENT_SECRET', 'your_secret_password')
    
    # LLM Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your_openai_key_here')
    LLM_MODEL = "gpt-3.5-turbo"
    
    # App Configuration
    MAX_BUILD_TIME = 600
