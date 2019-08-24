#!/bin/bash

if [[ "$#" -ne 2 ]]; then
    echo "Usage: ./index.sh <path-to-wiki-dump> <path_to_index_folder>"
    exit 2
fi

python3 index/wiki_indexer.py $1 $2
# inverted_index=$(ls temp | head -n 1)
# mv temp/inverted_index $2/'inverted_index.txt' ; rm -rf temp
