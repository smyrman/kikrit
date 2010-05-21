#!/bin/bash
echo -e "USAGE: First edit script to make sure it's all ok. Remove the echo "\
"before git-filter. Then run it with:\n '$ dev_tools/rename_commiters.sh'\n"

echo git filter-branch -f --commit-filter '
	if [ "$GIT_COMMITTER_NAME" = "sindrero" ];
        then
                GIT_COMMITTER_NAME="Sindre Røkenes Myren";
                GIT_AUTHOR_NAME="Sindre Røkenes Myren";
                GIT_COMMITTER_EMAIL="smyrman@gmail.com";
                GIT_AUTHOR_EMAIL="smyrman@gmail.com";
                git commit-tree "$@";
	elif [ "$GIT_COMMITTER_NAME" = "sperre" ];
        then
                GIT_COMMITTER_NAME="Andreas Hopland Sperre";
                GIT_AUTHOR_NAME="Andreas Hopland Sperre";
                GIT_COMMITTER_EMAIL="andreas.sperre@gmail.com";
                GIT_AUTHOR_EMAIL="andreas.sperre@gmail.com";
                git commit-tree "$@";
        else
                git commit-tree "$@";
        fi' HEAD
