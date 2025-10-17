import base64
import time
from github import Github, GithubException
import os

class GitHubManager:
    def __init__(self):
        self.github = Github(os.getenv('GITHUB_TOKEN'))
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
            pages_url = f"https://{os.getenv('GITHUB_USERNAME')}.github.io/{repo.name}"
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
