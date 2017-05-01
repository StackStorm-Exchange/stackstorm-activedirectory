#!/bin/sh
# subtree-remove
#
# Removes a subtree from being manage by this system.  But
# leaves the files intact.  If you wish to remove the subtree files too
# simply delete the directory.
# Parameters: $1 -> The prefix of the subtree to delete.
# 
mv .gitsubtree .gitsubtree.bak
exec < .gitsubtree.bak
while read line
do
    if [[ $line != $1* ]] 
	then
		echo $line >> .gitsubtree
	fi
done
rm .gitsubtree.bak