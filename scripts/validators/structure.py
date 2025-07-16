from pathlib import Path
from typing import List

class StructureValidator:

    REQUIRED_FILES = ['README.md', 'challenge.yml']
    DEPLOY_REQUIRED_FILES = ['docker-compose.yml', 'Dockerfile']

    def __init__(self, root_dir: str = 'tasks'):
        self.root_dir = Path(root_dir)
        self.errors: List[str] = []
    
    def validate_all_tasks(self) -> bool:
        if not self.root_dir.exists():
            self.errors.append(f"Root directory '{self.root_dir}' not found")
            return False
        
        for category in self.root_dir.iterdir():
            if not category.is_dir():
                continue

            for task in category.iterdir():
                if task.is_dir():
                    self._validate_task(task)
        
        return len(self.errors) == 0
    
    def _validate_task(self, task_path: Path) -> None:

        task_name = task_path.relative_to(self.root_dir)

        for file in self.REQUIRED_FILES:
            if not (task_path / file).exists():
                self.errors.append(f"{task_name}: Missing required file '{file}'")
        
        deploy_path = task_path / "deploy"
        if deploy_path.exists():
            for file in self.DEPLOY_REQUIRED_FILES:
                if not (deploy_path / file).exists():
                    self.errors.append(f"{task_name}/deploy: Missing required file '{file}'")
    
    def get_errors(self) -> List[str]:
        return self.errors
