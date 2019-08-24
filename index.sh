#!/bin/bash

if [[ "$#" -ne 2 ]]; then
    echo "Usage: python3 <path-to-wiki-dump> <path_to_index_folder>"
    exit 2
fi

python3 index/wiki_indexer.py $1 $2