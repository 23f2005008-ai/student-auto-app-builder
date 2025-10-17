import requests
import time
import json
import os

class EvaluationClient:
    def __init__(self):
        self.max_retries = 3
        self.retry_delays = [1, 2, 4]
    
    def notify_evaluation(self, evaluation_url, payload):
        """Notify evaluation service with exponential backoff"""
        print(f"📤 Notifying evaluation service: {evaluation_url}")
        
        for attempt, delay in enumerate(self.retry_delays):
            try:
                response = requests.post(
                    evaluation_url,
                    json=payload,
                    headers={'Content-Type': 'application/json'},
                    timeout=30
                )
                
                if response.status_code == 200:
                    print("✅ Successfully notified evaluation service")
                    return True
                else:
                    print(f"⚠️ Attempt {attempt + 1} failed: {response.status_code}")
                    
            except requests.RequestException as e:
                print(f"⚠️ Attempt {attempt + 1} failed: {e}")
            
            if attempt < len(self.retry_delays) - 1:
                print(f"⏳ Retrying in {delay} seconds...")
                time.sleep(delay)
        
        print("❌ Failed to notify evaluation service after all retries")
        return False
    
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
