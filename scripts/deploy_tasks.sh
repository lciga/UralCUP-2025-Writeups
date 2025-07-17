#/bin/bash
set -e 

changed_files=$(git diff-tree --no-commit-id --name-only -r $CI_COMMIT_SHA);
# CHANGED_APPS==$(git diff --name-only $CI_COMMIT_BEFORE_SHA...$CI_COMMIT_SHA | grep -E "deploy" | tr '\n' ',')
# echo "$CHANGED_APPS"

echo "Deploying all tasks in docker..."

for file in $changed_files; do
	directory=$(dirname $file)
	if [[ $directory == */deploy ]]; then
		echo "Deploying $directory...";
		docker compose -f $directory/docker-compose.yml up --build -d; 
	fi
done

echo "All tasks are deployed"

changed_files=$(git diff-tree --no-commit-id --name-only -r $CI_COMMIT_SHA);

echo "Deploying all tasks in CTFd..."
cd ..
echo `pwd`
for file in tasks/$changed_files; do
	echo "$file";
    directory=$( echo "$file" | sed -nE 's/(tasks\/(web|crypto|stego|forensic|osint|joy|reverse|pwn)\/[^\/]+?)\/.+?challenge\.(yaml|yml)/\1/p' )
    if [ -n "tasks/$directory" ]; then
		echo "Deploying $directory";
		ctf challenge install tasks/$directory;
    fi
done

# echo "All tasks are deployed"
