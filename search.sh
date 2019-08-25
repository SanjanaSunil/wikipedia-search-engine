#!/bin/bash

if [[ "$#" -ne 3 ]]; then
    echo "Usage: ./search.sh <path_to_index_folder> <path_to_input_query_file> <path_to_output_file>"
    exit 2
fi

python3 search/wiki_search.py $1 $2 $3