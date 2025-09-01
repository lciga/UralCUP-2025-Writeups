import subprocess
from pathlib import Path
import requests

class Challenge:
    
    SUCCESS = 0

    def __init__(self, ctfd_api_key: str, ctfd_url: str):
        self.CTFD_API_KEY = ctfd_api_key
        self.CTFD_URL = ctfd_url

    def install(self, challenge_path: Path):
        result = subprocess.run(['ctf', 'challenge', 'install', challenge_path])
        if result.returncode != self.SUCCESS:
            raise Exception(f"Failed to install challenge {challenge_path}.")

    def sync(self, challenge_path: Path):
        result = subprocess.run(['ctf', 'challenge', 'sync', challenge_path])
        if result.returncode != self.SUCCESS:
            raise Exception(f"Failed to install challenge {challenge_path}.")
    
    def delete(self, challenge_id: int):
        headers = {
            'Authorization': f'Token {self.CTFD_API_KEY}',
            'Content-Type': 'application/json'
        }
        response = requests.delete(f'{self.CTFD_URL}/api/v1/challenges/{challenge_id}', headers=headers)
        if response.status_code != 200:
            raise Exception(f'Failed to remove challenge {challenge_id}')