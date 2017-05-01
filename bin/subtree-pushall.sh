#!/bin/sh
# subtree-pushall
#
# Pushes all known subtrees back to their origin.
#
exec < .gitsubtree
while read line
do
	git subtree push --prefix=$line
done