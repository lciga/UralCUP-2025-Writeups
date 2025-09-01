import os
import sys
from typing import List, Dict
import requests
from pathlib import Path
import yaml
from utils.ctfd import Challenge

CTFD_API_KEY = os.environ.get('CTFD_API_KEY', None)
CTFD_URL = os.environ.get('CTFD_URL', None)

def fetch_current_ctfd_tasks() -> List[Dict]:
    headers = {
        'Authorization': f'Token {CTFD_API_KEY}',
        'Content-Type': 'application/json'
    }

    response = requests.get(f'{CTFD_URL}/api/v1/challenges', headers=headers)
    
    if response.status_code != 200 or response.json().get('success') != True:
        print(f"Unable to get challenges list from CTFd: {CTFD_URL}/api/v1/challenges")

    challenges: List[Dict] = response.json().get('data', [])

    return [
        {'name': ch.get('name', None), 
         'challenge_id': ch.get('id', None)}
            for ch in challenges]

def fetch_current_tasks(root_dir_name: str = 'tasks') -> List[Dict]:
    root_dir = Path(root_dir_name)
    if not root_dir.exists():
            print(f"Root directory '{root_dir}' not found")
            sys.exit(1)

    challenges: List = list()

    for category in root_dir.iterdir():
        if not category.is_dir():
            continue

        for task in category.iterdir():
            if task.is_dir():
                with open(task / 'challenge.yml', 'r') as challenge_file:
                    spec = yaml.safe_load(challenge_file)

                challenges.append({
                                    'name': spec.get('name', None),
                                    'path': task
                                    })
    
    return challenges


def main():
    ctfd_tasks = fetch_current_ctfd_tasks()
    repo_tasks = fetch_current_tasks()

    ctfd_challenge = Challenge(CTFD_API_KEY, CTFD_URL)

    ctfd_names = {challenge['name'] for challenge in ctfd_tasks}
    repo_names = {challenge['name'] for challenge in repo_tasks}

    to_delete = [challenge for challenge in ctfd_tasks if challenge['name'] not in repo_names]
    for challenge in to_delete:
        print(f'Deleting {challenge["name"]} challenge...')
        ctfd_challenge.delete(challenge['challenge_id'])
        print('Deleted!')
    
    to_install = [challenge for challenge in repo_tasks if challenge['name'] not in ctfd_names]
    for challenge in to_install:
        ctfd_challenge.install(challenge['path'])
    
    to_sync = [challenge for challenge in repo_tasks if challenge['name'] in ctfd_names]
    for challenge in to_sync:
        ctfd_challenge.sync(challenge['path'])

if __name__ == '__main__':
    main()