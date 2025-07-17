#/bin/bash
set -e 

CHANGED_FILES=$(git diff-tree --no-commit-id --name-only -r $CI_COMMIT_SHA);
# CHANGED_APPS==$(git diff --name-only $CI_COMMIT_BEFORE_SHA...$CI_COMMIT_SHA | grep -E "deploy" | tr '\n' ',')
# echo "$CHANGED_APPS"

echo "Deploying all tasks in docker..."

for file in $CHANGED_FILES; do
	directory=$(dirname $file)
	if [[ $directory == */deploy ]]; then
		echo "Deploying $directory...";
		docker compose -f $directory/docker-compose.yml up --build -d; 
	fi
done

echo "All tasks are deployed"

CREATED_FILES=$(git diff --name-only --diff-filter=A HEAD~1..HEAD)
# changed_files=$(git diff-tree --no-commit-id --name-only -r $CI_COMMIT_SHA);

echo "Deploying all tasks in CTFd..."

for file in $CREATED_FILES; do
    directory=$( echo "$file" | sed -nE 's/(tasks\/(web|crypto|stego|forensic|osint|joy|reverse|pwn)\/[^\/]+?)\/.+?challenge\.(yaml|yml)/\1/p' )
    if [ -d "$directory" ]; then
		echo "Installing $directory";
		ctf challenge install $directory;
    fi
done

# echo "All tasks are deployed"
MODIFIED_FILES=$(git diff --name-only --diff-filter=M HEAD~1..HEAD)

for file in $MODIFIED_FILES; do
    directory=$( echo "$file" | sed -nE 's/(tasks\/(web|crypto|stego|forensic|osint|joy|reverse|pwn)\/[^\/]+?)\/.+?challenge\.(yaml|yml)/\1/p' )
    if [ -d "$directory" ]; then
		echo "Syncing $directory";
		ctf challenge sync $directory;
    fi
done