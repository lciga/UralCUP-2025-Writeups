#/bin/bash
set -e 

CHANGED_FILES=$(git diff-tree --no-commit-id --name-only --diff-filter=d -r $CI_COMMIT_SHA);
echo "$CHANGED_FILES"

for file in $CHANGED_FILES; do
	directory=$(dirname $file)
	if [[ $directory == */deploy ]]; then
		echo "Deploying $directory...";
		docker compose -f $directory/docker-compose.yml up --build -d;
		PORT=$(grep -Eo "[0-9]+:[0-9]+" docker-compose.yml | cut -d: -f1)
		echo "Deployed $directory on 195.66.114.196:$PORT"
	fi
done
