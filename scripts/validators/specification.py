from pathlib import Path
from typing import List
import subprocess

class SpecificationValidator:

    SUCCESS = 0
    ERROR = 1

    def __init__(self, root_dir: str = 'tasks'):
        self.root_dir = Path(root_dir)
        self.errors: List[str] = []
        self.status: int = self.SUCCESS
    
    def validate_all_tasks(self) -> bool:
        if not self.root_dir.exists():
            self.errors.append(f"Root directory '{self.root_dir}' not found")
            return False
        
        for category in self.root_dir.iterdir():
            if not category.is_dir():
                continue

            for task in category.iterdir():
                print(task)
                if task.is_dir():
                    self._validate_task(task)
        
        return self.status == self.SUCCESS
    
    def _validate_task(self, task_path: Path) -> None:

        task_name = task_path.absolute().as_posix()
        result = subprocess.run(['ctf', 'challenge', 'lint', task_name])
        if result.returncode != self.SUCCESS:
            self.status = self.ERROR

    
    def get_errors(self) -> List[str]:
        return self.errors
