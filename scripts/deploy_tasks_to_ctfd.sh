#/bin/bash
set -e 

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