# Wikipedia Search Engine

## Inverted Index Creation

To create the inverted index, run the following command. The arguments are the absolute paths to the Wikipedia XML dump file and the folder where the inverted index is to be created and stored.

```bash
./index.sh <path_to_wiki_dump_file> <path_to_index_folder>
```

## Searching

To search, run the following command.

```bash
./search.sh <path_to_index_folder>
```

Enter the query one by one to get the top 10 results.
