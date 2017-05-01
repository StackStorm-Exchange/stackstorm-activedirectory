#!/bin/sh
# subtree-pull
#
# Pull a specific subtree from its origin.
# Parameters: $1 -> The prefix of the subtree you wish to pull
#					we will automatically lookup where to pull from
#
exec < .gitsubtree
while read line
do
	git subtree pull --prefix=$line | cut -d" " -f1-1
done