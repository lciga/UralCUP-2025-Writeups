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

CREATED_FILES=$(git diff --name-only --diff-filter=A HEAD~1..HEAD)

for file in $CREATED_FILES; do
    directory=$( echo "$file" | sed -nE 's/(tasks\/(web|crypto|stego|forensic|osint|joy|reverse|pwn)\/[^\/]+?)\/.+?challenge\.(yaml|yml)/\1/p' )
    if [ -d "$directory" ]; then
		ctf challenge install $directory;
    fi
done

MODIFIED_FILES=$(git diff --name-only --diff-filter=M HEAD~1..HEAD)

for file in $MODIFIED_FILES; do
    directory=$( echo "$file" | sed -nE 's/(tasks\/(web|crypto|stego|forensic|osint|joy|reverse|pwn)\/[^\/]+?)\/.+?challenge\.(yaml|yml)/\1/p' )
    if [ -d "$directory" ]; then
		ctf challenge sync $directory;
    fi
done