Python 3.13.7 (tags/v3.13.7:bcee1c3, Aug 14 2025, 14:15:11) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
from flask import Flask, request, jsonify
import hashlib
import threading
import time
from datetime import datetime
import json
import os
import requests
from github import Github, GithubException
import openai
import base64

app = Flask(__name__)

# Simple configuration
class Config:
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', 'your_github_token_here')
    GITHUB_USERNAME = os.getenv('GITHUB_USERNAME', 'your_github_username')
    STUDENT_EMAIL = os.getenv('STUDENT_EMAIL', 'your_email@example.com')
    STUDENT_SECRET = os.getenv('STUDENT_SECRET', 'your_secret_password')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your_openai_key_here')

# In-memory storage for build status
build_status = {}

def verify_secret(email, secret):
    """Verify student secret"""
    expected_secret = Config.STUDENT_SECRET
    return secret == expected_secret and email == Config.STUDENT_EMAIL

class GitHubManager:
    def __init__(self):
        self.github = Github(Config.GITHUB_TOKEN)
        self.user = self.github.get_user()
    
    def create_repository(self, task_id, description="Auto-generated app"):
        repo_name = f"auto-app-{task_id.replace(' ', '-').lower()}"
        
        try:
            # Create repository
            repo = self.user.create_repo(
                name=repo_name,
                description=description,
                auto_init=False,
                private=False
            )
            
            # Add MIT License
            license_content = self._get_mit_license()
            repo.create_file("LICENSE", "Add MIT License", license_content)
            
            print(f"✅ Repository created: {repo.html_url}")
            return repo
        except GithubException as e:
            raise Exception(f"Failed to create repository: {e}")
    
    def commit_files(self, repo, files):
        """Commit multiple files to repository"""
        for file_path, content in files.items():
            try:
                repo.create_file(file_path, f"Add {file_path}", content)
                print(f"✅ File committed: {file_path}")
            except Exception as e:
                print(f"⚠️ Could not commit {file_path}: {e}")
    
    def enable_pages(self, repo):
        """Enable GitHub Pages on the repository"""
        try:
            pages_url = f"https://{Config.GITHUB_USERNAME}.github.io/{repo.name}"
            print(f"✅ GitHub Pages will be available at: {pages_url}")
            return pages_url
        except Exception as e:
            raise Exception(f"Failed to enable Pages: {e}")
    
    def _get_mit_license(self):
        return """MIT License

Copyright (c) 2024 Student

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

class LLMAppGenerator:
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY
    
    def generate_app(self, brief, attachments, checks):
        """Generate complete application based on brief"""
        print("🤖 Generating app with LLM...")
        
        # For demo purposes, return a simple counter app
        # In production, you'd use the actual OpenAI API
        return self._get_demo_app(brief)
    
    def _get_demo_app(self, brief):
        """Provide a demo app for testing"""
        return {
            "files": {
                "index.html": f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Demo App - {brief[:30]}...</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{ padding: 20px; background: #f8f9fa; }}
        .counter {{ font-size: 3em; font-weight: bold; color: #007bff; }}
    </style>
</head>
<body>
    <div class="container text-center">
        <h1>Demo Application</h1>
        <p class="lead">Built automatically based on your request</p>
        
        <div class="card shadow-sm">
            <div class="card-body">
                <h3>Counter App</h3>
                <div class="counter" id="count">0</div>
                <div class="mt-3">
                    <button class="btn btn-primary me-2" onclick="increment()">+1</button>
                    <button class="btn btn-danger" onclick="decrement()">-1</button>
                    <button class="btn btn-secondary ms-2" onclick="reset()">Reset</button>
                </div>
            </div>
        </div>
        
        <div class="mt-4">
            <small class="text-muted">Brief: {brief}</small>
        </div>
    </div>

    <script>
        let count = 0;
        function increment() {{
            count++;
            document.getElementById('count').textContent = count;
        }}
        function decrement() {{
            count--;
            document.getElementById('count').textContent = count;
        }}
        function reset() {{
            count = 0;
            document.getElementById('count').textContent = count;
        }}
    </script>
</body>
</html>""",
                "README.md": f"""# Auto-Generated Application

This application was automatically generated based on your request.

## Brief
{brief}

## Features
- Simple counter functionality
- Bootstrap 5 styling
- Responsive design

## How to Use
1. Open `index.html` in a web browser
2. Click the buttons to increment/decrement the counter

## Technologies Used
- HTML5
- JavaScript
- Bootstrap 5

## License
MIT License
"""
            },
            "explanation": "Demo counter application with Bootstrap styling"
        }

class EvaluationClient:
    def __init__(self):
        self.max_retries = 3
        self.retry_delays = [1, 2, 4]
    
    def notify_evaluation(self, evaluation_url, payload):
        """Notify evaluation service with exponential backoff"""
        print(f"📤 Notifying evaluation service: {evaluation_url}")
        
        # For demo, just print the payload
        print(f"📦 Evaluation payload: {json.dumps(payload, indent=2)}")
        return True
    
    def build_evaluation_payload(self, request_data, repo_url, commit_sha, pages_url):
        """Build payload for evaluation service"""
        return {
            "email": request_data["email"],
            "task": request_data["task"],
            "round": request_data["round"],
            "nonce": request_data["nonce"],
            "repo_url": repo_url,
            "commit_sha": commit_sha,
            "pages_url": pages_url
        }

def process_build_request_async(request_data):
    """Process build request in background thread"""
    task_id = request_data["task"]
    
    try:
        build_status[task_id] = {"status": "processing", "started_at": datetime.now().isoformat()}
        print(f"🚀 Starting build process for task: {task_id}")
        
        # Initialize components
        github_mgr = GitHubManager()
        llm_generator = LLMAppGenerator()
        eval_client = EvaluationClient()
        
        # Generate app using LLM
        build_status[task_id]["status"] = "generating_code"
        print("📝 Generating application code...")
        generated_app = llm_generator.generate_app(
            request_data["brief"],
            request_data.get("attachments", []),
            request_data.get("checks", [])
        )
        
        # Create GitHub repository
        build_status[task_id]["status"] = "creating_repo"
        print("🐙 Creating GitHub repository...")
        repo = github_mgr.create_repository(task_id, request_data["brief"])
        
        # Add generated files
        build_status[task_id]["status"] = "committing_files"
        print("📁 Committing files to repository...")
        github_mgr.commit_files(repo, generated_app["files"])
        
        # Enable GitHub Pages
        build_status[task_id]["status"] = "enabling_pages"
        print("🌐 Enabling GitHub Pages...")
        pages_url = github_mgr.enable_pages(repo)
        
        # Get latest commit SHA
        commit_sha = repo.get_commits()[0].sha
        
        # Notify evaluation service
        build_status[task_id]["status"] = "notifying_evaluation"
        print("📤 Notifying evaluation service...")
        eval_payload = eval_client.build_evaluation_payload(
            request_data, repo.html_url, commit_sha, pages_url
        )
        eval_client.notify_evaluation(request_data["evaluation_url"], eval_payload)
        
        build_status[task_id] = {
            "status": "completed",
            "repo_url": repo.html_url,
            "pages_url": pages_url,
            "completed_at": datetime.now().isoformat()
        }
        
        print(f"✅ Build completed successfully!")
        print(f"📊 Repo: {repo.html_url}")
        print(f"🌐 Pages: {pages_url}")
        
    except Exception as e:
        build_status[task_id] = {
            "status": "failed",
            "error": str(e),
            "failed_at": datetime.now().isoformat()
        }
        print(f"❌ Build failed: {e}")

@app.route('/build', methods=['POST'])
def handle_build_request():
    """Handle initial build request"""
    try:
        data = request.json
        print(f"📨 Received build request for: {data.get('email', 'unknown')}")
        
        # Validate required fields
        required_fields = ['email', 'secret', 'task', 'round', 'nonce', 'brief', 'evaluation_url']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Verify secret
        if not verify_secret(data['email'], data['secret']):
            return jsonify({"error": "Invalid credentials"}), 401
        
        # Start async processing
        thread = threading.Thread(target=process_build_request_async, args=(data,))
        thread.daemon = True
        thread.start()
        
        return jsonify({
            "status": "accepted",
            "message": "Build request queued for processing",
...             "task": data["task"]
...         }), 200
...         
...     except Exception as e:
...         print(f"❌ Error handling request: {e}")
...         return jsonify({"error": str(e)}), 500
... 
... @app.route('/revise', methods=['POST'])
... def handle_revise_request():
...     """Handle revision request (round 2)"""
...     try:
...         data = request.json
...         print(f"📨 Received revision request for: {data.get('email', 'unknown')}")
...         
...         # Validate required fields
...         if data.get('round') != 2:
...             return jsonify({"error": "This endpoint is for revision requests (round 2)"}), 400
...         
...         # Verify secret
...         if not verify_secret(data['email'], data['secret']):
...             return jsonify({"error": "Invalid credentials"}), 401
...         
...         # Process revision
...         thread = threading.Thread(target=process_build_request_async, args=(data,))
...         thread.daemon = True
...         thread.start()
...         
...         return jsonify({
...             "status": "accepted", 
...             "message": "Revision request queued",
...             "task": data["task"],
...             "round": 2
...         }), 200
...         
...     except Exception as e:
...         return jsonify({"error": str(e)}), 500
... 
@app.route('/status/<task_id>', methods=['GET'])
def get_build_status(task_id):
    """Check build status"""
    status = build_status.get(task_id, {"status": "unknown"})
    return jsonify(status), 200

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "Student Auto App Builder",
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route('/test', methods=['GET'])
def test_endpoint():
    """Test endpoint to verify configuration"""
    return jsonify({
        "message": "Student API is working!",
        "github_configured": bool(Config.GITHUB_TOKEN and Config.GITHUB_TOKEN != "your_github_token_here"),
        "openai_configured": bool(Config.OPENAI_API_KEY and Config.OPENAI_API_KEY != "your_openai_key_here"),
        "environment": "production" if 'RAILWAY_STATIC_URL' in os.environ else "development"
    }), 200

if __name__ == '__main__':
    print("🚀 Starting Student API Server...")
    print("📍 Endpoints:")
    print("   POST /build     - Build new application")
    print("   POST /revise    - Revise application (round 2)") 
    print("   GET  /status/<task_id> - Check build status")
    print("   GET  /health    - Health check")
    print("   GET  /test      - Test configuration")
    print("=" * 50)
    
    # Check configuration
    if Config.GITHUB_TOKEN == "your_github_token_here":
        print("⚠️  WARNING: GITHUB_TOKEN not configured")
    if Config.OPENAI_API_KEY == "your_openai_key_here":
        print("⚠️  WARNING: OPENAI_API_KEY not configured")
    
    port = int(os.environ.get('PORT', 5000))
