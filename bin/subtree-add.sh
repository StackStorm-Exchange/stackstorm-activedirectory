#!/bin/sh
# subtree-add
#
# Adds a new subtree to the current git repository.
# Parametrs are to be supplied in the same order as supplied to git subtree add
# From that point forward, using any of the other subtree tools, you may refer
# to your subtree by its prefix.
#
git subtree add --prefix=$1 $2 $3
if [ $? -eq 0 ]; then
    echo $1 $2 $3 >> .gitsubtree
fi
