# Wikipedia Search Engine

A search engine for searching [Wikipedia XML dumps](https://en.wikipedia.org/wiki/Wikipedia:Database_download).

## Requirements

python3 and nltk library is required to run the search engine.

## Creation of Inverted Index

To create the inverted index, run the following command.

```bash
./index.sh <path_to_wiki_dump_file> <path_to_index_folder>
```

The arguments are the absolute paths to the Wikipedia XML dump file and the folder where the inverted index is to be created and stored.

## Querying

To search, run the following command.

```bash
./search.sh <path_to_index_folder>
```

Enter the query one by one to get the top 10 ranked results.
