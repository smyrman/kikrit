#!/bin/sh
last="$1"
new="$2"
echo "git tag -a v$new"
echo "git archive --format=zip --prefix=kikrit-$new/ v$new > kikrit-$new.zip"
echo "git log --no-merges v$new ^v$last > ChangeLog-$new"
echo "git shortlog --no-merges v$new ^v$last > ShortLog"
echo "git diff --stat --summary -M v$last v$new > diffstat-$new"
