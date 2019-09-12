#!/bin/bash

if [[ "$#" -ne 1 ]]; then
    echo "Usage: ./search.sh <path_to_index_folder>"
    exit 2
fi

python3 search/wiki_search.py $1
