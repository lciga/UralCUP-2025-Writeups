#/bin/bash
set -e 

CHANGED_FILES=$(git diff-tree --no-commit-id --name-only -r $CI_COMMIT_SHA);

for file in $CHANGED_FILES; do
	directory=$(dirname $file)
	if [[ $directory == */deploy ]]; then
		echo "Deploying $directory...";
		docker compose -f $directory/docker-compose.yml up --build -d; 
	fi
done
