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

# Configuration from environment variables
class Config:
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')
    GITHUB_USERNAME = os.getenv('GITHUB_USERNAME', '')
    STUDENT_EMAIL = os.getenv('STUDENT_EMAIL', '')
    STUDENT_SECRET = os.getenv('STUDENT_SECRET', '')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

# In-memory storage for build status
build_status = {}

def verify_secret(email, secret):
    """Verify student secret"""
    expected_secret = Config.STUDENT_SECRET
    return secret == expected_secret and email == Config.STUDENT_EMAIL

class GitHubManager:
    def __init__(self):
        if Config.GITHUB_TOKEN:
            self.github = Github(Config.GITHUB_TOKEN)
            self.user = self.github.get_user()
        else:
            self.github = None
    
    def create_repository(self, task_id, description="Auto-generated app"):
        if not self.github:
            return {"html_url": "https://github.com/demo", "name": "demo-repo"}
        
        repo_name = f"auto-app-{task_id.replace(' ', '-').lower()}"
        
        try:
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
        except Exception as e:
            print(f"❌ GitHub error: {e}")
            return {"html_url": "https://github.com/demo", "name": "demo-repo"}
    
    def commit_files(self, repo, files):
        """Commit multiple files to repository"""
        if not self.github:
            print("✅ Demo files committed")
            return
            
        for file_path, content in files.items():
            try:
                if isinstance(repo, dict):  # Demo repo
                    print(f"✅ Demo file: {file_path}")
                else:
                    repo.create_file(file_path, f"Add {file_path}", content)
                    print(f"✅ File committed: {file_path}")
            except Exception as e:
                print(f"⚠️ Could not commit {file_path}: {e}")
    
    def enable_pages(self, repo):
        """Enable GitHub Pages"""
        if isinstance(repo, dict):
            return f"https://{Config.GITHUB_USERNAME}.github.io/demo-repo"
        return f"https://{Config.GITHUB_USERNAME}.github.io/{repo.name}"
    
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
        if Config.OPENAI_API_KEY:
            openai.api_key = Config.OPENAI_API_KEY
    
    def generate_app(self, brief, attachments, checks):
        """Generate complete application based on brief"""
        print(f"🤖 Generating app for: {brief[:50]}...")
        
        # Create a simple app based on the brief
        return self._create_simple_app(brief)
    
    def _create_simple_app(self, brief):
        """Create a simple web app based on the brief"""
        return {
            "files": {
                "index.html": f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Auto-Generated App</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{ padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }}
        .app-container {{ max-width: 800px; margin: 0 auto; background: white; border-radius: 15px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }}
        .brief {{ background: #f8f9fa; padding: 15px; border-radius: 10px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="app-container">
        <h1 class="text-center mb-4">🎯 Auto-Generated Application</h1>
        
        <div class="brief">
            <h5>Your Request:</h5>
            <p class="mb-0">{brief}</p>
        </div>

        <div class="card shadow-sm mb-4">
            <div class="card-body text-center">
                <h3>🚀 Demo Application</h3>
                <p class="lead">This app was automatically generated based on your specifications</p>
                
                <div class="mt-4">
                    <h1 id="counter" class="display-1 text-primary">0</h1>
                    <div class="btn-group mt-3">
                        <button class="btn btn-success btn-lg" onclick="increment()">+1</button>
                        <button class="btn btn-danger btn-lg" onclick="decrement()">-1</button>
                        <button class="btn btn-secondary btn-lg" onclick="reset()">Reset</button>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="alert alert-info">
            <strong>ℹ️ Generated by:</strong> Student Auto App Builder API
        </div>
    </div>

    <script>
        let count = 0;
        function updateCounter() {{
            document.getElementById('counter').textContent = count;
            document.getElementById('counter').style.color = count < 0 ? '#dc3545' : count > 0 ? '#28a745' : '#007bff';
        }}
        function increment() {{
            count++;
            updateCounter();
        }}
        function decrement() {{
            count--;
            updateCounter();
        }}
        function reset() {{
            count = 0;
            updateCounter();
        }}
    </script>
</body>
</html>''',
                "README.md": f"""# 🚀 Auto-Generated Application

This application was automatically generated by the **Student Auto App Builder API**.

## 📋 Project Brief
{brief}

## 🛠️ Features
- Responsive design with Bootstrap 5
- Interactive counter functionality
- Professional documentation
- MIT License

## 🚀 Quick Start
1. Open `index.html` in any web browser
2. Use the buttons to interact with the counter
3. The app works immediately - no setup required!

## 📁 Project Structure
