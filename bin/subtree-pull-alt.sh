#!/bin/sh
# subtree-pull-alt
#
# Pull a specific subtree from its origin. Goes directly to 
# git because sometimes git subtree pull just fails :-(
# Parameters: $1 -> The prefix of the subtree you wish to pull
#					we will automatically lookup where to pull from
#
exec < .gitsubtree
while read line
do
    if [[ $line == $1* ]] 
	then
		git pull -s subtree ${line#*$1}
	fi
done